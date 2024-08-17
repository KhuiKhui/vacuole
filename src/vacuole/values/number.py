class Number:
    def __init__(self, number):
        self.number = number
        self.set_pos()
    def set_pos(self, start=None, end=None):
        self.start = start
        self.end = end
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
        
    def __repr__(self) -> str:
        return str(self.number)