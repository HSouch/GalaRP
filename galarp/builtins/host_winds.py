from ..components import winds as winds

from astropy import units as u


def BasicClusterWind():
    return winds.ConstantWind(strength=300 * u.km/u.s, disk_wind_angle=0.)


def BasicClusterDensity():
    return winds.ConstantDensity(density=1e-26 * u.g/u.cm**3)

