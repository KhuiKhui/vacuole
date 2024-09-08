from vacuole.values.number import *
from vacuole.values.string import *
class Assigner:
    def assign(self, raw_value):
        if isinstance(raw_value, int) or isinstance(raw_value, float):
            return Number(raw_value)
        if isinstance(raw_value, str):
            return String(raw_value)
        return None