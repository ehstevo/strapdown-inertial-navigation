# Inverse Mechanization: Generating Synthetic IMU Measurements

## Overview

This experiment demonstrates inverse inertial navigation mechanization.

Rather than estimating trajectory from IMU measurements, the process is reversed:

* a truth trajectory is prescribed,
* the aircraft attitude is defined along the trajectory,
* and the ideal accelerometer and gyroscope measurements required to produce that motion are computed.

This allows controlled generation of synthetic IMU data for later use in:

* forward mechanization,
* sensor-noise experiments,
* Schuler oscillation studies,
* and GPS/INS integration.

The experiment models a drone flying a figure-eight trajectory near Bel Air, Maryland.

---

# Experiment Setup

## Initial Conditions

The aircraft begins at:

* Latitude: 39.535°
* Longitude: -76.348°
* Height Above Ellipsoid: 212 m

The simulation duration is:

* 6 minutes
* with a sampling period of 0.1 seconds.

---

# Figure-Eight Trajectory

The aircraft trajectory is defined in a local curvilinear frame centered at the origin.

```math
\begin{aligned}
x_c &= \frac{R}{4}\sin(2\theta) \
y_c &= R(\cos\theta - 1) \
z_c &= \frac{\Delta h}{2}(\cos\theta - 1)
\end{aligned}
```

where:

* $R = 1000\ \text{m}$
* $\Delta h = 100\ \text{m}$
* $\theta \in [0, 2\pi]$

This trajectory creates:

* lateral turning motion,
* altitude variation,
* and continuously changing heading.

The resulting path resembles a smooth airborne figure-eight maneuver.

---

# Aircraft Attitude Profile

The aircraft attitude is prescribed using roll, pitch, and yaw angles.

## Roll

$\phi = -\frac{1}{27}\cos(\theta)$

---

## Pitch

$\theta_p = -\frac{1}{48}\sin(2\theta) + \frac{1}{143}\sin(4\theta)$

---

## Yaw

$\psi = \arctan2\left(-2\sin(\theta), \cos(2\theta)\right)$

The attitude profile is intentionally smooth so that:

* the resulting IMU signals remain physically realistic,
* and the generated body dynamics resemble a maneuvering aircraft.

---

# Inverse Mechanization

## Objective

Inverse mechanization computes the IMU measurements that would produce the prescribed trajectory.

Specifically, the experiment generates:

* body-frame specific force measurements,
* body-frame angular-rate measurements,
* and navigation-frame velocity.

These quantities correspond to what ideal accelerometers and gyroscopes would measure during the flight.

---

# Coordinate Transformations

The local curvilinear trajectory is first transformed into geodetic coordinates:

$(x_c, y_c, z_c) \rightarrow (\phi, \lambda, h)$

The geodetic trajectory is then used to compute:

* transport rates,
* Earth rotation terms,
* navigation-frame velocity,
* and gravity.

Aircraft attitude is represented using body-to-navigation direction cosine matrices (DCMs).

---

# Gyroscope Signal Generation

The gyroscope measurements are generated using the inverse gyroscope equation.

The body angular rate relative to inertial space is:

$\omega_{b,bi}$

which includes contributions from:

* body rotation relative to the navigation frame,
* navigation-frame transport rate,
* and Earth rotation.

The incremental attitude change between time steps is computed using:

$S = C_{nb}^T C_{nb}^+$

where:

* $C_{nb}$ is the current body-to-navigation DCM,
* and $C_{nb}^+$ is the next-step DCM.

The incremental rotation matrix is then converted into an angular-rate vector.

---

# Navigation-Frame Velocity

Navigation-frame velocity is reconstructed from the geodetic trajectory.

The velocity components are:

$\mathbf{v}_{ne}$

expressed in the local navigation frame.

Earth curvature terms are required because:

* latitude and longitude are angular coordinates,
* and linear velocity depends on local Earth radii of curvature.

The meridian and transverse radii of curvature are therefore computed at each time step.

---

# Accelerometer Signal Generation

Accelerometer measurements are generated using the inverse navigation equation.

