# Ellipsoidal Earth and Local Navigation Frames

## Overview

This experiment investigates how large-scale aircraft motion behaves when represented in multiple Earth-referenced coordinate systems. The goal is to build intuition for:

* geodetic coordinates,
* local tangent frames,
* curvilinear coordinates,
* Earth curvature effects,
* and gravity variation over an ellipsoidal Earth.

The simulation considers an aircraft following a large circular trajectory near Bel Air, Maryland while comparing how the same motion appears in different navigation frames.

---

# Experiment Setup

## Initial Conditions

The aircraft begins at:

* Latitude: 39.535°
* Longitude: -76.348°
* Height Above Ellipsoid: 212 m

The aircraft then follows a counterclockwise circular trajectory defined in a local curvilinear frame.

## Curvilinear Trajectory

The path is parameterized by:

\[
\begin{aligned}
x_c &= R(1 + \cos\theta) \
y_c &= R\sin\theta \
z_c &= -\left(\cos\theta + 1\right)\frac{\Delta h}{2}
\end{aligned}
\]

where:
\[
* (R = 1000\ \text{km})
* (\Delta h = 1\ \text{km})
* (\theta \in [\pi, -\pi])
\]

The trajectory spans a sufficiently large region that Earth curvature effects become visible.

---

# Coordinate Frames

This experiment compares several commonly used navigation frames.

## Curvilinear Frame

The curvilinear frame follows the local curvature of the Earth. Distances are measured along the curved Earth surface.

## Tangent Frame

The tangent frame is a locally flat approximation defined at the starting location.

For small trajectories, tangent and curvilinear frames appear nearly identical. Over large distances, however, the flat-Earth approximation begins to distort the geometry.

## Navigation Frame

The navigation frame rotates with the vehicle's geodetic position as it moves over the Earth.

## Earth-Centered Earth-Fixed (ECEF) Frame

The ECEF frame is a global Cartesian frame fixed to the rotating Earth.

---

# Results and Discussion

## 1. Curvilinear vs Tangent-Frame Trajectory

The first plot compares the aircraft trajectory in the local curvilinear frame and the local tangent frame.

![Curvilinear vs Tangent](../results/figures/ellipsoidal_earth_demo/curvilinear_vs_tangent.pdf)

### Observation

The trajectories differ because the tangent frame assumes a locally flat Earth, while the curvilinear frame follows the Earth's curvature.

For short trajectories, this difference is negligible. Over a 1000 km trajectory, however, Earth curvature becomes significant and the tangent-frame representation distorts the geometry.

This illustrates one of the fundamental limitations of flat-Earth approximations in long-range navigation.

---

## 2. Curvilinear Vertical Coordinate vs Height Above Ellipsoid

The next figure compares:

* the curvilinear vertical coordinate (z_c), and
* the geodetic height above the ellipsoid.

![zc vs Height](../results/figures/ellipsoidal_earth_demo/zc_vs_height.pdf)

### Observation

The curvilinear frame defines positive vertical motion downward, while geodetic height is measured upward from the ellipsoid.

Returning to (z_c = 0) simply means the aircraft returned to the original local vertical reference.

This does not imply that all Earth-referenced vertical quantities evolve identically along the trajectory.

---

## 3. Runway Position Relative to the Aircraft

Instead of plotting the aircraft trajectory itself, this experiment plots the apparent position of the starting runway from the perspective of the moving aircraft.

![Runway Relative Motion](../results/figures/ellipsoidal_earth_demo/runway_relative_motion.pdf)

### Observation

As the aircraft moves along its circular trajectory, the runway appears to move opposite the aircraft motion.

The apparent southward displacement occurs because:

* the navigation frame rotates with the vehicle,
* the Earth is curved,
* and the local-level frame changes continuously along the trajectory.

This demonstrates that local navigation frames are not globally inertial.

---

## 4. Tangent-Frame Vertical Position vs Navigation-Frame Vertical Position

The next figure compares:

* the aircraft vertical position in the tangent frame, and
* the apparent vertical position of the runway in the navigation frame.

![Vertical Comparison](../results/figures/ellipsoidal_earth_demo/vertical_frame_comparison.pdf)

### Observation

These quantities differ because:

* the tangent frame remains fixed at the initial location,
* the navigation frame rotates with the aircraft,
* and the Earth surface falls away from the initial tangent plane.

This effect becomes increasingly noticeable as the trajectory length increases.

---

## 5. Somigliana Gravity Variation

The final experiment evaluates gravity magnitude using the Somigliana gravity model.

![Somigliana Gravity](../results/figures/ellipsoidal_earth_demo/somigliana_gravity.pdf)

### Observation

Gravity varies along the trajectory due to:

* latitude changes,
* Earth oblateness,
* and altitude variation.

Although the aircraft climbs during portions of the trajectory, gravity does not necessarily decrease monotonically.

Latitude dependence can dominate the relatively small altitude variation.

---

## Supplemental Visualization: Distance to Earth Center

The following figure illustrates why gravity can increase even while height above the ellipsoid increases.

![Distance to Earth Center](../results/figures/ellipsoidal_earth_demo/distance_to_earth_center.pdf)

### Observation

The ellipsoidal Earth shape causes the distance to the Earth's center to vary differently than the height above the reference ellipsoid.

This demonstrates why gravity modeling requires both:

* altitude dependence, and
* latitude dependence.

---

# Key Takeaways

* Local tangent frames are approximations that become inaccurate over sufficiently large distances.
* Navigation frames rotate relative to inertial space as a vehicle moves over the Earth.
* Curvilinear and tangent-frame coordinates diverge due to Earth curvature.
* Gravity depends on both latitude and altitude.
* Accurate inertial navigation requires careful treatment of Earth geometry and reference frames.

These concepts form the foundation for later experiments involving:

* inertial mechanization,
* sensor error propagation,
* Schuler oscillation,
* static alignment,
* and GPS/INS integration.
