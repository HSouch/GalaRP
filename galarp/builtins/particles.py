from ..components import particles
from astropy import units as u

def LowResUniformGrid():
    return particles.UniformGridParticleSet(Rmax=15 * u.kpc, spacing=5 * u.kpc, 
                                            disp_R=10 * u.km / u.s, disp_z=5 * u.km / u.s)

def HighResUniformGrid():
    return particles.UniformGridParticleSet(Rmax=15 * u.kpc, spacing=0.2 * u.kpc, 
                                            disp_R=10 * u.km / u.s, disp_z=5 * u.km / u.s)

