# Rotating Frames and Navigation Kinematics

## Overview

This experiment investigates how position and velocity behave when represented in multiple rotating and inertial coordinate systems.

The simulation models an aircraft flying northward from the equator to the North Pole while comparing:

* Earth-Centered Inertial (ECI) coordinates,
* Earth-Centered Earth-Fixed (ECEF) coordinates,
* and local navigation-frame quantities.

The primary goal is to build intuition for:

* rotating reference frames,
* inertial versus Earth-fixed motion,
* frame-relative velocity definitions,
* and how navigation quantities depend on the coordinate system in which they are expressed.

These concepts form the foundation for later inertial navigation mechanization equations.

---

# Experiment Setup

## Flight Definition

The aircraft follows a simple northward trajectory:

[
\phi_d = \frac{\pi}{2}\left(\frac{t}{t_{dur}}\right)
]

where:

* (\phi_d) is geodetic latitude,
* (t_{dur} = 12\ \text{hours}),
* longitude is fixed at zero,
* and altitude remains constant at 1 km above the ellipsoid.

The simulation uses:

* a sampling period of 10 minutes,
* and assumes the ECI and ECEF frames align at (t = 0).

---

# Coordinate Frames

## Earth-Centered Inertial (ECI)

The ECI frame is approximately inertial and does not rotate with the Earth.

Objects fixed to the Earth therefore appear to rotate within this frame.

---

## Earth-Centered Earth-Fixed (ECEF)

The ECEF frame rotates with the Earth.

Positions fixed to the Earth remain stationary in ECEF coordinates.

---

## Navigation Frame

The navigation frame is a local-level frame attached to the aircraft geodetic position.

As the aircraft moves over the Earth, the navigation frame rotates relative to both ECI and ECEF frames.

---

# Velocity Definitions

Several velocity quantities are evaluated in this experiment.

## Inertial-Relative Velocity

[
\mathbf{v}_{ei}
]

represents the velocity of the Earth-fixed frame relative to the inertial frame.

---

## Earth-Relative Velocity

[
\mathbf{v}_{e}
]

represents the velocity obtained by differentiating ECEF position directly in the ECEF frame.

---

## Navigation-Frame Velocities

The experiment also compares navigation-frame representations of these velocities.

This demonstrates that:

* velocity depends on the frame in which the derivative is taken,
* and rotating a velocity vector into another frame is not equivalent to differentiating position within that frame.

---

# Results and Discussion

## 1. ECI Position and Inertial Velocity

The first figure shows:

* aircraft position in the ECI frame,
* and inertial velocity vectors plotted along the trajectory.

![ECI Position and Velocity](../results/figures/kinematics_demo/inertial_position_velocity.pdf)

### Observation

The trajectory forms a counterclockwise corkscrew pattern because the Earth rotates beneath the inertial frame.

Although the aircraft flies northward relative to the Earth, the Earth itself rotates eastward within the inertial frame.

The inertial velocity gradually decreases during the flight because the rotational contribution from Earth spin decreases as the aircraft approaches the North Pole.

Near the equator, the Earth's rotation contributes significantly to inertial velocity magnitude. Near the poles, this contribution approaches zero.

---

## 2. ECEF Position and Inertial-Relative Velocity

The next figure shows:

* aircraft position in the ECEF frame,
* and the inertial-relative velocity expressed in ECEF coordinates.

![ECEF Position and Inertial Velocity](../results/figures/kinematics_demo/ecef_position_inertial_velocity.pdf)

### Observation

The velocity vectors are not tangent to the ECEF position path.

This occurs because:

* the velocity was computed as the time derivative of inertial position,
* then rotated into the ECEF frame.

This produces the inertial-relative velocity expressed in ECEF coordinates.

Importantly:

> Rotating a velocity vector into another frame is not equivalent to differentiating position within that frame.

The final velocity direction differs significantly from the ECI-frame visualization because the Earth rotates by approximately 180 degrees during the 12-hour flight.

The ECEF axes rotate with the Earth, while the inertial frame remains fixed.

---

## 3. Velocity Magnitude Comparison: Inertial-Relative Velocities

The following figure compares the magnitudes of:

* (v_i),
* (v_{ei}),
* and (v_{ni}).

![Inertial Relative Velocity Magnitudes](../results/figures/kinematics_demo/inertial_relative_velocity_norms.pdf)

### Observation

These velocities have identical magnitudes because they represent the same physical velocity expressed in different coordinate frames.

Frame rotations change the vector components but do not change vector magnitude.

The gradual decrease in velocity magnitude occurs because Earth rotation contributes less inertial speed as latitude increases.

---

## 4. Velocity Magnitude Comparison: Earth-Relative Velocities

The next figure compares the magnitudes of:

* (v_e),
* (v_{ie}),
* and (v_{ne}).

![Earth Relative Velocity Magnitudes](../results/figures/kinematics_demo/earth_relative_velocity_norms.pdf)

### Observation

These velocities gradually increase throughout the flight.

Although latitude changes linearly with time, the Earth is ellipsoidal rather than spherical.

As the aircraft approaches the poles, the same latitude increment corresponds to a different physical displacement relative to the Earth surface.

This produces increasing Earth-relative velocity magnitude.

---

## 5. Local Gravity Variation

The final figure shows local gravity magnitude along the trajectory using the Somigliana gravity model.

![Gravity Variation](../results/figures/kinematics_demo/gravity_vs_time.pdf)

### Observation

Local gravity increases as the aircraft approaches the poles.

This occurs because:

* the Earth is oblate,
* the polar radius is smaller than the equatorial radius,
* and centrifugal effects from Earth rotation decrease near the poles.

As a result, the aircraft moves closer to the Earth's center while also experiencing reduced outward centrifugal acceleration.

---

# Key Takeaways

* Velocity depends on the frame in which the derivative is taken.
* Rotating a velocity vector into another frame is not equivalent to differentiating position within that frame.
* ECI and ECEF frames produce fundamentally different interpretations of motion.
* Earth rotation strongly affects inertial-frame trajectories.
* Navigation-frame quantities evolve as local-level frames rotate over the Earth.
* Gravity magnitude varies with latitude due to Earth oblateness and rotation.

These concepts are foundational for:

* inertial navigation mechanization,
* Coriolis effects,
* transport rates,
* Earth-rate compensation,
* and Schuler dynamics.
