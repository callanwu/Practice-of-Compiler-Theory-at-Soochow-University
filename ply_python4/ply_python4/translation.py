#! /usr/bin/env python
# coding=utf-8
from __future__ import division

# f_table = {}  # function table
# 目前认为f_table应该只放在class Tran里面，外面只放c_table
c_table = {}  # class table
# 搞清楚应该如何设置c_table, f_table
# 理解清楚设置它们的原理之后，再开始进行类相关操作的翻译
# 还可以稍微写一点代码进行翻译的尝试？


class Tran:

    def __init__(self):
        self.v_table = {}  # variable table
        # 考虑将f_table放到Tran类中
        # 为新定义的类都创建一个Tran，使得每个类都能有自己的函数
        self.f_table = {}  # function table

    def update_v_table(self, name, value):
        self.v_table[name] = value

    def update_f_table(self, name, value):
        self.f_table[name] = value

    def trans(self, node):

        # Translation

        # Assignment
        if node.getdata() == '[ASSIGNMENT]':
            '''assignment : VARIABLE '=' NUMBER
                          | VARIABLE '[' expression ']' '=' NUMBER
                          | VARIABLE '=' VARIABLE
                          | VARIABLE '=' VARIABLE '[' expression ']'
                          | self '=' VARIABLE
                          | VARIABLE '=' VARIABLE '(' expressions ')' '''
            if len(node.getchildren()) == 3:
                if node.getchild(0).getdata() == '[SELF]':                        # self '=' VARIABLE
                    value = self.v_table[node.getchild(2).getdata()]
                    # update v_table
                    self.trans(node.getchild(0))
                    # 注意这里访问类变量名用的是getvalue()
                    self.update_v_table(node.getchild(0).getvalue(), value)
                elif ord('0') <= ord(node.getchild(2).getdata()[0]) <= ord('9'):  # NUMBER
                    value = node.getchild(2).getvalue()
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                else:                                                             # VARIABLE
                    value = self.v_table[node.getchild(2).getdata()]
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)

            elif len(node.getchildren()) == 4:
                if node.getchild(2).getdata() == '=':  # NUMBER
                    arg = self.v_table[node.getchild(0).getdata()]
                    self.trans(node.getchild(1))
                    index = int(node.getchild(1).getvalue())
                    value = node.getchild(3).getvalue()
                    # update VARIABLE
                    arg[index] = value
                elif node.getchild(3).getdata() == '[EXPRESSION]':  # VARIABLE '[' expression ']'
                    arg1 = self.v_table[node.getchild(2).getdata()]
                    self.trans(node.getchild(3))
                    index = int(node.getchild(3).getvalue())
                    value = arg1[index]
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                elif node.getchild(3).getdata() == '[EXPRESSIONS]':  # VARIABLE '(' expressions ')'
                    variable = node.getchild(0).getdata()
                    cname = node.getchild(2).getdata()
                    self.trans(node.getchild(3))
                    vname1 = node.getchild(3).getvalue()

                    c = c_table[cname]
                    vname0, fnode = c.f_table['__init__']  # function_name : (variable_names, function)

                    for i in range(len(vname1)):
                        c.v_table[vname0[i]] = vname1[i]

                    c.trans(fnode)
                    self.update_v_table(variable, (cname, c))

        # Self
        elif node.getdata() == '[SELF]':
            '''self : SELF '.' VARIABLE'''
            if len(node.getchildren()) == 0:
                pass
            elif len(node.getchildren()) == 1:
                # 目前没有区分类成员变量和局部变量
                # 然而需要考虑区分，因为要实现__init__()函数
                # 初始化函数中两种变量是同名的，因此需要区分
                # 区分的代码实现应该放在该层（最底下）
                # ---
                # 考虑此处设置的值应该是类变量名还是类变量值
                # 目前考虑设置为类变量名
                # 在v_table中查询而获得值的操作应该放在类变量操作语句翻译中
                # 区分类成员变量和局部变量不需要在这里的前面添加'self.'
                # 否则在变量表中将查不到相应变量
                # 区分类成员变量和局部变量需要添加self.进行区分！！！
                value = 'self.' + node.getchild(0).getdata()
                node.setvalue(value)

        # Operation
        elif node.getdata() == '[OPERATION]':
            '''operation : VARIABLE '=' expression
                         | VARIABLE '+' '=' expression
                         | VARIABLE '-' '=' expression
                         | VARIABLE '[' expression ']' '=' expression
                         | self '=' expression'''
            if len(node.getchildren()) == 3:
                if node.getchild(0).getdata() == '[SELF]':    # self '=' expression
                    # Warning: 这样的检测方式可能会出错！
                    self.trans(node.getchild(0))
                    self.trans(node.getchild(2))
                    value = node.getchild(2).getvalue()
                    # update v_table
                    self.update_v_table(node.getchild(0).getvalue(), value)
                elif node.getchild(1).getdata()[0] == '=':    # VARIABLE '=' expression
                    self.trans(node.getchild(2))
                    value = node.getchild(2).getvalue()
                    # node.getchild(0).setvalue(value)
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                elif node.getchild(1).getdata()[1] == '=':  # '+=' or '-='
                    arg1 = self.v_table[node.getchild(0).getdata()]
                    self.trans(node.getchild(2))
                    arg2 = node.getchild(2).getvalue()
                    op = node.getchild(1).getdata()[0]
                    if op == '+':
                        value = arg1 + arg2
                    elif op == '-':
                        value = arg1 - arg2
                    # node.getchild(0).setvalue(value)
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)

            elif len(node.getchildren()) == 4:
                arg = self.v_table[node.getchild(0).getdata()]
                self.trans(node.getchild(1))
                index = int(node.getchild(1).getvalue())
                self.trans(node.getchild(3))
                value = node.getchild(3).getvalue()
                # update VARIABLE
                arg[index] = value

        # Expr
        elif node.getdata() == '[EXPRESSION]':
            '''expr : expression '+' term
                    | expression '-' term
                    | term'''
            if len(node.getchildren()) == 3:
                self.trans(node.getchild(0))
                arg0 = node.getchild(0).getvalue()
                self.trans(node.getchild(2))
                arg1 = node.getchild(2).getvalue()
                op = node.getchild(1).getdata()
                if op == '+':
                    value = arg0 + arg1
                elif op == '-':
                    value = arg0 - arg1
                node.setvalue(value)

            elif len(node.getchildren()) == 1:  # term
                self.trans(node.getchild(0))
                value = node.getchild(0).getvalue()
                node.setvalue(value)

        # Term
        elif node.getdata() == '[TERM]':
            '''term : term '*' factor
                    | term '/' factor
                    | factor'''
            if len(node.getchildren()) == 3:
                self.trans(node.getchild(0))
                arg0 = node.getchild(0).getvalue()
                self.trans(node.getchild(2))
                arg1 = node.getchild(2).getvalue()
                op = node.getchild(1).getdata()
                if op == '*':
                    value = arg0 + arg1
                elif op == '/':
                    value = arg0 - arg1
                node.setvalue(value)
            elif len(node.getchildren()) == 1:
                self.trans(node.getchild(0))
                value = node.getchild(0).getvalue()
                node.setvalue(value)

        # Factor
        elif node.getdata() == '[FACTOR]':
            '''factor : NUMBER
                      | VARIABLE
                      | STR
                      | self
                      | VARIABLE '[' expression ']'
                      | '(' expression ')' '''
            if len(node.getchildren()) == 1:
                if ord('0') <= ord(node.getchild(0).getdata()[0]) <= ord('9'):      # NUMBER
                    value = node.getchild(0).getvalue()
                    node.setvalue(value)
                elif node.getchild(0).getdata()[0] == "'":                         # STR
                    value = node.getchild(0).getdata()[1:-1]
                    node.setvalue(value)
                elif node.getchild(0).getdata() == '[SELF]':                        # self
                    self.trans(node.getchild(0))
                    value = self.v_table[node.getchild(0).getvalue()]
                    node.setvalue(value)
                elif node.getchild(0).getdata() == '[EXPRESSION]':                  # '(' expr ')'
                    self.trans(node.getchild(0))
                    value = node.getchild(0).getvalue()
                    node.setvalue(value)
                else:                                                               # VARIABLE
                    value = self.v_table[node.getchild(0).getdata()]
                    node.setvalue(value)

            elif len(node.getchildren()) == 2:
                arg = self.v_table[node.getchild(0).getdata()]
                self.trans(node.getchild(1))
                index = int(node.getchild(1).getvalue())
                value = arg[index]
                node.setvalue(value)

        # Print
        elif node.getdata() == '[PRINT]':
            '''print : PRINT '(' variables ')' '''
            self.trans(node.getchild(0))
            arg = node.getchild(0).getvalue()
            value = ''
            for i in range(len(arg)):
                value += str(self.v_table[arg[-1 - i]])
                value += ' '
            print(value)

        # Function
        elif node.getdata() == '[FUNCTION]':
            '''function : DEF VARIABLE '(' variables ')' '{' statements '}'
                        | DEF VARIABLE '(' SELF ')' '{' statements '}'
                        | DEF VARIABLE '(' SELF ',' variables ')' '{' statements '}' '''
            if node.getchild(1).getdata() == '[VARIABLES]':
                fname = node.getchild(0).getdata()
                self.trans(node.getchild(1))
                vname = node.getchild(1).getvalue()
                self.f_table[fname] = (vname, node.getchild(2))  # function_name : (variable_names, function)
            elif node.getchild(1).getdata() == '[SELF]':
                if len(node.getchildren()) == 3:
                    fname = node.getchild(0).getdata()
                    vname = []
                    self.f_table[fname] = (vname, node.getchild(2))
                elif len(node.getchildren()) == 4:
                    fname = node.getchild(0).getdata()
                    self.trans(node.getchild(2))
                    vname = node.getchild(2).getvalue()
                    self.f_table[fname] = (vname, node.getchild(3))

        # Run_function
        elif node.getdata() == '[RUN_FUNCTION]':
            '''run_function : VARIABLE '(' expressions ')'
                            | VARIABLE '.' VARIABLE '(' expressions ')' '''
            if len(node.getchildren()) == 2:
                fname = node.getchild(0).getdata()
                self.trans(node.getchild(1))
                vname1 = node.getchild(1).getvalue()

                vname0, fnode = self.f_table[fname]  # function_name : (variable_names, function)

                t = Tran()
                for i in range(len(vname1)):
                    t.v_table[vname0[i]] = vname1[i]

                value = t.trans(fnode)
                # (已解决)暂时不能设置为当前节点的值，因为会导致被误认为return接着往上传值
                # 解决方案：只取列表['[BREAK]', return_list]中的return_list作为当前节点值
                if isinstance(value, list):
                    node.setvalue(value[1])

                print(t.v_table)

            elif len(node.getchildren()) == 3:
                '''执行类函数是通过先访问变量，获得对应类代码，进入类中找到类函数，传递参数，最后才运行函数
                   例如a.add_score(60):
                   先通过变量a获得对应Student类的代码，进入类中获得add_score函数代码，再传递参数60进函数执行
                   因此在定义类函数的时候不需要将参数中的self放到参数表中'''
                variable = node.getchild(0).getdata()
                fname = node.getchild(1).getdata()
                self.trans(node.getchild(2))
                vname1 = node.getchild(2).getvalue()

                c = self.v_table[variable][1]
                vname0, fnode = c.f_table[fname]  # function_name : (variable_names, function)

                for i in range(len(vname1)):
                    c.v_table[vname0[i]] = vname1[i]

                value = c.trans(fnode)
                # (已解决)暂时不能设置为当前节点的值，因为会导致被误认为return接着往上传值
                # 解决方案：只取列表['[BREAK]', return_list]中的return_list作为当前节点值
                if isinstance(value, list):
                    node.setvalue(value[1])

                print(c.v_table)

        # Variables
        elif node.getdata() == '[VARIABLES]':
            '''variables :
                         | VARIABLE
                         | variables ',' VARIABLE
                         | self
                         | variables ',' self'''
            if len(node.getchildren()) == 1:
                if node.getchild(0).getdata() == '[NONE]':  # NONE
                    value = []
                    node.setvalue(value)
                elif node.getchild(0).getdata() == '[SELF]':  # self
                    self.trans(node.getchild(0))
                    value = [node.getchild(0).getvalue()]
                    # value = self.v_table[node.getchild(0).getdata()]
                    node.setvalue(value)
                else:                                       # VARIABLE
                    value = [node.getchild(0).getdata()]
                    # value = self.v_table[node.getchild(0).getdata()]
                    node.setvalue(value)

            elif len(node.getchildren()) == 2:
                if node.getchild(1).getdata() == '[SELF]':  # variables ',' self
                    self.trans(node.getchild(0))
                    value0 = node.getchild(0).getvalue()
                    self.trans(node.getchild(1))
                    value = [node.getchild(1).getvalue()]
                    value.extend(value0)
                    node.setvalue(value)
                else:                                       # variables ',' VARIABLE
                    self.trans(node.getchild(0))
                    value0 = node.getchild(0).getvalue()
                    value = [node.getchild(1).getdata()]
                    value.extend(value0)
                    node.setvalue(value)


        # Expression
        elif node.getdata() == '[EXPRESSIONS]':
            '''expressions :
                           | expression
                           | expressions ',' expression'''
            if len(node.getchildren()) == 1:
                if node.getchild(0).getdata() == '[NONE]':
                    value = []
                    node.setvalue(value)
                else:
                    self.trans(node.getchild(0))
                    value = [node.getchild(0).getvalue()]
                    node.setvalue(value)
            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(0))
                value0 = node.getchild(0).getvalue()
                self.trans(node.getchild(1))
                value = [node.getchild(1).getvalue()]
                value.extend(value0)
                node.setvalue(value)

        # Class
        elif node.getdata() == '[CLASS]':
            '''class : CLASS VARIABLE '{' statements '}' '''
            if len(node.getchildren()) == 2:
                cname = node.getchild(0).getdata()
                t = Tran()
                t.trans(node.getchild(1))
                c_table[cname] = t

        else:
            for c in node.getchildren():
                self.trans(c)

        return node.getvalue()
