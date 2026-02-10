from ..components import winds as winds

from astropy import units as u


def BasicClusterWind(disk_wind_angle=0.):
    return winds.ConstantWind(strength=300 * u.km/u.s, disk_wind_angle=disk_wind_angle)


def BasicClusterDensity():
    return winds.ConstantDensity(density=1e-26 * u.g/u.cm**3)

