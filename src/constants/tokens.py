#####  TOKEN TYPES  #####

##  MATH TOKENS  ##

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POWER = "POWER"
TT_MOD = "MOD"
TT_REMAINDER = "REMAINDER"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

##  MATH ASSIGNMENT OPERATORS  ##

TT_PLUS_ASSIGN = "PLUS_ASSIGN"
TT_MINUS_ASSIN = "MINUS_ASSIGN"

##  BOOLEAN TOKENS  ##

TT_GREATER_THAN = "GREATER_THAN"
TT_LESS_THAN = "LESS_THAN"
TT_GREATER_OR_EQ_TO = "GREATER_OR_EQ_TO"
TT_LESS_OR_EQ_TO = "LESS_OR_EQ_TO"
TT_EQ_TO = "EQ_TO"
TT_NOT_EQ_TO = "NOT_EQ_TO"
TT_TRUE = "TRUE"
TT_FALSE = "FALSE"
TT_NULL = "NULL"
COMP_OPS = (TT_GREATER_THAN, TT_LESS_THAN, TT_GREATER_OR_EQ_TO, TT_LESS_OR_EQ_TO, TT_EQ_TO, TT_NOT_EQ_TO)

##  LOGICAL OPERATIONS  ##

TT_AND = "AND"
TT_OR = "OR"
TT_NOT = "NOT"

##  BITWISE OPERATIONS  ##

TT_BIT_AND = "BIT_AND"
TT_BIT_OR = "BIT_OR"
TT_BIT_XOR = "BIT_XOR"
TT_BIT_NOT = "BIT_NOT"

##  VARIABLE TOKENS  ##

TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EQ = "EQ"
TT_DOUBLE_QUOTES = "DOUBLE_QUOTES"
TT_SINGLE_QUOTES = "SINGLE_QUOTES"

##  STRING TOKENS  ##

TT_STRING = "STRING"

##  SPECIAL OPERATORS  ##

TT_PLUS_PLUS = "PLUS_PLUS"
TT_MINUS_MINUS = "MINUS_MINUS"

##  MISC TOKENS ##

TT_NEWLINE = "NEWLINE"
TT_INDENT = "INDENT"
TT_COLON = "COLON"
TT_SEMI_COLON = "SEMI_COLON"
TT_EOF = "EOF"