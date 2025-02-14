import numpy as np

from astropy import units as u
from gala.units import galactic
from .base import Iterator


##################################################################
#####                    WIND  CLASSES                       #####
##################################################################

class Wind(Iterator):
    
    def __init__(self, strength=500, disk_wind_angle=None,  units=galactic):
        super().__init__(units=units, name="RPWind")
        self.disk_wind_angle = disk_wind_angle

    def unit_vector(self, t):
        return np.array([0, np.sin(self.disk_wind_angle), np.cos(self.disk_wind_angle)])
    


class ConstantWind(Wind):
    def __init__(self, units=galactic, disk_wind_angle = 0, strength=500  * u.km/u.s):
        super().__init__(disk_wind_angle, units=units)
        
        self.strength = (strength.to(units["length"]/units["time"])).value


    def evaluate(self, t):
        return self.unit_vector(t) * self.strength

    
class InterpolatedWind(Wind):

    def __init__(self, units=galactic):
        super().__init__(units=units)




##################################################################
#####                  DENSITY  CLASSES                     ######
##################################################################


class Density(Iterator):

    def __init__(self, units=galactic):
        super().__init__(units=units, name="RPDensity")


class ConstantDensity(Density):
    def __init__(self, density=1e-26 * u.g/u.cm**3, units=galactic):
        super().__init__(units=units)
        
        self.density = (density.to(units["mass"]/units["length"]**3)).value

