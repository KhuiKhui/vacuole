class Number:
    def __init__(self, number):
        self.number = number
    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.number + other.number)
    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.number - other.number)
    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.number * other.number)
    def div_by(self, other):
        if isinstance(other, Number):
            return Number(self.number / other.number)
    def raise_power(self, other):
        if isinstance(other, Number):
            return Number(self.number ** other.number)
    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.number % other.number)
    def is_greater_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.number > other.number))
    def is_greater_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.number > other.number))
    def is_greater_or_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.number >= other.number))
    def is_less_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.number < other.number))
    def is_less_or_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.number <= other.number))
    def is_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.number == other.number))
    def is_not_eq_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.number != other.number))
    def and_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.number and other.number))
    def or_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.number or other.number))
    def not_op(self):
        return Number(1 if self.number == 0 else 0)
    def bit_and_with(self, other):
        if isinstance(other, Number):
            return Number(self.number & other.number)
    def bit_or_with(self, other):
        if isinstance(other, Number):
            return Number(self.number | other.number)
    def bit_xor_with(self, other):
        if isinstance(other, Number):
            return Number(self.number ^ other.number)
    def bit_not_op(self, ):
        return Number(~self.number)
        
    def __repr__(self) -> str:
        return str(self.number)