The body-frame specific force is computed from:

* navigation-frame acceleration,
* Coriolis effects,
* transport-rate effects,
* and gravity.

The resulting quantity corresponds to the specific force measured by ideal accelerometers.

Importantly:

> Accelerometers do not measure gravity directly.

Instead, they measure:

$\text{specific force} = \text{kinematic acceleration} - \text{gravity}$

This distinction is fundamental to inertial navigation.

---

# Results and Discussion

## 1. Geodetic Aircraft Trajectory

The first figure shows aircraft latitude versus longitude.

![Geodetic Trajectory](../results/figures/inverse_mechanization_demo/geodetic_trajectory.pdf)

### Observation

The aircraft follows a smooth figure-eight trajectory centered near the initial geodetic location.

Although the maneuver spans only a few kilometers, the trajectory is still represented using full geodetic coordinates.

---

## 2. Height Above Ellipsoid

The next figure shows height above the ellipsoid versus time.

![Altitude Profile](../results/figures/inverse_mechanization_demo/altitude_profile.pdf)

### Observation

The altitude profile varies smoothly throughout the maneuver.

This produces corresponding changes in:

* gravity,
* vertical velocity,
* and accelerometer measurements.

---

## 3. Aircraft Attitude Profile

The following figure shows aircraft roll, pitch, and yaw over time.

![Attitude Profile](../results/figures/inverse_mechanization_demo/attitude_profile.pdf)

### Observation

The aircraft attitude evolves continuously throughout the maneuver.

The yaw angle follows the changing direction of motion along the figure-eight path, while roll and pitch remain relatively small.

This creates a physically plausible aircraft motion profile.

---

## 4. Specific Force Measurements

The next figure shows the generated body-frame accelerometer measurements.

![Specific Force](../results/figures/inverse_mechanization_demo/specific_force.pdf)

### Observation

The accelerometer outputs reflect:

* translational acceleration,
* rotational motion,
* gravity compensation,
* and frame-rotation effects.

The vertical accelerometer channel is dominated by gravity, while the horizontal channels capture maneuver-induced acceleration.

---

## 5. Angular-Rate Measurements

The following figure shows the generated body-frame gyroscope measurements.

![Angular Rate](../results/figures/inverse_mechanization_demo/angular_rate.pdf)

### Observation

The gyroscope outputs reflect:

* aircraft rotational motion,
* Earth rotation,
* and navigation-frame transport rates.

These signals represent the angular rates an ideal body-mounted IMU would measure during the maneuver.

---

## 6. Navigation-Frame Velocity

The final figure shows the reconstructed navigation-frame velocity.

![Navigation Velocity](../results/figures/inverse_mechanization_demo/navigation_velocity.pdf)

### Observation

The navigation-frame velocity evolves continuously throughout the maneuver.

The velocity profile reflects:

* curved flight geometry,
* changing heading,
* and altitude variation.

These velocities later serve as reference quantities for forward mechanization validation.

---

# Binary Data Output

The generated IMU and velocity data are saved to a binary file for later experiments.

Each row contains:

```math
[f_{b,bi,x}, f_{b,bi,y}, f_{b,bi,z},
\omega_{b,bi,x}, \omega_{b,bi,y}, \omega_{b,bi,z},
v_{ne,x}, v_{ne,y}, v_{ne,z}]
```

This synthetic dataset is later reused for:

* forward mechanization,
* noisy sensor experiments,
* and INS error studies.

---

# Key Takeaways

* Inverse mechanization generates synthetic IMU measurements from known truth trajectories.
* Gyroscope measurements include both body rotation and navigation-frame rotation effects.
* Accelerometers measure specific force rather than gravity directly.
* Earth rotation and transport rates contribute to realistic IMU signals.
* Earth curvature terms are required to reconstruct navigation-frame velocity from geodetic motion.
* Synthetic IMU generation enables controlled validation of forward navigation algorithms.

This experiment forms the foundation for subsequent studies involving:

* forward mechanization,
* noisy sensors,
* Schuler oscillation,
* and GPS/INS integration.
