from gala.units import galactic
from .particle_seeder import gen_exponential_distribution

import numpy as np

class ParticleSet:

    def __init__(self, positions=None, velocities=None, masses=None, radii=None, units=galactic):
        self.positions = positions
        self.velocities = velocities

        self.masses = masses
        self.radii = radii
    
        self.units = units


    def seed(self):
        raise NotImplementedError
    

    def gen_velocities(self, pot, rotation=1):
        
        vtot = pot.energy(self.positions)

        px, py, pz = self.positions
        theta = np.arctan2(py, px)
        incs = np.arctan2(pz, np.sqrt(px ** 2 + py ** 2))

        vx = -vtot * np.sin(theta) * rotation
        vy = vtot * np.cos(theta) * rotation
        vz = np.sqrt(vx ** 2 + vy ** 2) * np.sin(incs)

        self.velocities = np.array([vx, vy, vz])
        
        velocities = None
        return velocities
    
    
    def sigma_gas(self):
        return self.masses / (np.pi * self.radii ** 2)
    

    def save(self, set, fn):
        x,y,z = self.positions
        vx, vy, vz = self.velocities

        np.save(self, np.array([x,y,z,vx,vy,vz]))

    @staticmethod
    def from_file(fn):
        data = np.load(fn)
        x, y, z, vx, vy, vz = data

        return ParticleSet(positions=[x,y,z], velocities=[vx,vy,vz])



class ExponentialParticleSet(ParticleSet):

    def __init__(self, scale_length, scale_height, **kwargs):
        self.scale_height = scale_height
        self.scale_length = scale_length

        self.n_0 = 1 / (4 * np.pi * scale_length**2 * scale_height)

        super().__init__(**kwargs)
    
    def seed(self, Nparticles, potential, **kwargs):
        R, z = gen_exponential_distribution(Nparticles, self.scale_length, self.scale_height)
        phi = np.random.uniform(0, 2*np.pi, len(R))

        x = R * np.cos(phi)
        y = R * np.sin(phi)

        self.positions = np.stack([x, y, z])
        self.gen_velocities(potential, **kwargs)

    
