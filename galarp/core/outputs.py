
from astropy import units as u


class OrbitContainer:

    def __init__(self, data, units=None, metadata={}):
        self.data = data
        self.units = units

        self.metadata = metadata
    

    def get_orbit_data(self, velocity_units = u.km/u.s, transposed=True):
        pos, vel = self.data.pos, self.data.vel

        x, y, z = pos.xyz.value
        vx, vy, vz = vel.d_xyz.value

        if transposed:
            x, y, z = x.T, y.T, z.T
            vx, vy, vz = vx.T, vy.T, vz.T

        return x, y, z, vx, vy, vz


    def get_times(self):
        return self.data.t.value
    

    