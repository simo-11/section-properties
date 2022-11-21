import contextlib
import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from sectionproperties.pre.pre import DEFAULT_MATERIAL


@contextlib.contextmanager
def plotting_context(
    ax=None, pause=True, title="", filename="", render=True, axis_index=None, **kwargs
):
    """Executes code required to set up a matplotlib figure.

    :param ax: Axes object on which to plot
    :type ax: :class:`matplotlib.axes.Axes`
    :param bool pause: If set to true, the figure pauses the script until the window is closed. If
        set to false, the script continues immediately after the window is rendered.
    :param string title: Plot title
    :param string filename: Pass a non-empty string or path to save the image as. If this option is
        used, the figure is closed after the file is saved.
    :param bool render: If set to False, the image is not displayed. This may be useful if the
        figure or axes will be embedded or further edited before being displayed.
    :param axis_index: If more than 1 axes is created by subplot, then this is the axis to plot on.
        This may be a tuple if a 2D array of plots is returned.  The default value of None will
        select the top left plot.
    :type axis_index: Union[None, int, Tuple(int)]
    :param kwargs: Passed to :func:`matplotlib.pyplot.subplots`
    """

    if filename:
        render = False

    if ax is None:
        if not render:
            plt.ioff()
        elif pause:
            plt.ioff()
        else:
            plt.ion()

        ax_supplied = False
        (fig, ax) = plt.subplots(**kwargs)

        try:
            if axis_index is None:
                axis_index = (0,) * ax.ndim
            ax = ax[axis_index]
        except (AttributeError, TypeError):
            pass  # only 1 axis, not an array
        except IndexError as exc:
            raise ValueError(
                f"axis_index={axis_index} is not compatible with arguments to subplots: {kwargs}"
            ) from exc
    else:
        fig = ax.get_figure()
        ax_supplied = True
        if not render:
            plt.ioff()

    yield fig, ax

    ax.set_title(title)
    plt.tight_layout()
    ax.set_aspect("equal", anchor="C")

    # if no axes was supplied, finish the plot and return the figure and axes
    if ax_supplied:
        # if an axis was supplied, don't continue with displaying or configuring the plot
        return

    if filename:
        fig.savefig(filename, dpi=fig.dpi)
        plt.close(fig)  # close the figure to free the memory
        return  # if the figure was to be saved, then don't show it also

    if render:
        if pause:
            plt.show()
        else:
            plt.draw()
            plt.pause(0.001)


def draw_principal_axis(ax, phi, cx, cy):
    """
    Draws the principal axis on a plot.

    :param ax: Axes object on which to plot
    :type ax: :class:`matplotlib.axes.Axes`
    :param float phi: Principal axis angle in radians
    :param float cx: x-location of the centroid
    :param float cy: y-location of the centroid
    """
    # get current axis limits
    (xmin, xmax) = ax.get_xlim()
    (ymin, ymax) = ax.get_ylim()
    lims = [xmin, xmax, ymin, ymax]

    # form rotation matrix
    R = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])

    # get basis vectors in the directions of the principal axes
    x11_basis = R.dot(np.array([1, 0]))
    y22_basis = R.dot(np.array([0, 1]))

    def add_point(vec, basis, centroid, num, denom):
        """Adds a point to the list *vec* if there is an intersection."""

        if denom != 0:
            point = basis * num / denom + centroid
            vec.append([point[0], point[1]])

    def get_principal_points(basis, lims, centroid):
        """Determines the intersections of the principal axis with the four lines defining a
        bounding box around the limits of the cross-section. The middle two intersection points are
        returned for plotting.

        :param basis: Basis (unit) vector in the direction of the principal axis
        :type basis: :class:`numpy.ndarray`
        :param lims: Tuple containing the axis limits *(xmin, xmax, ymin, ymax)*
        :type lims: tuple(float, float, float, float)
        :param centroid: Centroid *(cx, cy)* of the cross-section, through which the principal axis
            passes
        :type centroid: list[float, float]
        """

        pts = []  # initialise list containing the intersection points

        # add intersection points to the list
        add_point(pts, basis, centroid, lims[0] - centroid[0], basis[0])
        add_point(pts, basis, centroid, lims[1] - centroid[0], basis[0])
        add_point(pts, basis, centroid, lims[2] - centroid[1], basis[1])
        add_point(pts, basis, centroid, lims[3] - centroid[1], basis[1])

        # sort point vector
        pts = np.array(pts)
        pts = pts[pts[:, 0].argsort()]  # stackoverflow sort numpy array by col

        # if there are four points, take the middle two points
        if len(pts) == 4:
            return pts[1:3, :]

        return pts

    # get intersection points for the 11 and 22 axes
    x11 = get_principal_points(x11_basis, lims, [cx, cy])
    y22 = get_principal_points(y22_basis, lims, [cx, cy])

    # plot the principal axis
    ax.plot(x11[:, 0], x11[:, 1], "k--", alpha=0.5, label="11-axis")
    ax.plot(y22[:, 0], y22[:, 1], "k-.", alpha=0.5, label="22-axis")


