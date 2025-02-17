import numpy as np
from ...utils import ellipse_coords


def k3d_plot(
    orbit_containers,
    bgcolor=0,
    particle_color=0xFFFFFF,
    outname="test_out/orbits.html",
    duration=20,
    transpose=False,
    size=0.1,
    alpha=0.5,
):
    import k3d

    colors = [0xFFFFFF, 0x3387FF, 0xFF3333]

    # wind = orbit_containers[0].metadata["WIND"].vector.to(u.km / u.s).value
    # wind = np.array([wind[1], wind[0], wind[2]])
    # wind /= np.sqrt(np.sum(wind**2))
    # wind_length = 2
    # wind_x0, wind_y0, wind_z0 = 0, 0, 0

    ell_xs, ell_ys, ell_zs = ellipse_coords(0, 0, 10, 10, 0)

    plot = k3d.plot(
        fps=60,
        axes_helper=0,
        grid_visible=False,
        background_color=0,
    )

    for i, container in enumerate(orbit_containers):
        orbits = container.data

        pos = orbits.pos

        p_x, p_y, p_z = pos.xyz.value
        if transpose:
            p_x, p_y, p_z = p_x.T, p_y.T, p_z.T

        #vmin, vmax = -20, 20

        # v_z[v_z > vmax] = vmax
        # v_z[v_z < vmin] = vmin

        particles = k3d.points(
            np.vstack([p_x[0], p_y[0], p_z[0]]),
            point_size=size,
            color=colors[i],
            opacity=alpha,
        )
        plot += particles

        n_points = p_x.shape[0]

        t_int = np.arange(0, n_points, 1)
        t_sub = np.linspace(0, duration, n_points)

        particles.positions = {
            str(t): np.vstack([p_x[t_int[i]], p_y[t_int[i]], p_z[t_int[i]]]).T
            for i, t in enumerate(t_sub)
        }

    plot += k3d.line(np.vstack([ell_xs, ell_ys, ell_zs]).T, color=0xFFFFFF)

    plot.display()

    with open(outname, "w") as fp:
        fp.write(plot.get_snapshot())
