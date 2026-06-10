# Strapdown Inertial Navigation: Models, Mechanization, and Error Dynamics

> A first-principles exploration of inertial navigation, state estimation, and navigation system design through simulation, implementation, and analysis of the core algorithms used in modern navigation systems.

---

## Overview

Modern navigation systems are often treated as black boxes.

GPS receivers provide position estimates, inertial navigation systems provide continuous navigation, and Kalman filters combine multiple sensors into a unified solution. While these tools are widely used, the underlying mathematics and physical principles are frequently hidden behind software libraries and commercial products.

This repository was created to develop a first-principles understanding of inertial navigation through a series of progressively more sophisticated simulations and experiments.

The project began as a self-study of inertial navigation and state estimation while working in the Positioning, Navigation, and Timing (PNT) field. Rather than treating navigation as a collection of disconnected equations, the goal was to build a complete conceptual foundation beginning with Earth modeling and ending with the error dynamics that govern real-world inertial navigation systems.

The repository is intentionally educational in nature.

The objective is **not** to develop a production-grade navigation system, but rather to implement and explore the core concepts underlying modern GPS/INS navigation architectures.

---

## Learning Objectives

The primary goals of this repository are:

- Develop intuition for inertial navigation systems from first principles.
- Understand how IMU measurements relate to vehicle motion.
- Implement strapdown inertial navigation algorithms.
- Explore the effects of sensor noise and bias.
- Investigate Earth-referenced navigation dynamics.
- Study how navigation errors evolve over time.
- Build a foundation for future work in sensor fusion and state estimation.

---

## Topics Covered

| Topic | Description |
|---------|---------|
| Ellipsoidal Earth | WGS-84 Earth model, curvature, and gravity calculations |
| Kinematics | Coordinate systems, attitude representations, and frame transformations |
| Inverse Mechanization | Generating ideal IMU measurements from a known trajectory |
| Forward Mechanization | Strapdown inertial navigation using accelerometer and gyroscope measurements |
| Static Alignment | Estimating attitude and latitude from gravity and Earth rotation |
| IMU Error Modeling | Allan variance and stochastic sensor noise models |
| Schuler Oscillation | Earth-referenced INS error dynamics and navigation drift |
| GPS/INS Integration | Proposed future extension using an Extended Kalman Filter |

---

# Repository Structure

```text
.
├── docs/
│   ├── 01_ellipsoidal_earth.md
│   ├── 02_kinematics.md
│   ├── 03_inverse_mechanization.md
│   ├── 04_forward_mechanization.md
│   ├── 05_static_alignment.md
│   ├── 06_imu_error_modeling.md
│   ├── 07_schuler_oscillation.md
│   └── 08_future_gps_ins_ekf.md
│
├── examples/
│   ├── coarse_static_alignment_demo.py
│   ├── ellipsoidal_earth_demo.py
│   ├── forward_mechanization_demo.py
│   ├── inverse_mechanization_demo.py 
│   ├── kinematics_demo.py
│   ├── noisy_imu_demo.py
│   └── schuler_oscillation_demo.py
│
├── src/
│   ├── earth.py
│   ├── mechanization.py
│   ├── noise.py 
│   ├── plotting.py
│   ├── rotations.py
│   └── trajectories.py
│
├── results/
│   ├── figures/
│
└── README.md
```

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/ehstevo/strapdown-inertial-navigation.git
cd strapdown-inertial-navigation
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run an Example

The repository is organized around standalone demonstrations.

For example:

```bash
python -m examples.ellipsoidal_earth_demo
```

```bash
python -m examples.forward_mechanization_demo
```

```bash
python -m examples.noisy_imu_demo
```

```bash
python -m examples.schuler_oscillation_demo
```

Generated figures will be saved to:

```text
results/figures/
```

---

## Recommended Demonstrations

For readers interested primarily in inertial navigation and estimation:

1. Forward Mechanization
2. IMU Error Modeling
3. Schuler Oscillation
4. Static Alignment

