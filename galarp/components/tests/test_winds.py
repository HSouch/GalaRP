from .test_base import TestBaseIterator

from .. import winds


class TestBaseWind(TestBaseIterator):
    
    iter_to_test = winds.Wind()


class TestInterpolatedWind(TestBaseWind):

    iter_to_test = winds.InterpolatedWind()