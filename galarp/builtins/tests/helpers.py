from numpy import sqrt, sum, isclose

class TestBuiltin:
    
    obj = None

    def test_init(self):
        assert self.obj is not None

    def test_units(self):
        assert self.obj.units is not None



class TestSatPotBuiltin(TestBuiltin):
    obj = None



class TestWindBuiltin(TestBuiltin):
    obj = None


    def test_unit_vector(self):
        assert self.obj.unit_vector(0) is not None
        assert len(self.obj.unit_vector(0)) == 3

        assert isclose(sqrt(sum(self.obj.unit_vector(0) ** 2)), 1.)


    def test_evaluate(self):
        assert self.obj.evaluate(0) is not None
        assert len(self.obj.evaluate(0)) == 3


class TestParticleSet(TestBuiltin):
    obj = None

