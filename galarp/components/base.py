from gala.units import galactic
from ..utils import UnitSet

class Iterator:
    def __init__(self, units=galactic, name=None):
        self.name = name
        self.units = units

        self.unitset = UnitSet(self.units)

    def evaluate(self, t):
        raise NotImplementedError("Abstract Base Class")


    def __repr__(self):
        return f'{self.name} with {self.units} units.'