import numpy as np
import matplotlib.pyplot as plt
import r3f

from src.ins.trajectories import circular_trajectory
from src.ins.earth import somigliana
from src.ins.plotting import save_figure, configure_axes

"""
Ellipsoidal Earth Demonstration

This example investigates how large-scale aircraft trajectories behave in
multiple Earth-referenced coordinate systems, including:

- local curvilinear coordinates,
- local tangent-plane coordinates,
- geodetic coordinates,
- ECEF coordinates,
- and rotating navigation frames.

The experiment highlights how Earth curvature affects navigation geometry,
frame transformations, and gravity variation over long distances.
"""


def plot_curvilinear_vs_tangent(curvilinear_traj, tangent_traj):
    fig, ax = plt.subplots()
    ax.plot(curvilinear_traj[1]/1e3, curvilinear_traj[0]/1e3, label="Curvilinear")
    ax.plot(tangent_traj[1]/1e3, tangent_traj[0]/1e3, label="Tangent")
    configure_axes(
        ax,
        xlabel="East, $y$ (km)",
        ylabel="North, $x$ (km)",
        title="Curvilinear vs Tangent-Frame Trajectory",
        equal=True,
    )
    ax.legend()
    return fig


def plot_curvilinear_vertical_vs_hae(theta_vec, curvilinear_traj, geodetic_traj):
    fig, ax = plt.subplots()
    ax.plot(theta_vec, curvilinear_traj[2], label="zc")
    ax.plot(theta_vec, geodetic_traj[2], label="hae")
    configure_axes(
        ax,
        xlabel="$\\theta_vec$, (rad)",
        ylabel="Height Above Ellipsoid (m)",
        title="Curvilinear Vertical Coordinate vs Height Above Ellipsoid",
        equal=False,
    )
    ax.legend()
    return fig


def plot_runway_relative_to_plane(nav_traj):
    fig, ax = plt.subplots()
    ax.plot(nav_traj[1]/1e3, nav_traj[0]/1e3)
    ax.plot(nav_traj[1][0]/1e3, nav_traj[0][0]/1e3, marker='o', color='red')
    configure_axes(
        ax,
        xlabel="East, $y_n$ (km)",
        ylabel="North, $x_n$ (km)",
        title="Runway Position Relative to the Aircraft",
        equal=False,
    )
    return fig


def plot_tangent_vertical_vs_nav_vertical(theta_vec, tangent_traj, nav_traj):
    fig, ax = plt.subplots()
    ax.plot(theta_vec, tangent_traj[2]/1e3, label='zt')
    ax.plot(theta_vec, nav_traj[2]/1e3, label='zn')
    configure_axes(
        ax,
        xlabel="$\\theta_vec$ (rad)",
        ylabel="Z (km)",
        title="Tangent-Frame Vertical Position vs Navigation-Frame Vertical Position",
        equal=False,
    )
    ax.legend()
    return fig


def plot_somigliana_gravity(theta_vec, gravity):
    fig, ax = plt.subplots()
    ax.plot(theta_vec, gravity)
    configure_axes(
        ax,
        xlabel="$\\theta_vec$ (rad)",
        ylabel="Gravity ($m/s^2$)",
        title="Somigliana Gravity Variation",
        equal=False,
    )
    return fig


def plot_distance_to_earth_center(theta_vec, d_flight, d_ellipse):
    fig, ax = plt.subplots()
    ax.plot(theta_vec, d_flight/1e3, label='flight')
    ax.plot(theta_vec, d_ellipse/1e3, label='ellipse')
    configure_axes(
        ax,
        xlabel="$\\theta_vec$ (rad)",
        ylabel="Distance to Earth Center (km)",
        title="Distance to Earth Center",
        equal=False,
    )
    ax.legend()
    return fig


def run_demo():

    # constants
    R = 1000e3      # Circular trajectory radius (m)
    delta_h = 1e3   # Peak altitude variation above trajectory origin (m)

    llh0 = np.array([39.535, -76.348, 212.0])           # Initial aircraft geodetic position
    theta_vec = np.linspace(np.pi, -np.pi, num=1000)    # Parameterize the circular trajectory over one complete revolution.

    # Generate a large circular aircraft trajectory in a local curvilinear frame.
    # The trajectory radius is intentionally large enough that flat-Earth
    # approximations begin to visibly diverge from Earth-following coordinates.
    curvilinear_traj = circular_trajectory(theta_vec, R, delta_h)

    # Transform the trajectory through several common navigation coordinate systems:
    #
    # Curvilinear -> Geodetic -> Tangent Frame
    #
    # These transformations allow comparison between Earth-following coordinates
    # and locally flat tangent-plane approximations.
    geodetic = r3f.curvilinear_to_geodetic(curvilinear_traj, llh0=llh0, degs=True)
    tangent_traj = r3f.geodetic_to_tangent(geodetic, llh0=llh0, degs=True)

    # Compute the apparent position of the original runway from the perspective
    # of the moving aircraft navigation frame.
    #
    # This illustrates how local navigation frames rotate and evolve as the
    # aircraft moves over the curved Earth surface.
    ecef_init = r3f.geodetic_to_ecef(llh0, degs=True)
    ecef_traj = r3f.geodetic_to_ecef(geodetic, degs=True)
    nav_traj = r3f.ecef_to_tangent(ecef_init, ecef_traj)

    # Evaluate local gravity magnitude along the trajectory using the Somigliana gravity model
    gravity = somigliana(geodetic[0]*np.pi/180, geodetic[2])


    # plots
    fig = plot_curvilinear_vs_tangent(curvilinear_traj, tangent_traj)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "curvilinear_vs_tangent")

    fig = plot_curvilinear_vertical_vs_hae(theta_vec, curvilinear_traj, geodetic)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "zc_vs_height")

    fig = plot_runway_relative_to_plane(nav_traj)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "runway_relative_motion")

    fig = plot_tangent_vertical_vs_nav_vertical(theta_vec, tangent_traj, nav_traj)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "vertical_frame_comparison")

    fig = plot_somigliana_gravity(theta_vec, gravity)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "somigliana_gravity")


    # Supplemental visualization:
    #
    # Height above the ellipsoid does not uniquely determine distance from the
    # Earth's center because the Earth is ellipsoidal rather than spherical.
    #
    # This figure helps explain why gravity variation depends on both:
    #
    # - latitude, and
    # - altitude.

    d_flight = np.sqrt(ecef_traj[0]**2 + ecef_traj[1]**2 + ecef_traj[2]**2)
    phic = np.arctan2(ecef_traj[2], np.sqrt(ecef_traj[0]**2 + ecef_traj[1]**2))
    r_ellipse = r3f.A_E*np.cos(phic)
    z_ellipse = r3f.B_E*np.sin(phic)
    d_ellipse = np.sqrt(r_ellipse**2 + z_ellipse**2)

    fig = plot_distance_to_earth_center(theta_vec, d_flight, d_ellipse)
    save_figure(fig, "results/figures/ellipsoidal_earth_demo", "distance_to_earth_center")

if __name__=="__main__":
    run_demo()
    # plt.show()