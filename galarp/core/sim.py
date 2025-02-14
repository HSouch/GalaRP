
from .. import builtins, components

import numpy as np

from astropy import units as u

from gala import integrate as gi
from gala.units import galactic



def F_RPS(t, particles, potential, wind, rho, shadow, **kwargs):
    units = kwargs.get("units", galactic)
    x, y, z, vx, vy, vz = particles.w
    q = np.stack([x, y, z])
    p = np.stack([vx, vy, vz])
    
    _t = np.array([0.0])
    acc = -potential(q, _t).T
    
    # Apply Ram Pressure Wind
    if kwargs.get("wind_on", True):
        v_rel = wind.evaluate(t) - p
        a_ram = (v_rel ** 2) * (rho.evaluate(t) / particles.sigma_gas)[:, np.newaxis]
        a_ram *= np.sign(v_rel)
        a_ram = a_ram.T
    
        # if kwargs.get("shadow_on", True):
        #     damping = shadow.evaluate(t, q, particles.sigms_gas).T
        #     a_ram *= damping

        acc += a_ram
    
    return np.vstack((p.T, acc))
    
    
class RPSim:
    def __init__(self, 
                 satellite_potential=builtins.satpots.JZ2023_Satellite(), 
                 particles=components.particles.ExponentialParticleSet(8, 0.5), 
                 wind=builtins.winds.BasicClusterWind(), 
                 rho_icm=(1e-26 * u.g/u.cm**3),
                 method=F_RPS, 
                 units=galactic, 
                 **kwargs):
        self.satellite_potential = satellite_potential
        self.particles = particles
        self.wind = wind
        self.rho_icm = rho_icm
        self.method = method

        
        self.units = units

        # Make sure we actually have particles to simulate
        if particles.positions is None:
            self.particles.seed(5000, self.satellite_potential)


    def ensure_common_units(self):
        units_to_compare = self.units
        for p in [self.satellite_potential, self.particles, self.wind]:
            assert p.units == units_to_compare, "Units do not match"
    

    def run(self, **kwargs):
        self.ensure_common_units()

        func_args = (self.particles, self.satellite_potential, self.wind, self.rho_icm, self.shadow)

        integrator = gi.RK5Integrator(
            self.method,
            func_args=func_args,
            func_units=galactic,
        )

        return 0

