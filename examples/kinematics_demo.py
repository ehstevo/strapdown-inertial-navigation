import numpy as np
import matplotlib.pyplot as plt
import r3f

from src.ins.earth import somigliana
from src.ins.plotting import configure_axes, save_figure

"""
Rotating Frames and Navigation Kinematics Demonstration

This example investigates how aircraft position and velocity behave when
represented in multiple rotating and inertial coordinate systems.

The simulation models an aircraft flying northward from the equator to
the North Pole while comparing motion in:

- Earth-Centered Inertial (ECI) coordinates,
- Earth-Centered Earth-Fixed (ECEF) coordinates,
- and local navigation-frame coordinates.

The demo illustrates several foundational inertial navigation concepts:

- Earth rotation effects,
- rotating versus inertial reference frames,
- frame-dependent velocity definitions,
- and the distinction between:
    - differentiating position in a frame,
    - versus rotating a derivative into a frame.

The resulting visualizations help build intuition for the kinematic
relationships used later in inertial navigation mechanization equations.
"""

def plot_inertial_position_velocity(p_i, v_i):
    fig, ax = plt.subplots()
    ax.plot(p_i[0], p_i[1], color='green', linewidth=5.0, label='$p_i$')
    ax.quiver(
        p_i[0,:-1], p_i[1,:-1],
        v_i[0], v_i[1],
        scale=200.0,
        scale_units='inches',
        width=0.002,
        headwidth=0.002,
        color='blue',
        label='$v_i$'
    )
    configure_axes(
        ax,
        xlabel="$x_i$-axis (m)",
        ylabel="$y_i$-axis (m)",
        title="ECI Position and Inertial Velocity"
    )
    ax.legend()
    return fig


def plot_ecef_inertial_position_velocity(p_e, v_ei):
    fig, ax = plt.subplots()
    ax.plot(p_e[0], p_e[1], color='green', linewidth=5.0, label='$p_e$')
    ax.quiver(
        p_e[0,:-1], p_e[1,:-1],
        v_ei[0], v_ei[1],
        scale=200.0,
        scale_units='inches',
        width=0.002,
        headwidth=0.002,
        color='blue',
        label='$v_{ei}$'
    )
    configure_axes(
        ax,
        xlabel="$x_e$-axis (m)",
        ylabel="$y_e$-axis (m)",
        title="ECEF Position and Inertial-Relative Velocity"
    )
    ax.legend()
    return fig


def plot_inertial_relative_velocity_norms(t, v_i, v_ei, v_ni):
    mag_vi = np.linalg.norm(v_i, axis=0)
    mag_vei = np.linalg.norm(v_ei, axis=0)
    mag_vni = np.linalg.norm(v_ni, axis=0)
    fig, ax = plt.subplots()
    ax.plot(t[:-1]/3600, mag_vi, label='$v_i$')
    ax.plot(t[:-1]/3600, mag_vei, label='$v_{ei}$')
    ax.plot(t[:-1]/3600, mag_vni, label='$v_{ni}$')
    configure_axes(
        ax,
        xlabel="Time (hrs)",
        ylabel="Velocity Magnitudes (m/s)",
        title="Velocity Magnitude Comparison: Inertial-Relative Velocities"
    )
    ax.legend()
    return fig


def plot_earth_relative_velocity_norms(t, v_e, v_ie, v_ne):
    mag_ve = np.linalg.norm(v_e, axis=0)
    mag_vie = np.linalg.norm(v_ie, axis=0)
    mag_vne = np.linalg.norm(v_ne, axis=0)
    fig, ax = plt.subplots()
    ax.plot(t[:-1]/3600, mag_ve, label='$v_e$')
    ax.plot(t[:-1]/3600, mag_vie, label='$v_{ie}$')
    ax.plot(t[:-1]/3600, mag_vne, label='$v_{ne}$')
    configure_axes(
        ax,
        xlabel="Time (hrs)",
        ylabel="Velocity Magnitudes (m/s)",
        title="Velocity Magnitude Comparison: Earth-Relative Velocities"
    )
    ax.legend()
    return fig


def plot_gravity_vs_time(t, gravity):
    gravity = gravity.reshape((-1, 1))
    fig, ax = plt.subplots()
    ax.plot(t/3600, np.linalg.norm(gravity, axis=1))
    configure_axes(
        ax,
        xlabel="Time (hrs)",
        ylabel="Local Gravity ($m/s^2$)",
        title="Local Gravity Variation"
    )
    return fig


def run_demo():

    # constants
    T = 10*60.0                 # sampling period (s)
    t_dur = 12*60*60.0          # duration (s)
    t = np.arange(0, t_dur, T)  # time array
    lat = (np.pi/2) * (t/t_dur) # latitudes
    lon = 0*t                   # longitudes
    hae = 0*t + 1000            # heights above ellipsoid

    # calculate position in e frame
    p_e = r3f.geodetic_to_ecef([lat, lon, hae])

    # calculate position in i frame
    p_i = np.zeros_like(p_e)
    for i in range(len(t)):
        C_ei = r3f.dcm_inertial_to_ecef(t[i])
        p_i[:,i] = C_ei.T @ p_e[:,i]

    # calculate the velocity in the e frame
    v_e = np.diff(p_e, axis=1)/T

    # calculate the velocity in the i frame
    v_i = np.diff(p_i, axis=1)/T

    # calculate the relative velocities
    v_ei = np.zeros_like(v_i)
    v_ie = np.zeros_like(v_e)
    v_ni = np.zeros_like(v_i)
    v_ne = np.zeros_like(v_e)
    for i in range(len(t)-1):
        C_ei = r3f.dcm_inertial_to_ecef(t[i])
        v_ei[:,i] = C_ei @ v_i[:,i]             # e frame's velocity relative to i frame
        v_ie[:,i] = C_ei.T @ v_e[:,i]           # i frame's velocity relative to e frame

        C_ne = r3f.dcm_ecef_to_navigation(lat[i], lon[i])
        v_ni[:,i] = C_ne @ v_ei[:,i]            # nav frame's velocity relative to i frame
        v_ne[:,i] = C_ne @ v_e[:,i]             # nav frame's velocity relative to e frame

        # you can also do v_ba = v_b + w_ba x p_b. Where a and b are two arbitrary reference frames.

    # calculate the local gravity along the flight
    gravity = somigliana(lat, hae)

    # plots
    fig = plot_inertial_position_velocity(p_i, v_i)
    save_figure(fig, "results/figures/kinematics_demo", "inertial_position_velocity")

    fig = plot_ecef_inertial_position_velocity(p_e, v_ei)
    save_figure(fig, "results/figures/kinematics_demo", "ecef_inertial_position_velocity")

    fig = plot_inertial_relative_velocity_norms(t, v_i, v_ei, v_ni)
    save_figure(fig, "results/figures/kinematics_demo", "inertial_relative_velocity_norms")

    fig = plot_earth_relative_velocity_norms(t, v_e, v_ie, v_ne)
    save_figure(fig, "results/figures/kinematics_demo", "earth_relative_velocity_norms")

    fig = plot_gravity_vs_time(t, gravity)
    save_figure(fig, "results/figures/kinematics_demo", "gravity_vs_time")


if __name__=="__main__":
    run_demo()
    # plt.show()