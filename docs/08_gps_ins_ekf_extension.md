# Future Extension: GPS/INS Integration Using an Extended Kalman Filter

## Overview

The previous demonstrations in this repository explored the fundamental components of inertial navigation:

- Earth modeling
- Coordinate transformations
- IMU measurement generation
- Strapdown mechanization
- Static alignment
- Sensor error modeling
- Schuler oscillation

Together, these demonstrations illustrate how an inertial navigation system operates and how errors propagate through the navigation solution.

However, a fundamental limitation remains:

> An inertial navigation system is a dead-reckoning navigation system.

Even with perfect Earth models and sophisticated mechanization algorithms, small sensor errors eventually accumulate into significant navigation errors.

Modern navigation systems overcome this limitation by combining inertial navigation with external aiding sensors.

The most common example is the integration of GPS and INS using an Extended Kalman Filter (EKF).

This document outlines a proposed future extension to the repository that would demonstrate GPS/INS integration and sensor fusion.

---

# Motivation

## Why INS Alone Is Not Enough

The IMU Error Modeling and Schuler Oscillation demonstrations showed that inertial navigation errors inevitably grow with time.

Examples include:

- Accelerometer biases
- Gyroscope biases
- Alignment errors
- Sensor noise
- Schuler dynamics

These errors produce:

```text
Accelerometer Bias
        ↓
Velocity Error
        ↓
Position Error
```

and

```text
Gyroscope Bias
        ↓
Attitude Error
        ↓
Gravity Misprojection
        ↓
Acceleration Error
        ↓
Velocity Error
        ↓
Position Error
```

As a result, inertial navigation systems eventually drift away from the true trajectory.

---

## Why GPS Alone Is Not Enough

GPS provides absolute position measurements with bounded error.

However, GPS also has limitations:

- Low update rate
- Signal blockage
- Urban canyon effects
- Multipath
- Jamming
- Spoofing
- Satellite outages

GPS therefore cannot serve as a complete navigation solution in many operational environments.

---

## Why Combine Them?

GPS and INS possess complementary strengths.

| INS | GPS |
|------|------|
| High-rate updates | Low-rate updates |
| Autonomous | Requires satellite visibility |
| Continuous navigation | Absolute position measurements |
| Works during outages | Bounded long-term error |
| Drifts with time | Does not drift |

Combining the two systems allows:

- GPS to correct INS drift.
- INS to bridge GPS outages.
- Continuous navigation with bounded error.

This concept forms the foundation of most modern navigation systems.

---

# Proposed Navigation Architecture

The proposed GPS/INS architecture would combine the forward mechanization algorithm developed in this repository with GPS measurements using an Extended Kalman Filter.

```text
                Accelerometers
                      │
                      ▼
               Forward Mechanization
                      │
                      ▼
              INS State Estimate
                      │
                      ▼
             Extended Kalman Filter
                      ▲
                      │
               GPS Measurements
```

The mechanization would continue to operate at the IMU update rate while GPS measurements would periodically correct accumulated drift.

---

# Proposed State Vector

A simple implementation could estimate:

\[
\mathbf{x}
=
\begin{bmatrix}
p_n \\
p_e \\
p_d \\
v_n \\
v_e \\
v_d \\
\phi \\
\theta \\
\psi
\end{bmatrix}
\]

where:

- \(p_n,p_e,p_d\) represent position,
- \(v_n,v_e,v_d\) represent velocity,
- \(\phi,\theta,\psi\) represent roll, pitch, and yaw.

This state vector directly corresponds to the navigation quantities propagated by the forward mechanization algorithm.

---

# INS Propagation

The state would be propagated using the strapdown mechanization developed earlier in the repository.

The nonlinear propagation equation is:

\[
\mathbf{x}_{k+1}
=
f(\mathbf{x}_k,\mathbf{u}_k)
\]

where:

- \(\mathbf{x}_k\) is the navigation state,
- \(\mathbf{u}_k\) contains accelerometer and gyroscope measurements,
- \(f(\cdot)\) represents the forward mechanization algorithm.

The mechanization would continue operating at the IMU update rate regardless of GPS availability.

---

# GPS Measurement Model

GPS would provide position measurements of the form:

\[
\mathbf{z}
=
\begin{bmatrix}
p_n \\
p_e \\
p_d
\end{bmatrix}
+
\mathbf{v}
\]

where:

- \(\mathbf{z}\) is the GPS measurement,
- \(\mathbf{v}\) represents measurement noise.

The corresponding measurement function would be:

\[
\mathbf{z}
=
h(\mathbf{x})
+
\mathbf{v}
\]

with

\[
h(\mathbf{x})
=
\begin{bmatrix}
p_n \\
p_e \\
p_d
\end{bmatrix}
\]

---

# Extended Kalman Filter

Because inertial navigation dynamics are nonlinear, a classical Kalman Filter is insufficient.

