from .. import base



class TestBaseIterator:
    
    iter_to_test = base.Iterator()

    def test_init(self):
        assert self.iter_to_test is not None

    def test_units(self):
        assert self.iter_to_test.units is not None
    
    def test_custom_print(self):
        assert isinstance(self.iter_to_test.__repr__(), str)

