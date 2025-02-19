from .outputs import OrbitContainer
from .. import builtins, components

import numpy as np

from astropy import units as u

from gala import dynamics as gd
from gala import integrate as gi
from gala.units import galactic



def F_RPS(t, w, particles, potential, wind, rho_icm, shadow, kwargs):
    units = kwargs.get("units", galactic)
    x, y, z, vx, vy, vz = w
    q = np.stack([x, y, z], axis=1)
    p = np.stack([vx, vy, vz], axis=1)
    
    _t = np.array([0.0])
    acc = -potential._gradient(q, _t).T
    
    # Apply Ram Pressure Wind
    if kwargs.get("wind_on", True):
        v_rel = wind.evaluate(t) - p
        a_ram = (v_rel ** 2) * (rho_icm.evaluate(t) / particles.surface_density()) * np.sign(v_rel) # [:, np.newaxis]
        a_ram = a_ram.T
    
        if kwargs.get("shadow_on", True) and shadow is not None:
            damping = shadow.evaluate(t, q, particles.sigma_gas).T
            a_ram *= damping

        acc += a_ram
    
    return np.vstack((p.T, acc))
    
    
class RPSim:
    def __init__(self, 
                 satellite_potential=builtins.satpots.JZ2023_Satellite(), 
                 particles=components.particles.ExponentialParticleSet(8, 0.5), 
                 wind=builtins.host_winds.BasicClusterWind(), 
                 rho_icm=builtins.host_winds.BasicClusterDensity(),
                 shadow=None,
                 method=F_RPS, 
                 units=galactic, 
                 **kwargs):
        self.satellite_potential = satellite_potential
        self.particles = particles
        self.wind = wind
        self.rho_icm = rho_icm

        self.shadow = shadow

        self.method = method

        self.units = units

        # Make sure we actually have particles to simulate
        if particles.positions is None:
            self.particles.seed(5000, self.satellite_potential)


    def ensure_common_units(self):
        units_to_compare = self.units
        for p in [self.satellite_potential, self.particles, self.wind]:
            assert p.units == units_to_compare, "Units do not match"
    

    def run(self, dt=5, integration_time=100.,  **kwargs):
        self.ensure_common_units()

        func_args = (self.particles, self.satellite_potential, self.wind, self.rho_icm, self.shadow, kwargs)
        integrator = gi.RK5Integrator(
            self.method,
            func_args=func_args,
            func_units=galactic,
        )

        self.particles.container.append(self.particles.phase_space_positions())

        orbits = integrator.run(
            gd.combine(self.particles.container), dt=dt, t1=0, t2=integration_time
        )

        output_metadata = {"WIND": self.wind,
                           "POTENTIAL": self.satellite_potential,
                           "RHO_ICM": self.rho_icm,
                           "SHADOW": self.shadow,
                           }

        return OrbitContainer(data=orbits, 
                              units=self.units,
                              metadata=output_metadata)


    def info(self):
        print("Galarp Simulation with:")
        print(f"  {self.particles}  ")
        print(f"  {self.rho_icm}  ")
        print(f"  {self.wind}  ")
        print(f"  {self.satellite_potential}  ")
    