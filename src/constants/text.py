import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
DIGITS_AND_LETTERS = DIGITS + LETTERS 

TYPES = ["var"]
CONSTANTS = ["true", "false", "null"]
FUNCTIONS = ["if", "else if", "else"]
KEYWORDS = TYPES + CONSTANTS + FUNCTIONS
