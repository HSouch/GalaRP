from . import helpers
from .. import host_winds, particles, satellite_potentials




class TestJZ2023Satellite(helpers.TestSatPotBuiltin):
    
    obj = satellite_potentials.JZ2023_Satellite()


class TestNA2023Satellite(helpers.TestSatPotBuiltin):
    
    obj = satellite_potentials.NA2023_Satellite()


class RB2006_Satellite(helpers.TestSatPotBuiltin):
    
    obj = satellite_potentials.RB2006_Satellite()
    




class TestBasicClusterWind(helpers.TestWindBuiltin):
    
    obj = host_winds.BasicClusterWind()