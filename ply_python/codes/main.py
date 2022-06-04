#from __future__ import division
import ply.lex as lex
import ply.yacc as yacc

from node import node, num_node


def clear_text(textlines):
    lines=[]
    for line in textlines:
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)


# LEX for parsing Python

# Tokens
tokens = ('VARIABLE', 'NUMBER', 'PRINT')

literals = ['=', '+', '-', '*', '(', ')', '{', '}', '<', '>', ',']

# Define of tokens

def t_NUMBER(t):
    r'[0-9]+'
    return t


def t_PRINT(t):
    r'print'
    return t


def t_VARIABLE(t):
    r'[a-zA-Z]+'
    return t

t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()


# YACC for parsing Python

def simple_node(t, name):
    t[0] = node(name)
    for i in range(1, len(t)):
        t[0].add(node(t[i]))
    return t[0]

def p_program(t):
    '''program : statements'''
    if len(t) == 2:
        t[0] = node('[PROGRAM]')
        t[0].add(t[1])


def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t) == 3:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t) == 2:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])


def p_statement(t):
    ''' statement : assignment
                  | operation
                  | print'''
    if len(t) == 2:
        t[0] = node(['STATEMENT'])
        t[0].add(t[1])


def p_assignment(t):
    '''assignment : VARIABLE '=' NUMBER'''
    if len(t) == 4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(num_node(t[3]))


def p_operation(t):
    '''operation : VARIABLE '=' expr
    '''
    if len(t) == 4:
        t[0] = node('[OPERATION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])

"""expr -> expr + term | term
term -> term * factor | factor
factor -> id | (expr)"""

def p_expr(t):
    '''expr : expr '+' term
            | expr '-' term
            | term
    '''
    t[0] = node('[expr]')
    if(len(t) == 2):
        t[0].add(t[1])
    else:
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_term(t):
    '''term : term '*' factor
            | term '/' factor
            | factor
    '''
    t[0] = node('[term]')
    if(len(t) == 2):
        t[0].add(t[1])
    else:
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_factor(t):
    '''factor : VARIABLE
            | NUMBER
    '''
    t[0] = node('[factor]')
    # if(type(t[1]) == type(t[0])):
    #     print(type(t[1]))
    #     t[0].add(t[1])
    if(t[1].isdigit()):       #数字
        t[0].add(num_node(eval(t[1])))
    else:
        t[0].add(node(t[1]))

def p_print(t):
    '''print : PRINT '(' values ')'
    '''
    t[0] = node('[PRINT]')
    t[0].add(node(t[1]))
    t[0].add(node(t[2]))
    t[0].add(t[3])
    t[0].add(node(t[4]))

def p_values(t):
    '''values : VARIABLE
                | values ',' VARIABLE
    '''
    if(len(t) == 4):
        t[0] = node('[VARIABLES]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
    else:
        t[0] = node('[VARIABLE]')
        t[0].add(node(t[1]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()

v_table = {}  # variable table


def update_v_table(name, value):
    v_table[name] = value


def trans(node):
    for c in node.getchildren():
        trans(c)
    # Translation
    # Assignment
    if (node.getdata() == '[ASSIGNMENT]'):
        ''' statement : VARIABLE '=' NUMBER'''
        value = node.getchild(2).getvalue()
        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(), value)
        #print(v_table)
    # Operation
    elif node.getdata() == '[OPERATION]':
        '''operation : VARIABLE '=' expr
        '''
        tmpname = node.getchild(0).getdata()      #变量名
        tmpvalue = calcExpr(node.getchild(2))
        node.getchild(0).setvalue(tmpvalue)
        update_v_table(tmpname, tmpvalue)
    # Print
    elif node.getdata() == '[PRINT]':
        '''print : PRINT '(' values ')'
        '''
        tmpLst = []
        for i in node.getchildren():
            showPrintData(i, tmpLst)
        tmpLst.reverse()
        for i in tmpLst: print(v_table[i], end="  ")
        print()


def showPrintData(item, tmpLst) -> object:        # 辅助函数: 递归输出树的所有节点
    if(item.getdata() == '[VARIABLE]'):     #只有单个元素
        #print(item.getchild(0).getdata(), end="\t")
        tmpLst.append(item.getchild(0).getdata())
    elif(item.getdata() == '[VARIABLES]'):
        tmpLst.append(item.getchild(2).getdata())   #item是variables标签,variables 下有一个并列的variable需要输出来
        for i in item.getchildren():
            if(len(i.getchildren()) == 3):      #i是variables标签,variables 下有一个并列的variable需要输出来
                # print(i.getchild(2).getdata(), end="++")
                tmpLst.append(i.getchild(2).getdata())
            for res in i.getchildren():
                #print(res.getdata())
                showPrintData(res, tmpLst)


def calcExpr(node):     #计算一个根节点为expr的值,每个有三个子节点的expr子节点为[expr, 运算符, term]
    res = 0
    #print(type(node))
    length = len(node.getchildren())
    #print(length)
    if(length == 3):        #3个子节点的情况
        if(node.getchild(1).getdata() == '+'):
            res = calcExpr(node.getchild(0)) + getFromTerm(node.getchild(2))
            #print(res, 1111)
        elif(node.getchild(1).getdata() == '-'):
            res = calcExpr(node.getchild(0)) - getFromTerm(node.getchild(2))

    elif(length == 1):
        return v_table[node.getchild(0).getchild(0).getchild(0).getdata()]  #expr -> term -> factor -> c

    return res

def getFromTerm(node):        #传入参数是一个term节点
    if(str(node.getchild(0).getchild(0).getdata()).isdigit()):
        return (int)(node.getchild(0).getchild(0).getdata())

    return v_table[node.getchild(0).getchild(0).getdata()]
def put2str(node):
        global res
        if node:
            data = str(node._data)
            data = data.replace("[","").replace("]","").replace("'","")
            res += data
        if node._children:
            for i in node._children:
                res += "["
                put2str(i)
                res += "]"
if __name__ == '__main__':
    text = clear_text(open('example.py', 'r').readlines())
    lex.input(text)
    for tok in iter(lex.token, None):
        print(repr(tok.type), repr(tok.value))
    print("-----------------------------------------")
    res = ""
    # syntax parse
    root = yacc.parse(text)
    put2str(root)
    print("["+res+"]")
    print("-----------------------------------------")
    root.print_node(0)
    print("-----------------------------------------")
    # translation
    trans(root)
    #print()
    print(v_table)