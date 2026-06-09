import numpy as np


def allan_windows(K, density=64):
    """
    Generate logarithmically spaced Allan variance averaging windows.

    Allan variance is evaluated over a range of averaging times rather
    than a single window length. This function generates a set of unique
    averaging-window sizes that are approximately logarithmically spaced,
    providing good coverage of both short-term and long-term sensor
    behavior.

    Parameters
    ----------
    K : int
        Number of samples in the sensor time series.

    density : int, optional
        Approximate number of window sizes per decade on the logarithmic
        scale. Larger values produce smoother Allan variance curves at the
        expense of additional computation.

    Returns
    -------
    M : ndarray
        Array of unique averaging-window lengths (samples).

        Each value of M corresponds to an Allan variance averaging time:

            tau = M * dt

        where dt is the sensor sampling period.
    """

    # Maximum averaging window is limited to approximately half the
    # available dataset length to ensure sufficient statistics.
    e_max = np.log10(np.floor(K / 2))

    # Generate logarithmically spaced candidate window lengths.
    M_real = np.logspace(0, e_max, round(e_max * density))

    # Convert to integer sample counts and remove duplicates introduced
    # by rounding.
    M = np.unique(np.round(M_real)).astype(int)

    return M


def allan_variance(y, M):
    """
    Compute the overlapping Allan variance of a time series.

    Allan variance is a statistical tool commonly used to characterize
    stochastic inertial sensor errors such as:

    - quantization noise,
    - white noise,
    - bias instability,
    - rate random walk,
    - and ramp noise.

    This implementation uses the overlapping Allan variance formulation,
    which provides improved statistical confidence by utilizing all
    possible overlapping averaging windows.

    Parameters
    ----------
    y : ndarray
        Time series to analyze.

        Typically a sequence of gyroscope or accelerometer measurements.

    M : ndarray
        Averaging window lengths (samples).

        Each value corresponds to an Allan averaging time:

            tau = M * dt

        where dt is the sampling period.

    Returns
    -------
    v : ndarray
        Allan variance evaluated at each averaging window length in M.
    """

    # Cumulative sum of the signal.
    #
    # Using cumulative sums allows the overlapping Allan variance to be
    # computed efficiently without explicitly forming every averaging
    # window.
    Y = np.cumsum(y)

    # Allan variance storage.
    v = np.zeros(len(M))

    for n_tau, m in enumerate(M):

        # Shifted cumulative-sum windows used to form the overlapping
        # second-difference operator.
        Yc = Y[(2 * m - 1):]
        Yb = Y[(m - 1):(-m)]
        Yj = Y[:(1 - 2 * m)]
        yj = y[:(1 - 2 * m)]

        # Overlapping Allan variance second difference.
        #
        # This quantity measures how the average value of the signal
        # changes between adjacent averaging windows of length m.
        delta = (Yc - 2 * Yb + Yj - yj) / m

        # Allan variance estimate at averaging window m.
        v[n_tau] = np.mean(delta**2) / 2

    return v


def generate_quantization_noise(sigma_q, K, dt):
    """
    Generate quantization noise.

    Quantization noise arises from the finite resolution of a digital
    sensor. Because the sensor output can only represent discrete values,
    small rounding errors are introduced into the measurements.

    This implementation follows the stochastic quantization-noise model
    commonly used in Allan variance analysis and inertial sensor
    characterization.

    Parameters
    ----------
    sigma_q : float
        Quantization noise coefficient.

    K : int
        Number of samples to generate.

    dt : float
        Sampling period (s).

    Returns
    -------
    n_q : ndarray, shape (K,)
        Quantization noise realization.
    """

    # Generate a Gaussian random sequence.
    w = np.random.randn(K + 1)

    # Quantization noise is modeled as the first difference of the
    # random sequence scaled by the quantization coefficient.
    n_q = (sigma_q / dt) * np.diff(w)

    return n_q