An Extended Kalman Filter linearizes the nonlinear system about the current state estimate and performs recursive state estimation.

The proposed implementation would include:

## Prediction

\[
P_{k+1}
=
F_k P_k F_k^T
+
Q_k
\]

where:

- \(P\) is the state covariance matrix,
- \(F\) is the linearized state-transition matrix,
- \(Q\) represents process noise.

The process noise would incorporate the IMU error models developed in the IMU Error Modeling demonstration.

---

## Measurement Update

### Innovation Covariance

\[
S
=
H P H^T
+
R
\]

### Kalman Gain

\[
K
=
P H^T S^{-1}
\]

### State Correction

\[
\hat{x}
=
\hat{x}
+
K r
\]

where

\[
r
=
z
-
h(\hat{x})
\]

is the measurement residual.

### Covariance Update

\[
P
=
P
-
K H P
\]

These equations determine how much trust should be placed in:

- the INS prediction,
- the GPS measurement.

---

# Proposed Simulation Environment

The GPS/INS demonstration would build directly upon the existing figure-eight aircraft simulation used throughout the repository.

The simulation would include:

## Truth Trajectory

- Figure-eight aircraft path
- Translational motion
- Rotational motion
- Altitude variation

## IMU Measurements

- Accelerometer measurements
- Gyroscope measurements
- Realistic sensor noise
- Bias-like error sources

generated using the stochastic IMU models developed earlier.

## GPS Measurements

Synthetic GPS position measurements generated from the truth trajectory and corrupted with Gaussian noise.

Example update rates:

| Sensor | Update Rate |
|----------|----------|
| IMU | 100 Hz |
| GPS | 1 Hz |

---

# Expected Results

## Pure INS Navigation

Based on the IMU Error Modeling and Schuler Oscillation demonstrations, a standalone INS is expected to exhibit:

- Continuously growing position error
- Increasing attitude uncertainty
- Long-term drift

A trajectory comparison would likely show increasing divergence from the truth trajectory.

---

## GPS-Aided INS Navigation

The addition of GPS measurements is expected to:

- Bound position error
- Reduce long-term drift
- Improve navigation accuracy

The resulting trajectory should remain much closer to the truth solution.

---

## Performance Metrics

Potential evaluation metrics include:

- Position RMSE
- Velocity RMSE
- Maximum position error
- Mean position error
- Final position error

Comparison tables could quantify the improvement provided by GPS aiding.

---

# GPS Outage Experiment

One particularly interesting extension would be a simulated GPS-denied interval.

For example:

```text
0–120 s     GPS Available
120–240 s   GPS Denied
240–360 s   GPS Available
```

Expected behavior:

### During Outage

- Navigation remains available.
- Position error gradually increases.
- INS propagation continues uninterrupted.

### After GPS Recovery

- GPS measurements become available again.
- The EKF corrects accumulated drift.
- Navigation accuracy improves rapidly.

This experiment would clearly demonstrate why inertial navigation systems remain valuable even in environments where GPS is available.

---

# Relationship to Previous Demonstrations

This proposed extension represents the natural culmination of the concepts developed throughout the repository.

```text
Ellipsoidal Earth
        ↓
Kinematics
        ↓
Inverse Mechanization
        ↓
Forward Mechanization
        ↓
Coarse Static Alignment
        ↓
IMU Error Modeling
        ↓
Schuler Oscillation
        ↓
GPS/INS Integration
```

Each demonstration contributes a foundational concept required to understand modern navigation systems.

---

# Future Directions

Beyond a basic GPS/INS EKF implementation, several additional extensions could be explored:

## Error-State Kalman Filtering

Estimate navigation errors rather than full navigation states.

This approach is commonly used in operational navigation systems.

---

## Unscented Kalman Filters

Replace linearization with sigma-point propagation to better handle nonlinear dynamics.

---

## Additional Navigation Sensors

Integrate:

- Barometers
- Magnetometers
- Wheel odometry
- Visual odometry
- Lidar measurements

into the navigation solution.

---

## Multi-Sensor Navigation Architectures

Explore advanced sensor-fusion techniques for autonomous systems operating in GPS-denied environments.

---

# Key Takeaways

- Inertial navigation systems provide continuous navigation but drift with time.
- GPS provides bounded position measurements but suffers from outages and low update rates.
- Combining GPS and INS produces a navigation solution that is more accurate and more robust than either sensor alone.
- The Extended Kalman Filter is one of the most common methods for performing GPS/INS sensor fusion.
- The mechanization, alignment, and error-analysis concepts developed throughout this repository naturally lead to GPS/INS integration.
- Implementing a GPS/INS EKF would be a logical next step and a valuable future extension of this project.

While not currently implemented, this extension represents the next stage in the progression from standalone inertial navigation toward complete multi-sensor navigation systems.