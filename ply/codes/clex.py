import ply.lex as lex
#Tokens
tokens = (
    'IDENTIFIER', 'NUMBER', 'ASSIGN', 'ADDRESS','LSHIFT','RSHIFT','LT', 'GT',
    'SELF_PLUS', 'SELF_MINUS', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GTE', 'LTE','LL_BRACKET', 'RL_BRACKET', 'LB_BRACKET',
    'RB_BRACKET', 'LM_BRACKET', 'RM_BRACKET', 'COMMA', 'DOUBLE_QUOTE','SEMICOLON', 'SHARP','INCLUDE', 'INT', 'FLOAT',
    'CHAR', 'DOUBLE', 'FOR', 'IF', 'ELSE', 'WHILE', 'DO', 'RETURN','STRING_LITERAL'
)
reserved = {
    'include': 'INCLUDE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'return': 'RETURN'
}
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_ASSIGN = r'='
t_ADDRESS = r'&'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LT = r'<'
t_GT = r'>'
t_SELF_PLUS = r'\+\+'
t_SELF_MINUS = r'--'
t_LTE = r'<='
t_GTE = r'>='

t_LL_BRACKET = r'\('
t_RL_BRACKET = r'\)'
t_LB_BRACKET = r'\{'
t_RB_BRACKET = r'}'
t_LM_BRACKET = r'\['
t_RM_BRACKET = r']'
t_COMMA = r','
t_DOUBLE_QUOTE = r'"'
t_SEMICOLON = r';'
t_SHARP = r'\#'

t_STRING_LITERAL = r'"[^"]*"'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

with open("prog.txt","r",encoding= "utf-8") as x:
    str = x.read()
lexer.input(str)
while True:
    tok = lexer.token()
    if not tok: break
    print(tok)