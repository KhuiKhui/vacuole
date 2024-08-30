import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
DIGITS_AND_LETTERS = DIGITS + LETTERS 

TYPES = ["var", "str", "int"]
CONSTANTS = ["true", "false", "null"]
FUNCTIONS = ["if", "else if", "else", "for", "while", "function"]
KEYWORDS = TYPES + CONSTANTS + FUNCTIONS
