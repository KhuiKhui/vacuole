from vacuole.values.number import *
from vacuole.values.type import *
class String(Type):
    def __init__(self, string):
        super().__init__(string) 
    def __repr__(self) -> str:
        return str(self.value)
    def add_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
    def mul_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value)