def print_results(cross_section, fmt):
    """Prints the results that have been calculated to the terminal.

    :param cross_section: structural cross-section object
    :type cross_section: :class:`~sectionproperties.analysis.section.CrossSection`
    :param string fmt: Number format
    """

    if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
        prefix = "E."
    else:
        prefix = ""

    table = Table(title="Section Properties")
    table.add_column("Property", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green")

    area = cross_section.get_area()
    if area is not None:
        table.add_row("A", "{:>{fmt}}".format(area, fmt=fmt))

    perimeter = cross_section.get_perimeter()
    if perimeter is not None:
        table.add_row("Perim.", "{:>{fmt}}".format(perimeter, fmt=fmt))

    if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
        mass = cross_section.get_mass()
        if mass is not None:
            table.add_row("Mass", "{:>{fmt}}".format(mass, fmt=fmt))

    if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
        ea = cross_section.get_ea()
        if ea is not None:
            table.add_row("E.A", "{:>{fmt}}".format(ea, fmt=fmt))

    (qx, qy) = cross_section.get_q()
    if qx is not None:
        table.add_row(prefix + "Qx", "{:>{fmt}}".format(qx, fmt=fmt))
        table.add_row(prefix + "Qy", "{:>{fmt}}".format(qy, fmt=fmt))

    (cx, cy) = cross_section.get_c()
    if cx is not None:
        table.add_row("cx", "{:>{fmt}}".format(cx, fmt=fmt))
        table.add_row("cy", "{:>{fmt}}".format(cy, fmt=fmt))

    (ixx_g, iyy_g, ixy_g) = cross_section.get_ig()
    if ixx_g is not None:
        table.add_row(prefix + "Ixx_g", "{:>{fmt}}".format(ixx_g, fmt=fmt))
        table.add_row(prefix + "Iyy_g", "{:>{fmt}}".format(iyy_g, fmt=fmt))
        table.add_row(prefix + "Ixy_g", "{:>{fmt}}".format(ixy_g, fmt=fmt))

    (ixx_c, iyy_c, ixy_c) = cross_section.get_ic()
    if ixx_c is not None:
        table.add_row(prefix + "Ixx_c", "{:>{fmt}}".format(ixx_c, fmt=fmt))
        table.add_row(prefix + "Iyy_c", "{:>{fmt}}".format(iyy_c, fmt=fmt))
        table.add_row(prefix + "Ixy_c", "{:>{fmt}}".format(ixy_c, fmt=fmt))

    (zxx_plus, zxx_minus, zyy_plus, zyy_minus) = cross_section.get_z()
    if zxx_plus is not None:
        table.add_row(prefix + "Zxx+", "{:>{fmt}}".format(zxx_plus, fmt=fmt))
        table.add_row(prefix + "Zxx-", "{:>{fmt}}".format(zxx_minus, fmt=fmt))
        table.add_row(prefix + "Zyy+", "{:>{fmt}}".format(zyy_plus, fmt=fmt))
        table.add_row(prefix + "Zyy-", "{:>{fmt}}".format(zyy_minus, fmt=fmt))

    (rx, ry) = cross_section.get_rc()
    if rx is not None:
        table.add_row("rx", "{:>{fmt}}".format(rx, fmt=fmt))
        table.add_row("ry", "{:>{fmt}}".format(ry, fmt=fmt))

    phi = cross_section.get_phi()
    (i11_c, i22_c) = cross_section.get_ip()
    if phi is not None:
        table.add_row("phi", "{:>{fmt}}".format(phi, fmt=fmt))
        table.add_row(prefix + "I11_c", "{:>{fmt}}".format(i11_c, fmt=fmt))
        table.add_row(prefix + "I22_c", "{:>{fmt}}".format(i22_c, fmt=fmt))

    (z11_plus, z11_minus, z22_plus, z22_minus) = cross_section.get_zp()
    if z11_plus is not None:
        table.add_row(prefix + "Z11+", "{:>{fmt}}".format(z11_plus, fmt=fmt))
        table.add_row(prefix + "Z11-", "{:>{fmt}}".format(z11_minus, fmt=fmt))
        table.add_row(prefix + "Z22+", "{:>{fmt}}".format(z22_plus, fmt=fmt))
        table.add_row(prefix + "Z22-", "{:>{fmt}}".format(z22_minus, fmt=fmt))

    (r11, r22) = cross_section.get_rp()
    if r11 is not None:
        table.add_row("r11", "{:>{fmt}}".format(r11, fmt=fmt))
        table.add_row("r22", "{:>{fmt}}".format(r22, fmt=fmt))

    if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
        e_eff = cross_section.get_e_eff()
        g_eff = cross_section.get_g_eff()
        if e_eff is not None:
            table.add_row("E_eff", "{:>{fmt}}".format(e_eff, fmt=fmt))
            table.add_row("G_eff", "{:>{fmt}}".format(g_eff, fmt=fmt))

        nu_eff = cross_section.get_nu_eff()
        if nu_eff is not None:
            table.add_row("nu_eff", "{:>{fmt}}".format(nu_eff, fmt=fmt))

    j = cross_section.get_j()
    if j is not None:
        table.add_row("J", "{:>{fmt}}".format(j, fmt=fmt))

    gamma = cross_section.get_gamma()
    if gamma is not None:
        table.add_row("Iw", "{:>{fmt}}".format(gamma, fmt=fmt))

    (x_se, y_se) = cross_section.get_sc()
    if x_se is not None:
        table.add_row("x_se", "{:>{fmt}}".format(x_se, fmt=fmt))
        table.add_row("y_se", "{:>{fmt}}".format(y_se, fmt=fmt))

    (x_st, y_st) = cross_section.get_sc_t()
    if x_se is not None:
        table.add_row("x_st", "{:>{fmt}}".format(x_st, fmt=fmt))
        table.add_row("y_st", "{:>{fmt}}".format(y_st, fmt=fmt))

    (x1_se, y2_se) = cross_section.get_sc_p()
    if x1_se is not None:
        table.add_row("x1_se", "{:>{fmt}}".format(x1_se, fmt=fmt))
        table.add_row("y2_se", "{:>{fmt}}".format(y2_se, fmt=fmt))

    (A_sx, A_sy) = cross_section.get_As()
    if A_sx is not None:
        table.add_row(prefix + "A_sx", "{:>{fmt}}".format(A_sx, fmt=fmt))
        table.add_row(prefix + "A_sy", "{:>{fmt}}".format(A_sy, fmt=fmt))

    (A_s11, A_s22) = cross_section.get_As_p()
    if A_s11 is not None:
        table.add_row(prefix + "A_s11", "{:>{fmt}}".format(A_s11, fmt=fmt))
        table.add_row(prefix + "A_s22", "{:>{fmt}}".format(A_s22, fmt=fmt))

    (beta_x_plus, beta_x_minus, beta_y_plus, beta_y_minus) = cross_section.get_beta()
    if beta_x_plus is not None:
        table.add_row("betax+", "{:>{fmt}}".format(beta_x_plus, fmt=fmt))
        table.add_row("betax-", "{:>{fmt}}".format(beta_x_minus, fmt=fmt))
        table.add_row("betay+", "{:>{fmt}}".format(beta_y_plus, fmt=fmt))
        table.add_row("betay-", "{:>{fmt}}".format(beta_y_minus, fmt=fmt))

    (
        beta_11_plus,
        beta_11_minus,
        beta_22_plus,
        beta_22_minus,
    ) = cross_section.get_beta_p()
    if beta_x_plus is not None:
        table.add_row("beta11+", "{:>{fmt}}".format(beta_11_plus, fmt=fmt))
        table.add_row("beta11-", "{:>{fmt}}".format(beta_11_minus, fmt=fmt))
        table.add_row("beta22+", "{:>{fmt}}".format(beta_22_plus, fmt=fmt))
        table.add_row("beta22-", "{:>{fmt}}".format(beta_22_minus, fmt=fmt))

    (x_pc, y_pc) = cross_section.get_pc()
    if x_pc is not None:
        table.add_row("x_pc", "{:>{fmt}}".format(x_pc, fmt=fmt))
        table.add_row("y_pc", "{:>{fmt}}".format(y_pc, fmt=fmt))

    (sxx, syy) = cross_section.get_s()
    if sxx is not None:
        if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
            table.add_row("M_p,xx", "{:>{fmt}}".format(sxx, fmt=fmt))
            table.add_row("M_p,yy", "{:>{fmt}}".format(syy, fmt=fmt))
        else:
            table.add_row("Sxx", "{:>{fmt}}".format(sxx, fmt=fmt))
            table.add_row("Syy", "{:>{fmt}}".format(syy, fmt=fmt))

    (sf_xx_plus, sf_xx_minus, sf_yy_plus, sf_yy_minus) = cross_section.get_sf()
    if sf_xx_plus is not None:
        table.add_row("SF_xx+", "{:>{fmt}}".format(sf_xx_plus, fmt=fmt))
        table.add_row("SF_xx-", "{:>{fmt}}".format(sf_xx_minus, fmt=fmt))
        table.add_row("SF_yy+", "{:>{fmt}}".format(sf_yy_plus, fmt=fmt))
        table.add_row("SF_yy-", "{:>{fmt}}".format(sf_yy_minus, fmt=fmt))

    (x11_pc, y22_pc) = cross_section.get_pc_p()
    if x_pc is not None:
        table.add_row("x11_pc", "{:>{fmt}}".format(x11_pc, fmt=fmt))
        table.add_row("y22_pc", "{:>{fmt}}".format(y22_pc, fmt=fmt))

    (s11, s22) = cross_section.get_sp()
    if s11 is not None:
        if list(set(cross_section.materials)) != [DEFAULT_MATERIAL]:
            table.add_row("M_p,11", "{:>{fmt}}".format(s11, fmt=fmt))
            table.add_row("M_p,22", "{:>{fmt}}".format(s22, fmt=fmt))
        else:
            table.add_row("S11", "{:>{fmt}}".format(s11, fmt=fmt))
            table.add_row("S22", "{:>{fmt}}".format(s22, fmt=fmt))

    (sf_11_plus, sf_11_minus, sf_22_plus, sf_22_minus) = cross_section.get_sf_p()
    if sf_11_plus is not None:
        table.add_row("SF_11+", "{:>{fmt}}".format(sf_11_plus, fmt=fmt))
        table.add_row("SF_11-", "{:>{fmt}}".format(sf_11_minus, fmt=fmt))
        table.add_row("SF_22+", "{:>{fmt}}".format(sf_22_plus, fmt=fmt))
        table.add_row("SF_22-", "{:>{fmt}}".format(sf_22_minus, fmt=fmt))

    console = Console()
    console.print(table)
    print("")
