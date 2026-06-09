# Coarse Static Alignment from Gravity and Earth Rotation

## Overview

Before an inertial navigation system can begin propagating position, velocity, and attitude, it must first determine its initial orientation relative to the Earth.

This process is known as **static alignment**.

When a navigation-grade IMU is stationary, it measures two physical quantities:

1. **Gravity**, using the accelerometers.
2. **Earth rotation**, using the gyroscopes.

Together, these measurements are sufficient to estimate:

- Roll
- Pitch
- Yaw
- Latitude

without any external aiding source.

This experiment demonstrates a classical coarse-alignment procedure using two stationary IMUs mounted in unknown orientations.

---

# Objectives

The goals of this experiment are:

- Estimate roll and pitch from gravity measurements.
- Estimate yaw and latitude from Earth rotation measurements.
- Reconstruct the expected IMU measurements from the estimated alignment.
- Compare reconstructed measurements against recorded measurements.
- Evaluate the quality of two different IMU sensors.

---

# Background

## Why Alignment is Necessary

The mechanization equations developed in the previous examples assume that the navigation system already knows its initial attitude.

In practice, this is not true.

When an aircraft inertial navigation system is powered on, the system must determine:

```text
Body Frame
      ↓
Navigation Frame
```

before navigation can begin.

Without this alignment step, the mechanization equations cannot correctly interpret accelerometer and gyroscope measurements.

---

# Static Alignment Theory

## Determining Roll and Pitch

When the IMU is stationary, the accelerometers measure gravity.

The measured specific force vector points opposite the local gravity vector:

$\mathbf{f}^b \approx -\mathbf{g}^b$

Since gravity always points downward, the measured gravity direction uniquely determines:

- Roll
- Pitch

The alignment equations used in this experiment are:

```math
p = \tan^{-1}
\left(
\frac{f_x}
{\sqrt{f_y^2 + f_z^2}}
\right)
```

```math
r = \tan^{-1}
\left(
\frac{-f_y}
{-f_z}
\right)
```

where:

- $r$ is roll,
- $p$ is pitch.

---

## Determining Yaw

Once roll and pitch have been determined, the measured Earth-rate vector can be used to estimate yaw.

Earth rotates at approximately:

```math
\omega_E = 7.292115 \times 10^{-5}
\ \text{rad/s}
```

The gyroscopes measure this rotation in the body frame.

By resolving the Earth-rate vector into the navigation frame, the remaining unknown attitude angle is yaw.

This process is often referred to as:

**gyrocompassing**

---

## Determining Latitude

The Earth-rate vector in the navigation frame is:

```math
\boldsymbol{\omega}_{n,ei}
=
\begin{bmatrix}
\omega_E \cos(\phi) \\
0 \\
-\omega_E \sin(\phi)
\end{bmatrix}
```

where:

- $\phi$ is latitude.

After estimating the navigation-frame Earth-rate vector, latitude can be recovered from:

```math
\phi
=
\tan^{-1}
\left(
\frac{-\omega_z}
{\omega_x}
\right)
```

---

# Experiment Setup

Two stationary IMUs were placed on a table:

| Parameter | Value |
|------------|--------|
| Height Above Ellipsoid | -3.5 m |
| Duration | ~12 minutes |
| Sensor A Sample Rate | 100 Hz |
| Sensor B Sample Rate | 250 Hz |

The orientations of the two sensors were unknown.

The goal is to estimate the alignment of each sensor using only the recorded accelerometer and gyroscope measurements.

---

# Alignment Results

## Sensor A

Using the mean accelerometer and gyroscope measurements, the estimated alignment parameters are:

| Quantity | Value |
|-----------|-----------|
| Roll | *computed by demo* |
| Pitch | *computed by demo* |
| Yaw | *computed by demo* |
| Latitude | *computed by demo* |

### Interpretation

The accelerometer measurements provide a stable estimate of gravity direction, allowing roll and pitch to be determined accurately.