These demonstrations contain the majority of the navigation-specific concepts developed throughout the project.

---

# Demonstration Progression

The demonstrations are intentionally ordered so that each experiment builds upon concepts introduced previously.

```text
Ellipsoidal Earth
        ↓
Kinematics
        ↓
Inverse Mechanization
        ↓
Forward Mechanization
        ↓
Static Alignment
        ↓
IMU Error Modeling
        ↓
Schuler Oscillation
        ↓
GPS/INS Integration (Future Work)
```

The repository can therefore be viewed as a guided progression from fundamental Earth models to complete navigation systems.

---

# Featured Demonstrations

## Forward Mechanization

The Forward Mechanization demonstration implements a complete strapdown inertial navigation algorithm.

Given accelerometer and gyroscope measurements, the algorithm estimates:

- Position
- Velocity
- Attitude

while accounting for:

- Earth rotation
- Earth curvature
- Transport rate
- Somigliana gravity

This demonstration forms the core of the repository and serves as the foundation for the later error-analysis experiments.

---

## IMU Error Modeling

Real inertial sensors contain numerous stochastic error sources.

This demonstration explores:

- Quantization noise
- White noise
- First-order Gauss-Markov processes
- Bias instability
- Rate random walk

using both simulation and Allan variance analysis.

The resulting models provide realistic sensor errors for subsequent navigation experiments.

---

## Schuler Oscillation

One of the defining characteristics of Earth-referenced inertial navigation systems is the presence of Schuler oscillation.

This demonstration investigates how:

- Accelerometer biases
- Gyroscope biases
- Position errors
- Velocity errors
- Attitude errors

propagate through the navigation equations.

The experiment provides intuition for long-term navigation error dynamics and highlights the importance of accurate attitude estimation.

---

# Key Results

The repository implements and demonstrates:

- WGS-84 Earth modeling and gravity calculations.
- Navigation-frame and body-frame coordinate transformations.
- Inverse mechanization for generating synthetic IMU measurements.
- Strapdown inertial navigation using forward mechanization.
- Coarse static alignment using gravity and Earth rotation.
- IMU stochastic error modeling and Allan variance analysis.
- Schuler oscillation and Earth-referenced navigation dynamics.
- Modular navigation utilities for Earth models, rotations, trajectories, mechanization, and sensor noise.

Together, these demonstrations provide a practical introduction to the foundations of inertial navigation.

---

# Recommended Reading Path

For readers primarily interested in navigation algorithms and estimation, the following order is recommended:

1. Forward Mechanization
2. IMU Error Modeling
3. Schuler Oscillation
4. Static Alignment

These demonstrations contain the majority of the navigation-specific concepts and provide the strongest intuition for how real-world inertial navigation systems operate.

For readers seeking a complete progression from first principles, begin with Ellipsoidal Earth and proceed sequentially through the repository.

---

# Future Work

The next logical extension of this repository is GPS/INS sensor fusion using an Extended Kalman Filter.

Potential future additions include:

- GPS/INS EKF implementation
- Error-state Kalman filtering
- Unscented Kalman Filters
- GPS outage analysis
- Additional aiding sensors
  - Barometers
  - Magnetometers
  - Wheel odometry
  - Visual odometry
- Multi-sensor navigation architectures

A design document outlining the proposed GPS/INS extension is included in:

```text
docs/08_future_gps_ins_ekf.md
```

---


# Disclaimer

This repository is intended for educational and research purposes.

The implementations prioritize clarity, transparency, and conceptual understanding over computational efficiency or production readiness.

The goal is to provide a first-principles exploration of inertial navigation rather than a flight-certified navigation solution.

---

## Author

Alex Stevenson

Computer Scientist | Positioning, Navigation, and Timing (PNT)

Areas of Interest:

- State Estimation
- Inertial Navigation
- Sensor Fusion
- Autonomous Systems
- Aerospace Navigation
- Machine Learning for Navigation
