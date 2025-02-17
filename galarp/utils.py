
import numpy as np

def ellipse_coords(x, y, a, b, theta, num_points=100, b_is_ellipticity=False):
    # Generate angles for sampling
    angles = np.linspace(0, 2 * np.pi, num_points)

    # If b is supplied as an ellipticity (and not as the semiminor axis directly, calculate semiminor axis)
    if b_is_ellipticity:
        b = a * (1 - b)

    # Parametric equation for the ellipse
    x_coords = (
        x + a * np.cos(angles) * np.cos(theta) - b * np.sin(angles) * np.sin(theta)
    )
    y_coords = (
        y + a * np.cos(angles) * np.sin(theta) + b * np.sin(angles) * np.cos(theta)
    )
    z_coords = np.zeros(num_points)
    # Return the sampled coordinates as a NumPy array
    return x_coords, y_coords, z_coords
