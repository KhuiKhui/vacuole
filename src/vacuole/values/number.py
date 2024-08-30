from vacuole.values.type import *

class Number(Type):
    def __init__(self, value):
        super().__init__(value)
    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
    def div_by(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
    def raise_power(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
    def is_greater_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value))
    def is_greater_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value))
    def is_greater_or_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value))
    def is_less_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value))
    def is_less_or_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value))
    def is_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value))
    def is_not_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value))
    def and_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value))
    def or_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value))
    def not_op(self):
        return Number(1 if self.value == 0 else 0)
    def bit_and_with(self, other):
        if isinstance(other, Number):
            return Number(self.value & other.value)
    def bit_or_with(self, other):
        if isinstance(other, Number):
            return Number(self.value | other.value)
    def bit_xor_with(self, other):
        if isinstance(other, Number):
            return Number(self.value ^ other.value)
    def bit_not_op(self):
        return Number(~self.value)
        
    def __repr__(self) -> str:
        return str(self.value)