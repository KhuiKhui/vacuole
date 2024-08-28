from vacuole.values.number import *
class String:
    def __init__(self, string):
        self.string = string 
    def __repr__(self) -> str:
        return str(self.string)
    def add_to(self, other):
        if isinstance(other, String):
            return String(self.string + other.string)
    def mul_by(self, other):
        if isinstance(other, Number):
            return String(self.string * other.number)