def generate_white_noise(sigma_rw, K, dt):
    """
    Generate white measurement noise.

    White noise models random sample-to-sample measurement uncertainty and
    is typically the dominant short-term error source in inertial sensors.

    In Allan variance analysis, this process corresponds to:

    - Angle Random Walk (ARW) for gyroscopes
    - Velocity Random Walk (VRW) for accelerometers

    White noise samples are independent and identically distributed with
    zero mean and constant variance.

    Parameters
    ----------
    sigma_rw : float
        Random-walk coefficient.

        Typically specified as:

        - rad / sqrt(s) for gyroscopes
        - m/s / sqrt(s) for accelerometers

    K : int
        Number of samples to generate.

    dt : float
        Sampling period (s).

    Returns
    -------
    n_rw : ndarray, shape (K,)
        White-noise realization.
    """

    # Generate independent Gaussian samples.
    w = np.random.randn(K)

    # Scale the samples to achieve the desired continuous-time
    # random-walk intensity.
    n_rw = (sigma_rw / np.sqrt(dt)) * w

    return n_rw


def generate_fogm_noise(sigma_f, K, dt, tau_f):
    """
    Generate first-order Gauss-Markov (FOGM) noise.

    A FOGM process models a slowly varying, time-correlated sensor bias.
    In inertial sensor modeling, this is commonly used to represent bias
    instability.

    Unlike white noise, consecutive samples are correlated. The correlation
    decays exponentially with time constant `tau_f`.

    Parameters
    ----------
    sigma_f : float
        Steady-state standard deviation of the FOGM process.

    K : int
        Number of samples to generate.

    dt : float
        Sampling period (s).

    tau_f : float
        Correlation time constant (s).

    Returns
    -------
    n_f : ndarray, shape (K,)
        First-order Gauss-Markov noise realization.
    """

    # Initialize the correlated bias process.
    n_f = np.zeros(K)

    # Steady-state variance of the FOGM process.
    v_f = sigma_f**2

    # Discrete-time driving-noise variance chosen so that the process
    # approaches the desired steady-state variance.
    v_hat = v_f * (1.0 - np.exp(-2.0 * dt / tau_f))

    # Propagate the Gauss-Markov process.
    for i in range(1, K):
        n_f[i] = (
            np.exp(-dt / tau_f) * n_f[i - 1]
            + np.sqrt(v_hat) * np.random.randn()
        )

    return n_f


def generate_brownian_noise(sigma_b, K, dt):
    """
    Generate Brownian noise (rate random walk).

    Brownian noise is produced by integrating white noise over time,
    resulting in a random-walk process whose variance grows with time.

    In inertial sensor modeling, this process is commonly used to
    represent rate random walk and other long-term drifting error
    sources.

    Unlike white noise or Gauss-Markov noise, Brownian noise is
    non-stationary and does not converge to a finite variance.

    Parameters
    ----------
    sigma_b : float
        Brownian-noise coefficient.

    K : int
        Number of samples to generate.

    dt : float
        Sampling period (s).

    Returns
    -------
    n_b : ndarray, shape (K,)
        Brownian-noise realization.
    """

    # Generate a white-noise driving process.
    w = np.random.randn(K)

    # Integrate the white noise to produce a random walk.
    #
    # The sqrt(dt) scaling preserves the continuous-time Brownian
    # motion intensity as the sampling rate changes.
    n_b = np.cumsum(sigma_b * np.sqrt(dt) * w)

    return n_b


def generate_ramp_noise(sigma_r, K, dt):
    """
    Generate ramp noise.

    Ramp noise models a continuously drifting sensor bias and is often
    used to represent very low-frequency error sources that dominate at
    long averaging times.

    This process is generated by double integrating white noise,
    producing a smoothly varying drift whose variance grows faster than
    a standard random walk.

    In Allan variance analysis, ramp noise is associated with the
    longest-term error behavior and can eventually dominate all other
    stochastic error sources.

    Parameters
    ----------
    sigma_r : float
        Ramp-noise coefficient.

    K : int
        Number of samples to generate.

    dt : float
        Sampling period (s).

    Returns
    -------
    n_r : ndarray, shape (K,)
        Ramp-noise realization.
    """

    # Generate a white-noise driving process.
    w = np.random.randn(K)

    # Double integration of the driving noise produces a smooth,
    # continuously drifting ramp-like error process.
    n_r = np.cumsum(
        np.cumsum(
            sigma_r * np.sqrt(2 / K) * dt * w
        )
    )

    return n_r