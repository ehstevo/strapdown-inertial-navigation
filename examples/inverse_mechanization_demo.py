import numpy as np
import matplotlib.pyplot as plt
import r3f
from pathlib import Path

from src.ins.trajectories import figure_eight_curvilinear, figure_eight_attitude
from src.ins.mechanization import inverse_mechanize
from src.ins.plotting import save_figure, configure_axes

"""
Inverse Mechanization Demonstration

This example generates synthetic IMU measurements from a prescribed
aircraft trajectory and attitude profile.

The demo illustrates:

- inverse inertial mechanization,
- navigation-frame velocity reconstruction,
- transport-rate effects,
- Earth-rate compensation,
- and ideal accelerometer/gyroscope signal generation.

The resulting synthetic IMU data is later reused for forward
mechanization and INS error studies.
"""


def plot_geodetic_trajectory(llh_t):
    fig, ax = plt.subplots()
    ax.plot(llh_t[1], llh_t[0])
    configure_axes(
        ax,
        xlabel="Longitude (deg)",
        ylabel="Latitude (deg)",
        title="Geodetic Aircraft Trajectory"
    )
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_useOffset(False)   # disables scientific notation
    return fig


def plot_altitude_profile(t, llh_t):
    fig, ax = plt.subplots()
    ax.plot(t/60, llh_t[2])
    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Height Above Ellipsoid (m)",
        title="Height Above Ellipsoid"
    )
    return fig


def plot_attitude_profile(t, rpy_t, include_yaw=True):
    fig, ax = plt.subplots()
    ax.plot(t/60, rpy_t[:,0], label='roll')
    ax.plot(t/60, rpy_t[:,1], label='pitch')
    if include_yaw:
        ax.plot(t/60, rpy_t[:,2], label='yaw')
    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Roll Pitch and Yaw (rad)",
        title="Aircraft Attitude Profile"
    )
    ax.legend()
    return fig


def plot_specific_force(t, fbbi_t, include_vertical=True):
    fig, ax = plt.subplots()
    ax.plot(t/60, fbbi_t[:, 0], label="$f_{b,bi,x}$")
    ax.plot(t/60, fbbi_t[:, 1], label="$f_{b,bi,y}$")
    if include_vertical:
        ax.plot(t/60, fbbi_t[:, 2], label="$f_{b,bi,z}$")
    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Specific Forces ($m/s^2$)",
        title="Specific Force Measurements"
    )
    ax.legend()
    return fig


def plot_angular_rate(t, wbbi_t, include_vertical=True):
    fig, ax = plt.subplots()
    ax.plot(t/60, wbbi_t[:, 0], label="$w_{b,bi,x}$")
    ax.plot(t/60, wbbi_t[:, 1], label="$w_{b,bi,y}$")
    if include_vertical:
        ax.plot(t/60, wbbi_t[:, 2], label="$w_{b,bi,z}$")
    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Rotation Rates (rad/s)",
        title="Angular-Rate Measurements"
    )
    ax.legend()
    return fig


def plot_navigation_velocity(t, vne_t):
    fig, ax = plt.subplots()
    ax.plot(t/60, vne_t[:, 0], label="$v_{ne',x}$")
    ax.plot(t/60, vne_t[:, 1], label="$v_{ne',y}$")
    ax.plot(t/60, vne_t[:, 2], label="$v_{ne',z}$")
    configure_axes(
        ax,
        xlabel="Time (min)",
        ylabel="Velocities (m/s)",
        title="Navigation-Frame Velocity"
    )
    ax.legend()
    return fig


def run_demo():

    # save data
    SAVE_BINARY = True
    OUTPUT_DATA = Path("data/data_fbbi_wbbi_vne.bin")

    # simulation parameters
    t_dur = 6*60.0              # duration of simulation (s)
    T = 0.1                     # sampling period (s)
    R = 1000.0                  # radius of figure 8 (m)
    delta_h = 100.0             # change in height (m)

    # Initial aircraft geodetic position
    lat0 = 39.535           # latitude of origin (deg)
    lon0 = -76.348          # longitude of origin (deg)
    hae0 = 212.0            # height above ellipsoid of origin (m)

    # Number of simulation samples
    K = round(t_dur/T) + 1

    # parameterize the trajectory
    theta_vec = np.linspace(0, 2*np.pi, K)

    # define time array
    t = np.arange(0, K) * T

    # Generate the prescribed aircraft motion:
    #
    # - figure-eight position trajectory
    # - and smooth aircraft attitude profile
    #
    # These truth states will later be inverse mechanized into synthetic
    # IMU measurements.
    xyz_curvilinear = figure_eight_curvilinear(theta_vec, R, delta_h)
    rpy_t = figure_eight_attitude(theta_vec)

    # Convert the local curvilinear trajectory into geodetic coordinates.
    llh_t = r3f.curvilinear_to_geodetic(xyz_curvilinear, [lat0, lon0, hae0], degs=True)

    # trajectory plots
    fig = plot_geodetic_trajectory(llh_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "geodetic_trajectory")

    fig = plot_altitude_profile(t, llh_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "altitude_profile")

    fig = plot_attitude_profile(t, rpy_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "attitude_profile")

    # Perform inverse mechanization.
    #
    # Given the prescribed aircraft trajectory and attitude profile,
    # compute the ideal:
    #
    # - accelerometer measurements,
    # - gyroscope measurements,
    # - and navigation-frame velocity.
    #
    # These quantities represent the synthetic IMU signals that would
    # generate the specified aircraft motion.

    llh_t[0:2,:] = llh_t[0:2,:] * (np.pi/180)   # Mechanization equations operate in radians.
    fbbi_t, wbbi_t, vne_t = inverse_mechanize(llh_t.T, rpy_t, T, t_dur)

    # inverse mechanization plots
    fig = plot_specific_force(t, fbbi_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "specific_force")

    fig = plot_angular_rate(t, wbbi_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "angular_rate")

    fig = plot_navigation_velocity(t, vne_t)
    save_figure(fig, "results/figures/inverse_mechanization_demo", "navigation_velocity")

    # Save specific forces, rotation rates, and velocities to binary file
    if SAVE_BINARY:
        M = np.hstack((fbbi_t, wbbi_t, vne_t))
        M.tofile(OUTPUT_DATA)


if __name__=="__main__":
    run_demo()
    # plt.show()