The gyroscope measurements then provide an estimate of the Earth-rate vector, allowing yaw and latitude to be recovered.

---

## Sensor B

Using the same alignment procedure:

| Quantity | Value |
|-----------|-----------|
| Roll | *computed by demo* |
| Pitch | *computed by demo* |
| Yaw | *computed by demo* |
| Latitude | *computed by demo* |

### Interpretation

Because Sensor B exhibits lower gyroscope noise, the Earth-rate measurement is more precise.

This generally produces more accurate estimates of yaw and latitude.

---

# Alignment Validation

After estimating the alignment, the expected accelerometer and gyroscope measurements can be reconstructed.

The reconstructed measurements are then compared against the recorded measurements.

Perfect alignment would produce zero residuals.

Any remaining residuals represent:

- Sensor noise
- Sensor bias
- Modeling errors

---

# Accelerometer Residuals

## Sensor A

![Sensor A Accelerometer Residuals](../results/figures/static_alignment_demo/sensor_a_accel_residuals.pdf)

### Observation

The residual accelerometer measurements remain centered around zero.

### Interpretation

This indicates that the estimated orientation correctly explains the measured gravity vector.

The remaining error is primarily sensor noise.

---

## Sensor B

![Sensor B Accelerometer Residuals](../results/figures/static_alignment_demo/sensor_b_accel_residuals.pdf)

### Observation

The residuals remain small and approximately zero-mean.

### Interpretation

The alignment solution accurately reconstructs the expected gravity measurements.

---

# Gyroscope Residuals

## Sensor A

![Sensor A Gyroscope Residuals](../results/figures/static_alignment_demo/sensor_a_gyro_residuals.pdf)

### Observation

The residual gyroscope measurements exhibit noticeable variability.

### Interpretation

Earth rotation is extremely small:

```math
\omega_E
=
7.292115\times10^{-5}
\ \text{rad/s}
```

As a result, gyroscope noise has a significant effect on the estimated Earth-rate vector.

---

## Sensor B

![Sensor B Gyroscope Residuals](../results/figures/static_alignment_demo/sensor_b_gyro_residuals.pdf)

### Observation

The residuals are visibly smaller than those of Sensor A.

### Interpretation

The lower gyroscope noise allows Sensor B to resolve Earth rotation more accurately.

This improves the estimation of:

- Yaw
- Latitude

and ultimately leads to a better alignment solution.

---

# Which Sensor is Better?

The accelerometers in both sensors are capable of measuring gravity with high accuracy.

The primary challenge in static alignment is measuring Earth rotation.

Earth rotation is approximately:

$15^\circ/\text{hour}$

which corresponds to only:

```math
7.29\times10^{-5}
\ \text{rad/s}
```

Successfully resolving such a small signal requires a low-noise gyroscope.

Because Sensor B exhibits lower gyroscope residuals and lower gyroscope noise, it is likely the more accurate sensor.

---

# Relationship to Navigation Systems

Static alignment is one of the first operations performed by a navigation-grade INS.

A typical workflow is:

```text
Power On
    ↓
Static Alignment
    ↓
Navigation Initialization
    ↓
Forward Mechanization
    ↓
External Aiding (GPS, etc.)
```

The quality of the initial alignment directly affects subsequent navigation performance.

Poor alignment can introduce:

- Position drift
- Velocity drift
- Attitude drift

through the same mechanisms explored in the Schuler oscillation experiment.

---

# Key Takeaways

- Gravity measurements provide roll and pitch information.
- Earth rotation measurements provide yaw and latitude information.
- Static alignment can be performed without GPS or any external aiding source.
- Gyrocompassing relies on accurately measuring the Earth's rotation rate.
- Navigation-grade gyroscopes are required for high-quality alignment.
- Sensor B demonstrates superior alignment performance due to its lower gyroscope noise.
- Static alignment is a critical initialization step for any inertial navigation system.

This experiment demonstrates how a stationary IMU can determine its orientation relative to the Earth using only fundamental physical references: gravity and Earth rotation.