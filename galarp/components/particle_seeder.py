import ctypes
import numpy as np
import os


def gen_exponential_distribution(pcount, h_R, h_z):

    # TODO - Change this back once the C++ code is working properly
    return _gen_exponential_distribution_numpy(pcount, h_R, h_z)


    try:
        return _gen_exponential_distribution_ctypes(pcount, h_R, h_z)
    
    except Exception as e:
        print("Error using ctypes:", e)
        return _gen_exponential_distribution_numpy(pcount, h_R, h_z)


def _gen_exponential_distribution_ctypes(pcount, h_R, h_z):
    current_dir = os.path.dirname(os.path.abspath(__file__))    
    testlib = ctypes.CDLL(os.path.join(current_dir, "ccomponents/particleseeder.o"))

    class ParticleSet(ctypes.Structure):
        _fields_ = [
            ("R", ctypes.POINTER(ctypes.c_double)),
            ("z", ctypes.POINTER(ctypes.c_double)),

            ("count", ctypes.c_size_t),
        ]

    testlib.seed_particles.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float]
    testlib.seed_particles.restype = ctypes.POINTER(ParticleSet)

    testlib.free_particles.argtypes = [ctypes.POINTER(ParticleSet)]
    testlib.free_particles.restype = None

    particles = testlib.seed_particles(int(pcount), h_R, h_z)
    count = particles.contents.count

    R = np.ctypeslib.as_array(particles.contents.R, shape=(count,))
    z = np.ctypeslib.as_array(particles.contents.z, shape=(count,))

    print("Number of particles:", count)
    print("First 5 R-coordinates:", R[:5])
    print("First 5 z-coordinates:", z[:5])

    # Free the memory
    testlib.free_particles(particles)

    return [R, z]


def _gen_exponential_distribution_numpy(pcount, h_R, h_z, max_tries=1000):

    n0 = 1 / (4 * np.pi * h_R**2 * h_z)
    R, z = [], []
    for i in range(pcount):
        for j in range(max_tries):
            r_attempt = np.random.uniform(0, 5*h_R)
            z_attempt = np.random.uniform(-5*h_z, 5*h_z)

            p = n0 * np.exp(-(r_attempt / h_R)) * np.exp(-(np.abs(z_attempt) / h_z))

            if p >= np.random.uniform(0, 1):
                R.append(r_attempt)
                z.append(z_attempt)
                break

    return [np.array(R), np.array(z)]
