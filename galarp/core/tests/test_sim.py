
from ..sim import RPSim
from ..outputs import OrbitContainer



def test_sim_init():

    sim = RPSim()
    assert sim is not None


def test_simple_run():
    sim = RPSim()
    results = sim.run()

    assert results is not None
    assert isinstance(results, OrbitContainer)


def test_defaults():
    # This is to check that defaults are assigned when nothing user-defined is supplied
    sim = RPSim()

    assert sim.satellite_potential is not None
    assert sim.units is not None
    assert sim.particles is not None
    assert sim.wind is not None
    assert sim.rho_icm is not None
