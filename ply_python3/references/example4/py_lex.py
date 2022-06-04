#! /usr/bin/env python
#coding=utf-8
import ply.lex as lex

# LEX for parsing Python

# Tokens
tokens=('VARIABLE','NUMBER','IF','WHILE','PRINT','DEF','RETURN')

literals=['=','+','-','*','(',')','{','}','<','>'] 

#Define of tokens

def t_NUMBER(t):
    r'[0-9]+'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_IF(t):
    r'if'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DEF(t):
    r'def'
    return t

def t_RETURN(t):
    r'return'
    return t


def t_VARIABLE(t):
    r'[a-zA-Z]+'
    return t


# Ignored
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lex.lex()
from util import clear_text
text1=clear_text(open('binary_search.py','r').readlines())
lex.input(text1)
for tok in iter(lex.token, None):
    print(repr(tok.type), repr(tok.value))