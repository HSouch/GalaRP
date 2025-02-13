
from ..sim import RPSim



def test_sim_init():

    sim = RPSim()
    assert sim is not None


def test_simple_run():
    sim = RPSim()
    results = sim.run()

    assert results is not None


def test_defaults():
    # This is to check that defaults are assigned when nothing user-defined is supplied
    sim = RPSim()

    assert sim.satellite_potential is not None
    assert sim.units is not None
