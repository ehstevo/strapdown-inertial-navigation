"""
Coarse Static Alignment Demonstration

Estimate IMU orientation and latitude from stationary accelerometer and
gyroscope measurements using gravity and Earth rotation.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import r3f

from src.ins.earth import somigliana
from src.ins.plotting import configure_axes, save_figure


OUTPUT_DIR = Path("results/figures/coarse_static_alignment_demo")
DATA_A = Path("data/fbbi_wbbi_A.bin")
DATA_B = Path("data/fbbi_wbbi_B.bin")


def load_static_imu_data(path):
    """Load stationary IMU data from a binary file."""
    data = np.fromfile(path).reshape((-1, 6)).T
    return data[0:3], data[3:6]


def coarse_static_align(fbbi_mean, wbbi_mean, hae):
    """
    Estimate roll, pitch, yaw, and latitude from stationary IMU measurements.

    Static alignment uses two physical references:

    - accelerometers measure gravity direction, which determines roll/pitch
    - gyroscopes measure Earth rotation, which determines yaw/latitude

    Parameters
    ----------
    fbbi_mean : ndarray, shape (3,)
        Mean body-frame specific force measurement.

    wbbi_mean : ndarray, shape (3,)
        Mean body-frame angular-rate measurement.

    hae : float
        Height above ellipsoid (m).

    Returns
    -------
    rpy : ndarray, shape (3,)
        Estimated roll, pitch, yaw angles (rad).

    lat : float
        Estimated geodetic latitude (rad).

    fbbi_pred : ndarray, shape (3,)
        Predicted accelerometer measurement from estimated alignment.

    wbbi_pred : ndarray, shape (3,)
        Predicted gyroscope measurement from estimated alignment.
    """

    # Roll and pitch are determined from the measured gravity direction.
    pitch = np.arctan(fbbi_mean[0] / np.sqrt(fbbi_mean[1]**2 + fbbi_mean[2]**2))
    roll = np.arctan2(-fbbi_mean[1], -fbbi_mean[2])

    cr = np.cos(roll)
    sr = np.sin(roll)
    cp = np.cos(pitch)
    sp = np.sin(pitch)

    # Yaw is determined by resolving the measured Earth-rate vector after
    # roll and pitch have aligned the vertical axis.
    a = wbbi_mean[1] * cr - wbbi_mean[2] * sr
    b = wbbi_mean[0] * cp + wbbi_mean[1] * sr * sp + wbbi_mean[2] * cr * sp
    yaw = np.arctan2(-a, b)

    rpy = np.array([roll, pitch, yaw])
    Cnb = r3f.rpy_to_dcm(rpy).T

    # Estimate latitude from the Earth-rate vector resolved in the
    # navigation frame.
    wnei_est = Cnb @ wbbi_mean
    lat = np.arctan(-wnei_est[2] / wnei_est[0])

    # Reconstruct the ideal measurements implied by the estimated alignment.
    gravity_mag = somigliana(lat, hae)
    gravity_nav = np.array([0.0, 0.0, gravity_mag])
    fbbi_pred = -Cnb.T @ gravity_nav

    earth_rate_nav = np.array([
        r3f.W_EI * np.cos(lat),
        0.0,
        -r3f.W_EI * np.sin(lat),
    ])
    wbbi_pred = Cnb.T @ earth_rate_nav

    return rpy, lat, fbbi_pred, wbbi_pred


def summarize_sensor(name, fbbi_t, wbbi_t, hae):
    """Compute mean measurements, alignment estimate, and predicted signals."""
    fbbi_mean = np.mean(fbbi_t, axis=1)
    wbbi_mean = np.mean(wbbi_t, axis=1)

    fbbi_std = np.std(fbbi_t, axis=1)
    wbbi_std = np.std(wbbi_t, axis=1)

    rpy, lat, fbbi_pred, wbbi_pred = coarse_static_align(
        fbbi_mean,
        wbbi_mean,
        hae,
    )

    return {
        "name": name,
        "fbbi_t": fbbi_t,
        "wbbi_t": wbbi_t,
        "fbbi_mean": fbbi_mean,
        "wbbi_mean": wbbi_mean,
        "fbbi_std": fbbi_std,
        "wbbi_std": wbbi_std,
        "rpy": rpy,
        "lat": lat,
        "fbbi_pred": fbbi_pred,
        "wbbi_pred": wbbi_pred,
    }


def print_alignment_summary(result):
    """Print a compact alignment summary."""
    name = result["name"]
    rpy_deg = result["rpy"] * 180 / np.pi
    lat_deg = result["lat"] * 180 / np.pi

    print(f"\nSensor {name}")
    print("-" * 40)
    print(f"Roll:     {result['rpy'][0]: .6f} rad  ({rpy_deg[0]: .3f} deg)")
    print(f"Pitch:    {result['rpy'][1]: .6f} rad  ({rpy_deg[1]: .3f} deg)")
    print(f"Yaw:      {result['rpy'][2]: .6f} rad  ({rpy_deg[2]: .3f} deg)")
    print(f"Latitude: {result['lat']: .6f} rad  ({lat_deg: .3f} deg)")
    print(f"Gyro std: {result['wbbi_std']} rad/s")


def plot_accel_residuals(result, dt):
    """Plot accelerometer residuals after static alignment."""
    t = np.arange(result["fbbi_t"].shape[1]) * dt
    residual = result["fbbi_t"] - result["fbbi_pred"].reshape((-1, 1))

    fig, ax = plt.subplots()
    ax.plot(t / 60, residual[0] * 1000, label="$x_b$")
    ax.plot(t / 60, residual[1] * 1000, label="$y_b$")
    ax.plot(t / 60, residual[2] * 1000, label="$z_b$")

    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Accelerometer Residual (mm/s$^2$)",
        title=f"Sensor {result['name']} Accelerometer Residuals",
    )
    ax.legend()
    return fig


def plot_gyro_residuals(result, dt):
    """Plot gyroscope residuals after static alignment."""
    t = np.arange(result["wbbi_t"].shape[1]) * dt
    residual = result["wbbi_t"] - result["wbbi_pred"].reshape((-1, 1))

    fig, ax = plt.subplots()
    ax.plot(t / 60, residual[0] * 1000, label="$x_b$")
    ax.plot(t / 60, residual[1] * 1000, label="$y_b$")
    ax.plot(t / 60, residual[2] * 1000, label="$z_b$")

    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Gyroscope Residual (mrad/s)",
        title=f"Sensor {result['name']} Gyroscope Residuals",
    )
    ax.legend()
    return fig


def run_demo():
    hae = -3.5

    fbbi_A_t, wbbi_A_t = load_static_imu_data(DATA_A)
    fbbi_B_t, wbbi_B_t = load_static_imu_data(DATA_B)

    result_A = summarize_sensor("A", fbbi_A_t, wbbi_A_t, hae)
    result_B = summarize_sensor("B", fbbi_B_t, wbbi_B_t, hae)

    print_alignment_summary(result_A)
    print_alignment_summary(result_B)

    for result, dt in [(result_A, 0.01), (result_B, 0.004)]:
        fig = plot_accel_residuals(result, dt)
        save_figure(fig, OUTPUT_DIR, f"sensor_{result['name'].lower()}_accel_residuals")
        plt.close(fig)

        fig = plot_gyro_residuals(result, dt)
        save_figure(fig, OUTPUT_DIR, f"sensor_{result['name'].lower()}_gyro_residuals")
        plt.close(fig)


if __name__ == "__main__":
    run_demo()