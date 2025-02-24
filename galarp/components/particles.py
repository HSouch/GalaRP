from astropy import constants as c
from astropy import units as u

from gala.units import galactic
from gala import dynamics as gd
from .particle_seeder import gen_exponential_distribution

from ..utils import UnitSet

import numpy as np

class ParticleSet:

    def __init__(self, positions=None, velocities=None, 
                 masses=5e4 * u.Msun, 
                 radii=40 * u.pc, 
                 units=galactic):
        self.container = []
        
        # Initial positions and velocities
        self.positions = positions
        self.velocities = velocities

        self.original_mass_units = masses.unit
        self.original_radius_units = radii.unit

        self.masses = masses.to(units["mass"]).value
        self.radii = radii.to(units["length"]).value

        self.sigma_gas = self.masses / (np.pi * self.radii ** 2)
    
        self.units = units
        self.unitset = UnitSet(self.units)
        
    
    def phase_space_positions(self):
        return gd.PhaseSpacePosition(pos=self.positions , 
                                    vel=self.velocities )

    def seed(self):
        raise NotImplementedError
    

    def gen_velocities(self, potential, rotation=1, **kwargs):
        # Generate velocities using the enclosed mass of the potential
        xs, ys, zs = self.positions
        rs = np.sqrt(xs**2 + ys**2 + zs**2) * self.unitset.length
        theta = np.arctan2(ys, xs)
        incs = np.arctan2(zs, np.sqrt(xs**2 + ys**2))
        
        m_encs = potential.mass_enclosed([xs, ys, zs])

        v_circ = np.sqrt(c.G * m_encs / rs).to(self.unitset.velocity).value
        
        vx = -np.sin(theta) * v_circ * rotation
        vy = np.cos(theta) * v_circ * rotation
        vz = np.sqrt(vx ** 2 + vy ** 2) * np.sin(incs)

        self.velocities = np.array([vx, vy, vz])


    def surface_density(self):
        return self.sigma_gas
    

    def save(self, fn):
        x,y,z = self.positions
        vx, vy, vz = self.velocities

        np.save(fn, [x,y,z,vx,vy,vz])

    @staticmethod
    def from_file(fn, units=galactic):
        data = np.load(fn)
        x, y, z, vx, vy, vz = data

        return ParticleSet(positions=[x,y,z], velocities=[vx,vy,vz], units=units)



class UniformGridParticleSet(ParticleSet):

    def __init__(self, Rmax = 10 * u.kpc, spacing = 0.5 * u.kpc, 
                 disp_R = 0 * u.km / u.s, disp_z = 0 * u.km/u.s,  
                 units=galactic, **kwargs):
        super().__init__(units=units, **kwargs)
        
        self.Rmax = Rmax.to(units["length"]).value
        self.spacing = spacing.to(units["length"]).value

        self.disp_R = disp_R.to(self.unitset.velocity).value    
        self.disp_z = disp_z.to(self.unitset.velocity).value

    def seed(self, potential, **kwargs):
        xs, ys = np.meshgrid(np.arange(-self.Rmax, self.Rmax, self.spacing),
                             np.arange(-self.Rmax, self.Rmax, self.spacing))
        xs = xs.flatten()
        ys = ys.flatten()

        # Remove particles outside of Rmax
        rs = np.sqrt(xs**2 + ys**2)
        mask = rs <= self.Rmax
        xs = xs[mask]
        ys = ys[mask]

        zs = np.zeros_like(xs)

        self.positions = np.vstack((xs, ys, zs))

        self.gen_velocities(potential, **kwargs)

        # Add velocity dispersion to the disk if requested
        self.velocities[0] += np.random.normal(0, self.disp_R, self.velocities.shape[1])
        self.velocities[1] += np.random.normal(0, self.disp_R, self.velocities.shape[1])
        self.velocities[2] += np.random.normal(0, self.disp_z, self.velocities.shape[1])



class ExponentialParticleSet(ParticleSet):

    def __init__(self, Nparticles, scale_length, scale_height, units=galactic, **kwargs):
        self.Nparticles = Nparticles

        self.scale_height = scale_height
        self.scale_length = scale_length

        self.n_0 = 1 / (4 * np.pi * scale_length**2 * scale_height)

        super().__init__(units=units, **kwargs)
    
    def seed(self, potential, **kwargs):
        R, z = gen_exponential_distribution(self.Nparticles, self.scale_length, self.scale_height)
        phi = np.random.uniform(0, 2*np.pi, len(R))

        x = R * np.cos(phi)
        y = R * np.sin(phi)

        self.positions = np.stack([x, y, z])
        self.gen_velocities(potential, **kwargs)

        
    
