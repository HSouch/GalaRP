from ..components import winds as winds

from astropy import units as u


def BasicClusterWind():
    return winds.ConstantWind(strength=500 * u.km/u.s, disk_wind_angle=0)

