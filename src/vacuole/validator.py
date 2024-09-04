class Validator:
    def isValidDataType(self, type, input_value):
        value = input_value.value
        if type == "var":
            return True
        if isinstance(value, int) and type != "int":
            return False
        if isinstance(value, str) and type != "str":
            return False
        
        return True