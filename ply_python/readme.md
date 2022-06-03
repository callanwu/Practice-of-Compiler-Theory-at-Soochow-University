| 院系       | 年级专业 | 姓名   | 学号       | 实验日期  |
| ---------- | -------- | ------ | ---------- | --------- |
| 计算机学院 | 2019计科 | 吴家隆 | 1915404063 | 2021.11.8 |

*编程语言：**python3.9***

------

[TOC]

# 实验内容

- 利用PLY实现简单的Python程序的解析

  1.示例程序位于example/

  2.需要进行解析的文件为**example.py**

  要解析的内容为：

  ```python
  a=1
  b=2
  c=a+b
  d=c-1+a
  print(c)
  print(a,b,c)
  ```

  3.需要完成以下内容的解析

   *赋值语句*

   *完整的四则运算*

   *print语句*

  四则运算的无二义性下文法大致如下：
  $$
  expr -> expr + term | term\\
  
  term -> term * factor | factor\\ 
  
  factor -> id | (expr)
  $$
  （***\*不需要消除二义性\****）

  4.解析结果以语法树的形式呈现

- 编程实现语法制导翻译

  1.语法树上每个节点有一个属性value保存节点的值

  2.设置一个变量表保存每个变量的值

  3.基于深度优先遍历获取整个语法树的分析结果

# 实验步骤

## 使用lex进行序列标记

首先获取要解析的文本

```python
import ply.lex as lex
def clear_text(textlines):
    lines=[]
    for line in textlines:
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)
```

在本次实验中要识别的tokens包括以下

```python
tokens = ('VARIABLE', 'NUMBER', 'PRINT')

literals = ['=', '+', '-', '*', '(', ')', '{', '}', '<', '>', ',']
```

ply使用"t_"开头的变量来表示规则。如果变量是一个字符串，那么它被解释为一个正则表达式，匹配值是标记的值。 如果变量是函数，则其文档字符串包含模式，并使用匹配的标记调用该函数。该函数可以自由地修改序列或返回一个新的序列来代替它的位置。 如果没有返回任何内容，则忽略匹配。 通常该函数只更改“value”属性，它最初是匹配的文本。

```python
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
```

对文本进行测试，输出每一个识别到的token

```python
text = clear_text(open('0.py', 'r').readlines())
lex.input(text)
for tok in iter(lex.token, None):
    print(repr(tok.type), repr(tok.value))
```

结果如下：

![image-20211128225315457](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211128225315457.png)

## 使用yacc进行语法分析

PLY 的解析器适用于lex解析出的序列标记。 它使用 BNF 语法来描述这些标记是如何组装的。 

对node进行定义

```python
class node:
    def __init__(self, data):
        self._data = data
        self._children = []
        self._value=None
    def getdata(self):
        return self._data
    def setvalue(self,value):
        self._value=value
    def getvalue(self):
        return self._value
    def getchild(self,i):
        return self._children[i]
    def getchildren(self):
        return self._children
    def add(self, node):
        self._children.append(node)
    def print_node(self, prefix):
        print ('  '*prefix,'+',self._data)
        for child in self._children:
            child.print_node(prefix+1)
def num_node(data):
    t=node(data)
    t.setvalue(float(data))
    return t
```

四则运算的无二义性下文法大致如下
$$
expr -> expr + term | term\\

term -> term * factor | factor\\ 

factor -> id | (expr)
$$
定义文法

```python
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
```

## 实行语法制导翻译

定义变量存储字典结构和更新函数

```python
v_table = {}  # variable table
def update_v_table(name, value):
    v_table[name] = value
```

翻译函数

```python
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
```

其他辅助函数

```python
def showPrintData(item, tmpLst) : #辅助函数: 递归输出树的所有节点
    if(item.getdata() == '[VARIABLE]'): #只有单个元素
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
```

将node函数递归输出为字符串语法树形式便于在http://mshang.ca/syntree上检查结果

```python
def put2str(node):
        global res
        if node:
            data = str(node._data)
            data = data.replace("[","").replace("]","").replace("/'","")
            res += data
        if node._children:
            for i in node._children:
                res += "["
                put2str(i)
                res += "]"
```

# 实验结果

## 主程序代码

```python
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
```

## 结果

输出结果总共为四部分

第一部分为识别的序列，在实验步骤中使用lex进行序列标记已经展示结果

第二部分为字符串形式的语法树 

结果如下：

\[PROGRAM\[STATEMENTS\[STATEMENTS\[STATEMENTS\[STATEMENTS\[STATEMENTS\[STATEMENTS\[STATEMENT\[ASSIGNMENT\[a]\[=]\[1]]]]\[STATEMENT\[ASSIGNMENT\[b]\[=]\[2]]]]\[STATEMENT\[OPERATION\[c]\[=]\[expr\[expr\[term\[factor\[a]]]]\[+]\[term\[factor\[b]]]]]]]\[STATEMENT\[OPERATION\[d][=]\[expr\[expr\[expr\[term\[factor\[c]]]]\[-]\[term\[factor\[1]]]]\[+]\[term\[factor\[a]]]]]]]\[STATEMENT\[PRINT\[print]\[(]\[VARIABLE\[c]]\[)]]]]\[STATEMENT\[PRINT\[print]\[(]\[VARIABLES\[VARIABLES\[VARIABLE\[a]]\[,]\[b]]\[,]\[c]][)]]]]]

**生成语法树如下：**

![img](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABjkAAAGrCAYAAACSdPU6AAAAAXNSR0IArs4c6QAAIABJREFUeF7s3Q/8FVWd//EP/kNQvqioqCABpmhkZLn5B8z+WKi7qYWiG2i6aG7qWprW7pao+KvdUqNYtVApU1Ex8V8tBpVpgkJbJpp/0ARCUDBQAQX/83t85vaB853vOTNz751779x7X/fx4KHwvTNz5jnznTlz3nPO6bZhw4YNwgcBBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQaDKBboQcTXbEKC4CCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAghEAoQcnAgIIIAAAggggAACCCCAAAIIIIAAAggggAACCCDQlAKEHE152Cg0AggggAACCCCAAAIIIIAAAggggAACCCCAAAIIEHJwDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggggEBTChByNOVho9AIIIAAAggggAACCCCAAAIIIIAAAggggAACCCBAyME5gAACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAk0pQMjRlIeNQiOAAAIIIIAAAggggAACCCCAAAIIIIAAAggggAAhB+cAAggggAACCCCAAAIIIIAAAggggAACCCCAAAIINKUAIUdTHjYKjQACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAoQcnAMIIIAAAggggAACCCCAAAIIIIAAAggggAACCCDQlAKEHE152Cg0AggggAACCCCAAAIIIIAAAggggAACCCCAAAIIEHJwDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggggEBTChByNOVho9AIIIAAAggggAACCCCAAAIIIIAAAggggAACCCBAyME5gAACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAk0pQMjRlIeNQiOAAAIIIIAAAggggAACCCCAAAIIIIAAAggggAAhB+cAAggggAACCCCAAAIIIIAAAgkCCxaIHH+8yPz5nb90+ukiEyeK9OhR+vepU0XGju26ohtvFBkzxr8B3zITJohccEG4QKtWldY3c+am78TLkrXM8a1YeWbPFhk+vGsZ7OcjR5b2t08ffzlt+7vskvw9TjwEEEAAAQQQQKBaAUKOagVZHgEEEEAAAQQQQAABBBBAoKUFrMH+/PM3hRUWNAwcuCno0Eb/Sy8VmTZN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yiuvvCJvvvlmdEyK1iNFGwrsOGiQsuuuu8oHP/jBKET59Kc/3eyHgvIjgAACCCCAQIsJEHK02AFldxCogQAhRw1QWSUCCCCAAAIIIPCd73xHfvazn0U9BzSAeOuttyKUojV425HSh0f9owFEnz595MMf/rBcfPHF8oEPfICDWRCBOXPmyHXXXSd/+tOfZNmyZdF59cYbb0TDe/nOq3q88Rga1kv/XXvU6PnU0dEh/fv3l4985CMybty4KFDhgwACCCCAAAIIZBUg5MgqxfcQaF8BQo72PfbsOQIIIIAAAm0rcMUVV8hNN90kf/nLX2TNmjVNFUBsv/32MmzYMPnqV78qn/jEJ9r2GLLjtRG44447onDusccekxUrVshrr70W9UixeVLiW21kkKK9UWxosu22204GDBggI0aMkK9//euif+eDAAIIIIAAAq0hQMjRGseRvUCglgKEHLXUZd0IIIAAAgggULbA9ddfL1OmTJGnnnoqCiC0gVU/Re8BsdVWW0UNq+973/vkrLPOkmOOOabsfWcBBNpBQOdH+cUvfiELFiyQlStXRkGKDutV1CBFJ5rv0aOHaMD43ve+Vw477DD52te+1g6Hin1EAAEEEECgEAKEHIU4DBQCgUILEHIU+vBQOAQQQAABBIolcOedd4r2gnjiiSc2zjmg4UMjAwgVShoyR3+uAUTv3r1lyJAh0XA5J510UrFgKQ0CCOQq8N3vfld+85vfyDPPPBNdq9atW1foieY1SNH5UXSouL333lv+6Z/+SU477bRcTVgZAggggAACzSpAyNGsR45yI1A/AUKO+lmzJQQQQAABBGoqcO+998rll18u8+fPl5dffjkaqz8pgNDCNHKoGQsmttxyy2jMfn1DWic+1l4QfBBAAIEiC2hwovPuzJ49W5YsWRIFKa+//nrUG+Xdd9/1Fr2R11sd1kvD3p49e8ouu+wi++67rxx77LHyuc99rsjMlA0BBBBAAIFIgJCDEwEBBNIECDnShPg5AggggAACOQg8+uijMn78eHn44Ydl1apVTRVAbLvttjJw4EA57rjjorHu+SCAAAII1F7gkUceiYbu+/3vfx9NNL969erEiea1RI0KUtyJ5vWesdtuu8l+++0nJ598cjRPCh8EEEAAAQSqESDkqEaPZRFoDwFCjvY4zuwlAggggECCgE6u++Uvf1nmzZsn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8Y+On6oVzVBPk/gE5O5Dv1tJDc0fYo0CNlloaPJP22ffvCVW8XbfznT3wzc+uK9yzamKAAIIIIBAOwuUc7+M1wuyvEDg6zmRFnKMHdv1iLh1Ad9LDrYdHRrFbSwLhRwzZ3bdhtUTknpyuA13hBzt/JvDviNQfIFqQw67rtp1b+XKrvNrJG3D7hGTJ4sQchT/fKGECOQpQMiRpybrQgABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAgboJEHLUjZoNIYAAAggggAACCCCAAAIIIIAAAggggAACCCCAQJ4ChBx5arIuBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQqJsAIUfdqNkQAggggAACCCCAAAIIIIAAAggggAACCCCAAAII5ClAyJGnJutCAAEEEMhd4N5775VPfOITua+XFSKAAAIIIIAAAggggAACCBRf4C9/+Yu8973vLX5BKSECCDRMgJCjYfRsGAEEEGhtgR/+8IfyH//xH/Laa6/Ju+++G+3shg0bOu10/O/ViHTr1q3T4vb3Hj16yJ577inf/e535VOf+lQ1m2BZBBBAAAEEEGhDAa1T5FlnaUNCdhkBBNpE4J577pFbb71V/vSnP8mKFStk7dq18uabb8o777xTk2dBvT7rn8022yz6s8UWW8iWW24pW221lXTv3l222Wab6E/v3r1l++23l5133ll23XVX2X333WWPPfaQvfbaS3bZZZc2OTrsJgKtLUDI0drHl71DAAEEyhYYN26c3HzzzVFl1B7oaxVOxIMJLaz9m1ZStSJ6yy23yEUXXSTz58+XV1991RuW+AKUsnf87wuEwhKtJPfv31/OPvtsOeussypdPcshgAACCCCAQJMJEHI02QGjuAggkCiwZs0amThxovzud7+TRYsWycsvvyzr16+Xt99+e+PLae4KGhXy2nOZPhM+9NBD0Utr999/v7zwwgtRebVcvrLZcu5/7btZ98XCEwtQNt98840Bij4Xbr311lF40qtXL9luu+1kxx13lL59+0q/fv3kPe95T9Tr5H3ve1+0DB8EEKiPACFHfZzZCgIIIFBzgY9//OMyZ86cqGIaqvBlrdSlFTYUTlhlUMMArTAX7XP00UdHRqtXr97oFC9jrY20orvTTjvJCSecIJdddlnRiCgPAggggAACCMQECDk4JRBAoBEC06dPF/3z2GOP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+veePXvKqFGj5LrrrquskCyFAAIIIFATAeqfNWFlpQgg0MYCI0aMkLlz58o777zTRUHbwEaOHCl33313Gwux6wi0lgAhRwsdzy233HLjxTsUaGjleZdddpHly5dHDShJwcfmm28ub731VgsJsSsIZBPgITObE99CAIGwQO/eveW1117rcq+tJKzQrbiBhf6//unevbusW7dO3vOe98jSpUtrtq3NNttMBg8eLAsWLOCQI4AAAgjUSID6Z41gWS0CCLSFgNa7+/fvL6tXr+7SzmUv+uh3dtxxR1m1apX3O7vuuqv85S9/kR49erSFGTuJQKsJEHI06RHVACIUUlhjiDZKvP3225n3cIsttvC+PWorsEYVXwqeeSN8EYEmEOAhswkOEkVEoE4CRxxxhPz617+uae8KvV/vueee8sQTT5S9V5Ver4455hj51a9+FfXijAcvlQQxvl4j2267rYwbN06+973vlb1fLIAAAgi0m0Cl1/N2c2J/EUAAARX4zGc+I/fcc4+3l4bWrYcOHSqPPvpoJyzfdfbQQw+VBx980Nt2pi8UnXDCCfSA5pRDoEkECDkKfqAGDRokS5YsaVivi6y9Q3Sej6effrrgmhQPgWwCPGRmc+JbCDSbQJ8+fTa+3eU25FfSqK/77utdoS8hXH/99XL88cfXhaee16uHHnooGurqxRdfrFmvEX3hYu+995b58+fXxY+NIIAAAkURqOf1vCj7TDkQQACBrAI777yzrFy50tsDQ8OISZMmyWmnnZa4uizX2VtvvVW++MUvypo1a7psS8MT7UG9cOHCrMXmewggUEcBQo46YqdtSscEtJ4XScNN2fAUaeur1c979eoVDY+RNtyVNlTYfCC1KgvrRaAWAlkqP7XYLutEAIFsAieffLLcdNNN3iEaKwksfL0Q9CFmt912k7/+9a/ZCtWgbzXD9UonRteA5I033si914gdOx0e7Otf/3r0hw8CCCDQjALNcD1vRlfKjAACzSfwhS98QW6++Wbv8Ol6rdSXbJ955pmyd6zS6+z+++8fvYDjGylF57s7/fTT6blc9tFgAQTyFyDkyN800xpbcWioWgyhlQmTLyGQs0CllZ+ci8HqEGgLgb59+24cF7cWvSsUUe9P3/jGN+TCCy9sOdNWvV5NnTpVzj333OiNPf3U4tzQ3qrDhg2TefPmtdx5wQ4hgEDzCbTq9bz5jgQlRgCBegvoXBrPP/+8d85YfRn4vPPOk29961tVFyuv6+xll10mF198sbz66qtdyqQvSg0ZMqSiYWir3kFWgECbCxBy1OEEaOfG/1YMc+pwyrCJBgvkVflp8G6weQTqKnDRRRfJt7/97dx6V2jhfcNB6WSBy5cvr+u+FXljXK86H50DDzxQHnnkkejNv1oEI7o1HfZs4sSJMmbMmCKfGpQNAQSaTIDreZMdMIqLAAIVCeiLRxoS+Eb90Oug9qReunRpRetOW6iW19n3ve99smDBgmgev/hH56nTl600rOGDAAK1EyDkyNFWu6nZUAyh4aZ0c+0+jFPWYbnUc+3atTkeIVaFQDaBWlZ+spWAbyHQWIEBAwZsfJsq70mpLbjQFwC0kfgnP/lJY3e2ybfO9ar6A/jd735XvvOd78grr7wSrazacMQ3/JnWfQ466CC59957qy8wa0AAgZYU4HrekoeVnUKg7QX23HNPefbZZ729NLRX7ec///m6Texdz+vsV7/6VfnRj34UDfUe/2iboPYm/sMf/tD25wcACOQpQMhRoWbWCbm1oWjRokUVbqV9Fttrr7023viSAiJtFNO3M/kgUEuBelZ+arkfrBuBadOmyUknnRT1rojPo1TJ3BUq6utdofMhrFq1CvAGCHC9agD63zepD6dPPfVUND5ztcFI6HdLJ9mcPn16FJDwQQCB1hbget7ax5e9Q6AdBK6++mr58pe/7J2HTa9x2iP7xRdfbBhFo6+zgwcPjub7i/f20HJ1dHTI5MmT5fjjj2+YDxtGoNkFCDkyHEGGXMqAVKOvtPNQXzUiZbUZBBpd+clQRL7ShgLaBVon2NNKcd69K6yBVceQPeyww+See+5pQ+Hm3GWuV8113HSekSlTpkRjONfq93jrrbeWT33qU3LnnXc2Fw6lRaDNBbiet/kJwO4j0IQCH/jAB+Txxx/3DtGkbTlHHHGE/PznPy/MnhXtOnvyySfLLbfcEoVC8Y+2Qx588MFy//33F8aPgiBQdAFCDucIHXPMMdEFOP62q33FHWKD3gSNO7Wz9qIZPXq03HzzzY0rKFtuWoGiVX6aFpKCewWefPJJ2X///b3DG+bZu2KbbbaR1atXcxRaXIDrVYsf4L/vnk5guXDhwi4hZ57XDJ3088EHH4zGwuaDAAL1F+B6Xn9ztogAAtkFfve738mRRx4ZDb8Ur3/o9Ut7dutcGvoMUtRP0a+z69evl/e+973ywgsveI11Xjh9GU2fJfkggEBXAUIOxyQ+BIf+SMdQfv311zl3Ci6gby3axFV5DBlR8N2leDUWKHrlp8a7z+prLBAfr9/dnG8sf+1d8eEPf1jmzp1b45Kx+mYU4HrVjEetPmU+5ZRT5LbbbvM2RiSFI5UGJ/XZK7aCQOsKcD1v3WPLniHQCgLuc4r20jjwwANl9uzZTbVrzXidPeqoo2TmzJmdJmqnrtZUpx2FraMAIYeDPXbsWLnxxhvryM+mailw2mmnyTXXXFPLTbBuBBBAoGwB7cmxzz77lL0cCyCAAAK1Fnj++efpyVFrZNaPAAIIIIBAEwo88MADcsghhzRhyVuryH/84x+jF+D4IIBAVwFCDs4KBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQaEoBQo6mPGwUGgEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBAg5OAcQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEECgKQUIOZrysFFoBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQIOTgHEAAAQQQQKABAvOWzZORN4yUcw86V8YfOr4BJWCTCCCAAAIIIIAAAggggAACRRXgmbGoR4ZyFVEg15BjwQKR448XmT+/tKvDholMmyYyZIjInDkiI0aECdzv6rdWrRIZM0Zk4ECRiRNFevQoLZt1Pfpdtyy2ZXc7bnlnz5b/3979wGpd3Ycf/6BWhJRLVmzocpGA3Ya6PzjTDQW72mXxEtK0XS4TN2ALAWVV10WjWzcVFOdi4681tMWOVbpsQCMGXOcSwiWL/ScIW0NxU6uZtQy4mXXYhWuDgiK/fO6zc+95zj3n++d5vs/zfM/3+36SpnKf759zXud8z/f5ns/3nCOLFvnT99ZbIrffLrJ5s4i93QMPiKzz9Ett2CBy773jeRgaEtm2rZEf96PH0Dxt3y5y4oQ/zfY+9vldi4GBxnFmzOhcVUs6Z8jDpGbt2uay1LSuWNFsaluHcmF8zf7udvZ5TJrcc7v7mHzZ25k6qOXnfkw5pNUhkx/dX+vxoUP5roPOlWRvjuwrM1OedopC9m4dd9sc33Ueqieha1KPYcrtyJHmayp0Pt81al/b7jXZikOWNqST135vaky1z8oP1mqXL7lDAAEEEEAAAQQQQKAVAdM/EeqncvsZ3P6y0LNj6HnW11+S9Dwbel628+rrH3L7/XT7pPPo91n6fVoxjmUfnhljKSnSWQaBwoIcvg5r7ah89FGRO+8cD1LYHYj9/Y1ggO9jN2RpDbvvOKbxvusuf3BBz2m2uewykV/+5XBaQh3ZaY2x3VEbCkAkHUO/Gx5uDgwYK/1u167xIJLJz+7djYBMJz55zmnMNm3yB49sm6QAhN7cb721OZ8mb1pHHn7Y/53tpPVHP1/6UiPg5vv4giEmjRr8CtVTu2748hH68ZH1OuhEOfbimMbS/EgxnfGhH0c+e9+2Wa5zXz0xPxpDP/7sYF5SMCTtGjUBTJPfVh000NZKG9KLsuac2QX4wZrdii0RQAABBBBAAAEEEKiLQFpfhO852H5hNPTs6Nsv9IJxUl9Vludl3/6+PqW0frUs/T5Vrhc8M1a5dMlb0QKFBDlMY5oUtLATnra9+f7HPxb5yU9EBgf9ncxJx8nS+Wm2ueWWRsAg1Amuje6bb4rs3Stid9qnNcbmZnHuXDgfrQQ5zHFXrgwHcIquKHnPmRbkMDdFHW3z0kvhQEURQQ4NFPX1iUyb5q9Hmtb77hOZPr2hZkYOpf2w0G3tQJmOWnI7xAlyhEdFmDrqMwrZu9d1lus89KMoLUChbcLMmSJz5/oDjZr+tGPYQY60t12SHFptQ4puBzhesQL8YC3Wk6MhgAACCCCAAAIIIFAVgbSZAdwXPt2+Cd/LwqHnZ1+/S1pfVdrzsm9/Xz9RWr8aQQ6mOK7KNU0+Oi9QSJAjS2dwniCH3fDpdDFbt/qnYSoqyKE3B22gP/rRiUED0wF+222NEQWtBDl0JMCll06cmsl0krpvexurUAdqlo7doqtO3nOmBTlM3u65R2TNGpFQwKaoIIcGyr7wBX890rRo+bz6avPImSz12nbR/d3RNQQ5xqeYS5oSzh2OG7J3g21Z6mVSkMN37dnn0OnyQiOJ8gY50oYc6/GSHFppQ4puBzheewI37rxRdrywY/Qgs6fPli8OfFFW/9Nq1uRoj5W9EUDAI+BOL2pPDRkamasvnpgXi0yHg74A9NnPipipO91Rq+Y83/ymyFe/2tgu6X5PYSGAgF9g1w93ydInlo59ufOGnTJ4+SBcCCBQY4HQ7AOhfjB97tW+s8ceE/mrvxLJM+OJ71k1FHzI+rzs2z/PeUzRE+QYD3Koyfpvr+deUeN2gawnCxQS5AitWRE6ddpIDrsxNOtU+KadKirIoYEL02Hprmmh/9bO6xtuaKyX0WqQQ6fs0mmk3Dn+06LjvumqzE3ltdeSp2oqsvLnPWdSkMPtmE4bBtnudFVq+OCDInffPTGQpfnSAJaO5HjiifaCHIsXT1xHhiBHI7AUClSaOuoGL9JGcpjrsNUgR1K52D+iLr64UaahKcvyjORo16GVNqTINoBjtS4wcnpElmxfIsdGjsn+1fulf1q/DL85LAu3LJSjJ4/K/dfdz8LjrfOyJwIIOAJpLw6401Lo7maqUzOa1UzjaU93Ye659ghrcy7fHNsUDAIIZBPQlyD2vLJHhlYOyYL+BaM7bTy4UVZduUr6JvdlOwhbIYBA5QRCz6y+vhb3+TkUGAg9P/u2D/XTZH1edvcP9d8xkiO56prR/ydPn2x6bvTdOyp3EZAhBHIKFBLk0HNmWX/CpC0pOOGbFinUkZglyGEWQTfntt9As28Oui6Hdmbq2gtmAXK7A1z39wU5fAuPmzfY3BuN7+GwlSCHpiVtLYic9SDT5nnOmRTkcDt7k7ZNG8mhC5e7H3vKKLvuPPmkyPe+N3Hxcw1iabm79SzL4tfujwT3bQuCHMlTOoXaBF+QwzdXqF0n7XpgX+e+H2yhH32+NiUpOJEnyJG0bVaHvG1IpgubjTouYN7OdN/KNH8nyNHxIqjUCTZ8Z0PTG1xu5qhPlSru3JkJvSTg3svsQIiexH2hxDfaQ7dzf5elrXGVOwPsgEDNBEK/EWrGQHYRQCAgkDX44N6fQ9ON+4IcocCHr68qz/OyeWHCzppvrZAsQY60fp8qVyAT5Fj8C4vl8aWPj2XVvEg3q29W09+rbEHeEEgTKCzIYU5kLxgeWlA6KTihjbM2cvaIilBHd5YgR5aFx81b4XpOuxNcz6tvoOtbbUePtjeSwyxc7d6kWg1yGG/7xmFPRZBW8O18n+WcocCFKTN7arC0+lDESA4tw1OnmgNZ5rw6VZYGtkJBjiwLj9v1zC7TqVMnvh0Z6tBup0zKvG87nftmegyTP7eOZx3J4f4oCl0rejydlsNenycpCNftIIc65GlDylwv6pQ2fcvm2ePPjo3iMHlnTY461QLyikB3BEJTI4bm2n7xxUa6PvGJ5ilbQ79P3XtilqkYu5NzzoJAnAIauN7ygy0TfiPEmRtSjQACRQu4z7uhlxn0vq0f0++k/+17VvW9JBhapNz3WyDP87Jvf9NfaE9tmSXI4a4/UrRzmY+X9Myoz5nHR47L7uW7GflX5kIkbV0TKDzIYVJuGi9fg5nUqe2L9oY6OIsOctgN9uzZjc5p0xnv6+hMa4x9NyD3zf7/9/8ab8W502SFbkqhmmHcQoGlTtSopHOGOoZDb95r+nxTHaSN5Ei72bk3dvvm7wbUigpy2OVuphjS/JkpIExZpE3b1oky68Ux252myf6h5qY/a5DDrie+H1Zuu+Vz8l1beYIcRTnkaUN6Ud6cc6JA6McnQQ5qCwIIFC3grsXhHt/uVDD30KuvnvgbJS3IYV7uIMhRdAlyvLoJ0EFVtxInvwjkE3Cf/Q4dmjj6MjQDhTmT795v7uO+mQLMfklBiizPy6HfEr4+mlCfmJ6HNTnCC4+HXqbLV8vYGoHqCHQsyKFEoQefUOdunimO9PhFBzn0mKYTXNfg0HUavvIVkRkzxqeHanVNDruj1u6Y1amSighy9KrxT5vr0fYyvknrjLgLkBcd5LADWboGhy7mrNOU+dKWd+Fxcxy77u/d21iMXD91DXJk6QBJmz881OS2EuQwZe1ed6EhvaY8fSOK8gQ5inTI2oZU51YVd04YyRF3+ZUt9UxXVbYSKVd6kn43uSm1Xyyyp/oM3Sf174zkKFd5k5r4Beigir8MyQECnRaw+1zcdURNP5BvDUxff5nv+Tn0nOoGKfI+LycFOexn8bSXhwlyJAc5GMnR6SuQ48ck0NEgR9qURf39zcPpkt509jXGnQhymLf758wRsdNX1EgOUzlMQz1zpsikSe2P5EjqiO1khQw9TPu8km6KoQfqooMcps709Ynoei32tERFjeQw3no8DXBoGc+dW98gR9K6JGrl+z5LgMnubEmals73o8h3/KS6ljQs2Be089Xnoh2ytCGdvPY5dnYB7ZT+4rNfbFpQVPc2ndWsoZDdki0RQCBZIO23ltnbvud9//si7shY8xtmxw6RefPGz5m0todZ044yQgCB7AKsyZHdii0RqKuAubfrLCk6nbP9Ymja7BDus3Ce9Tfc4EPe52Vf8ML3TEyQI7lmh9bkGH5zWBZuWSirf321rPvYurpeHuQbgSaBQoIc9gLd9oNQqLHyNcRpjbOvMexEkMMc88ABEfvBruggR5aF2kNviWta7FEmoY7iIut63nP6vNLeLvS9QVB0kENNzHncdRmKDnLYU3P5pjpKq/NFll+vj2Xqu6bDnpot7e9J66G0E+Qw6dC1Oszw3aRRGbq9rz3LM5JDj5GW35CPzyFLG9Lrcuf8DQHzA1T/e//q/dI/rV/Mj9WTp08KQQ5qCgIIFCngm5ZRf/s8/XTj5SI3cG/+rS/4mFGnvilJze8ne9RHllGKReaNYyFQNQGzcOzzrz/f9DLExoMbZdWVq5hjvWoFTn4QaFHA3JfdKb6TZkPxPS+Hghy+aavc59+8z8tJ0131Yk0ODSqv/qfVE148a7FIurab/dy484adMnj5oJh7x7GRY6zp1LWS4EQxCBQS5LA77+yFgkOL+/o6d7M8JLlR6CxBDn1b3/2YBjV0Q3AXILdvDu50Ves8AVPToW0Wug511Jo8Jy30FHpL3Le2hTvVQNEVMM85Xdu0t9jtOmR7pQU53AWl9Ti2p+9GbB7m9UHffuswFORwF7/WcxjrtOmSTEdD3YMcpi4aD7tu+upt3pEcSdd5aHirHdB86CGRz31OJGlEiK+NyhvkKNohrQ0pug3geK0LmEDH0ZNHRw+y6JJFsv4bqb4fAAAgAElEQVS69fJ7T/ye3HHNHbx90zoteyKAgEfAvd+a3+Tm3nfkSPNLB24Aw3RMfOYzIp/+9PgJ3Ht2lt/vFBACCKQL6LRVO17YMbah6chK35MtEECgDgLmfuv2K6SNgnD7YY4eFVm2zP/ca347mHu9fewTJ8L7GX/3N4E9LabZxrcOq2873d7k9cknRdL6fbLUAR1Fv/dHe6NbpNsEOdZctUYOHD8g+47tG83u7OmzCXBkKXi2qZVAYUGOWqmRWQQQQAABBBBAAAEEKiqQ1mlS0WyTLQQQQAABBBCooIAZ+XD9h6/n5bIKli9ZQsAIEOSgLiCAAAIIIIAAAggggMCYAEEOKgMCCCCAAAIIVEVAR9Uv3rZYHvvkY7Kgf0FVskU+EEDAESDIQZVAAAEEEEAAAQQQQAABghzUAQQQQAABBBBAAAEEEIhSgCBHlMVGohFAAAEEEEAAAQQQ6IwAIzk648pREUAAAQQQQAABBBBAoDMCBDk648pREUAgYoFly5bJjh3jiz9GnBWSjgACCCCAQGaBhx56SD73uc9l3p4NEUAAAQQQQAABBBBAAIEyCBDksEph0qRJcu7cuTKUC2koQIDyLACx4oe44IIL5L333hvNZdK1r3VJP+edd548+uijcvPNN1dchuwhgAACCFRZ4MILL5R333038/3voosuklOnTlWZhLwhgAACCCCAQIIA/StUDwQQKLsAQQ6CHGWvoy2nj5twy3SV2rGVQMbZs2fl/PPPzx0A+Zu/+RtZs2ZNpfzIDAIIIIBAnAIzZ86UEydOjAbxswby897/9LfWrFmz5L/+67/iRCLVCCCAAAIIIJBJgP6VTExshAACPRQgyEGQo4fVr7On5ibcWd8yHf1973ufaMeMfrJ05Gjd+J3f+R0ZGhryZiOp7nzjG9+QP/zDP8wdANm8ebOsXr26TGykBQEEEEAgcoHf/d3flaeeemrs3he6B5oRifr/V111lfzbv/1b7vvfxz/+cfnud7+b61x/8Ad/IFu3bo1cmeQjgAACCCCAAP0r1AEEECi7AEEOghxlr6Mtp4+bcMt0pdxRAxk6tVTWN1K1/OfMmSM/+tGPcuen1brTagDka1/7mqxatSp3OtkBAQQQQKAeAnlGJeo97P3vf7+cPHkyN06r978PfvCD8tOf/jTzPVqnfzTTZeVOJDsggAACCCCAQNcFWv2N0PWEckIEEKitAEEOghyVrfzchOMrWp0jXEdk5Alk9PX1yf/+7/8WmtlO1J1WAyBbtmyRP/qjPyo0fxwMAQQQQKB8AlOnTpW33357NGFZRiV2IlDQifvf5MmT5Z133smcLw3QjIyMlK+ASBECCCCAAAI1FujEb4Qac5J1BBDogABBDoIcHahW5TgkN+FylIObCu3s0Lc38wQydBSH6fjpRq66XXe2b98+GsjIuwj63/3d38nKlSu7QcI5EEAAAQQKEPjwhz8sR44cyXUP/Mu//Et54IEHCjh7+iG6ef/7/Oc/L5o3E9BJC+xo2q644gr5j//4j/SMsAUCCCCAAAIIFCrQzd8IhSacgyGAQG0ECHIQ5KhsZecm3Luiveiii0bf2szTcaFTcZw+fbp3iS5pW6BzmetUVnkDIH//938vy5cvL4UniUAAAQTqJHDvvffKX//1X+e6B7Y6vWLRrmX57fSrv/qr8uKLL+YKBqn5n//5nxdNwvEQQAABBBBAQETK8huBwkAAAQRCAgQ5StqxSZVtX4CbcPuGSUf4uZ/7udHpJPIEMs4//3w5c+ZMZxNWwNFjqTsayNDFzPMGQP7hH/5BdDFYPggggAACrQvkWSdDz6IvAJw6dar1E3ZhzxjufzpN5c9+9rNRjbTRH7qNjgYty0sUXShCToEAAggggEBHBGL4jdCRjHNQBBCIRoAgh1VUNNrR1NtMCaU8MzElbmRPq5GlM0HNdY5wM/d2+ynozRGqUHd0KqubbrqJAEhvqhBnRQCBighMnz59tEM96xSLnVgno5uUsd//8gSeNK8f+MAH5H/+53+6Scy5EEAAAQQQiFIg9t8IUaKTaAQQyCVAkIMgR64KE9PG3ISzldbAwID8y7/8S+YRGXpUHZEReyAjSafqdUcXM1+7di0BkGyXCFshgEDFBX7jN35DDh06lHof1HuDfvT/P/nJT8o//uM/Vk6mqvc/Xb/qG9/4Rq4y/q3f+i351re+VbkyJkMIIIAAAgi0IlDV3witWLAPAgiUU4AgB0GOctbMAlLFTXgc8ctf/rLcfvvtuTu1dYHwOn7qXHcee+wx+eM//uPcdUXXDvn93//9OlYX8owAAhEIfPe735Xf/u3fzty26X1gxowZ8vrrr0eQu+KSWMf73+zZs2V4eDjXaJ39+/fLb/7mbxYHz5EQQAABBBAouUAdfyOUvEhIHgIIOAIEOQhyVPai4CY8XrTm7VPzF/Pv2KfV6FTlpe74Zf/2b/9WbrnllmAnYdLc6J0qK46LAAIIZBEI3Qd1eqMY1orKkscituH+16w4depUefvtt0f/6N7juOcVUeM4BgIIIIBALAL8RoilpEgnAvUVIMhR37In5zUSePDBB+Xuu++uUY7JarcFNm/ePDoFFh8EEECgjAJ79+6V66+/voxJI00RCujIIJ3Oig8CCCCAAAIIIIAAAgiUQ4AgRznKgVQggAACCCCAAAIIIIAAAggggAACCCCAAAIIIIBATgGCHDnB2BwBBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQTKIUCQoxzlQCoQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAgpwBBjpxgbI4AAggggAACCCCAAAIIIIAAAggggAACCCCAAALlECDIUY5yIBUIIIAAAggggAACCCCAAAIIIIAAAggggAACCCCQU6DjQY59+0SuvXY8VQMDItu3i8yYIfLAAyLr1oVTvHatyCOPiEyZ0thG91uxQuSZZ0QWLWr87a23RG6/XWTz5vBxNmwQuffe8f3dLe3zmDS553b3Mfmyt3vjDZHly0WGhiamxaT55ZdFli0Tee655nyYPUx+9N+a90OHmv3cI8+fL7Jjh8i8eTlLPmVzk44jR8bLy7dLUvma7e0869/cNJvv77qr4ed+TLnbf7frgP49rdxMOu390vYx56t6WRdbczgaAggggAACCCBQbgH9bbl1a/Jv3HLngNQhgAACCCCAAAIIIICALdDRIId2Iu/a1dwJrx3au3c3AhP2x3R0b9o0HsCwv7cDCEkBCO2QvvVWf8e/PtA8/HByUEDTrB3h+vnSl8LBA18HuUmjBmA0qOL72B3+vny4QQ4T4NFjme/6+8PHL6p628GLbdv8wYcs5esLTKnTo4+K3HlnI4AVCnKYv199dXOwS/Oo57700vF02QEzNwCi24eCHJR1UTWG4yCAAAIIIIAAAnEI6O9G/W1oXryKI9WkEgEEEEAAAQQQQAABBEICHQtymA7/lSv9HeRugtKCHKaTWkdBvPRSOFBRRJBjeFikr09k2jR/MEHTet99ItOnN3JhRpvkCXJcdlkjD24AoSxBDhPAmDlTZO7ciUGGLOWbNSjjC3JkOb5dh+z0Tpo08aE1FOSgrGkcEUAAAQQQQACBegkQ5KhXeZNbBBBAAAEEEEAAgeoLdCzIkTYFUd4ghz6MaIf0PfeIrFkjEgqeFBXkGBwU+cIX/G94mVEEr77aSFMrQQ6dmkn3d0e6lCHIYQcY5szxj4zJUr5Zgj5aD3zHMuVtT1eWdDmah1UdQaMjebT87NE0SUGOqpf1rh/ukqVPLB3j23nDThm8fLD6rRs5bEnAnYLOTPenBwuN3tLgs7nmzLWoI+E++9nx6fvckWvmPN/8pshXv9rYzjcKq6VMsBMCCFRWgDaqc0V7cPigrHlqjexZsUf6p/V37kQ9PLI7haomxZ5K150GNzTF6i23NKaU1ely9YWlj3ykMR2t+X1vpuM19z57+tlOTTXbQ1ZOjQACCCBQYYEN39kg67+9fiyH9193v6z7WMK88xW2IGsIIFBugY4FOUwH92uvZVszImkkh9sJnvT2VVFBjgcfFLn7bpGPfrR5JIrm67bbGiM5nniivSDH4sWNY2sgwXTmlyHIYU/rdfHFjTS6U3BlKV/7QTGp89It37yjOEznq5l2YM+eiWu3JAU5qlzWN+68Ufa8skeGVg7Jgv4Fo63RxoMbZdWVq6Rvcl+5WydS13UB9zpxA5Xm36bN0gSaqQdNG2amjrM7jcw1bgcfzbno7Ol6MXNCBKIVoI3qbNHVIchhBH3PEr7f4O5Ut6G19Xx/twNy7vp/TJXV2brM0RFAAAEEihHQFyZfeP2FsaCGeYGSFyeL8eUoCCBQrEDHghyazLT1J+ysJAU53MUBk7ZNC3LowuXux54yyh5B8OSTIt/73sTFz3UEho4ScEcbhBYe93X2mUW2zQOQSUOvgxy+KaZCizNmKV/bxHbwlb0xSZu6zHcJ2A+rU6c2Ol7tRdOTghzaOVvFsuYHSPbG0n07xd2zDm+rhEZeude/fS2pk7sGkm+0h27nts1u25e9tNgSAQTqKEAb1flSr3uQw7d2n/vijS9obz/z2MF885v6wIHmF758v0k7X7qcAQEEEEAAgfYFRk6PyJLtS2RW3yx5fOnj7R+QIyCAAAIFCnQ0yGHSaS8KbU99kiXIYR4Q7BEVSWs9pAU5siw8bqagOnWqMYpBAxo6ksGcV6fK0n+HghxZFh43Hfpq4Oug17+7UzVlXeOinfqhD286xYy96Hpa0CFL+ZoFyDVt7rQ17kiO0PnsY7jHcd/Ic4+ZFuSoYllrx/2WH2yR/av3V3baiXbqOvs2C4Q6XXxtql5vL77Y2P8Tn2ge7RYaaede13TyUAMRQCCPAG1UHq3s29Y1yO/eq0IvGbm/vUPTtYb+7pt+Ne13dfbSY0sEEEAAAQS6JzD85rAs3LJQjp48KosuWSS7l+9mdoju8XMmBBDIINCVIIcb7HA7ufX70A9+39y55ni+aU6KDHJMmdIIQOhHAx16bP23drbPmFFckMN+O/HOOydO/2Ly240ghxtIsOuQr9zs702wI2k7c/yk0S1p01X5HkR9Hav2G3knTohce23znP/ug2fVylqnqjo+cpwfHxkaQjZptG96jYQ+9pRzpl2++uqJwdi0IIc7io11OKh9CCCQRYA2KotSe9vUeSSHuxaHK2l+2x49Or72hr4IZT4EOdqre+yNAAIIIFBOAftliNnTZ4+u23XTUzeNJpYgRznLjFQhUGeBrgY5FNo3FFz/HgpyhBagDnWEFx3ksEc26Bocl146/tZyUSM5NP/m4X3v3sZi5Prp9kiOpOBCkqt9AYXK197GfRvTfTBMmrJLj5M1yGFvp9MHXH99cpCjamWtQY5njz/LSI4MLXxd32R1r0t36qkQnT16y57uT7dPC3Js2tQYCcdIjgwVk00QQGBMIOvvENMOmYWfaaOyVyKCHCL9/Y0Xm0IfRnJkr09siQACCCAQt4D+LhjYOiB3XHPH2JocZroqzRlBjrjLl9QjUEWBrgc5Qg+pviBH2hv9vs60ooMcpqO8r0/kueeap3EqMshhHso1wDFzpsjcud0PciTZhebCdi+KLJ0Qbln7HhiTOkCzBjk0bebYl13WmA/ZfmvcLb+qlTVrclSxye5cntLaW3Nm+xr//vdF3CkAQ2tyJK3toUEPPggggECSAG1U5+tHnYMcqhtag86WJ8jR+XrIGRBAAAEEyiHg608wU1Zd0ncJQY5yFBOpQAABS6BjQQ59CLjvPpGvfKUxtZN+kt7Q9wU50jrMfR3hRQc5NN3mPO56IkUHOdIW8u70dFWhUTOmvthBJZ3+Ka18dZ2L225rbDdv3nitS1s/w2xpprZy3U1Hx5w544Gg0Nvjeiz7rfOkIEfVytq8ZfH868/L0MohWdC/YJR248GNsurKVcyfya1ggoC55uzrRNu/p59uvNnqBjtD16K+QW1PW+dbZJyRHFRABBDIK0AblVeM7UMCSYuM278v9bf3+vUiq1c3fssS5KBOIYAAAgjURcAENK6Zdc3oIuOmf2HfsX2syVGXSkA+EYhMoGNBDnXwrafhThtgvNwgR9qURbqfb3RBWpBjxYqJJWSvD+Hr6DfnMQuQ253+ZpFyXb/DbDc0NPEcJt+hhyO3Y9+3rkUngxxp6bIDAKYDNEv5+kzcoEXSuUOmvoCTlr1ZL8UuAfsYaUGOKpa1Tlu144UdYyQ7b9gpg5cPRtZUkdxuCbjr8phrzbQ/R440X2duAMMEHD/zGZFPf3o81W7bT5CjWyXKeRColgBtVLXKs1e5sdfgsJ8D3N+d7vp/BDl6VWKcFwEEEECgFwJmNIc599c/9XXZcmjL6D+ZrqoXJcI5EUAgSaCjQQ7oEUAAAQTqJZA0qqpeEuQWAQTKKEAbVcZSIU0IIIAAAggggAACCCCAQHsCBDna82NvBBBAAAFLgA5EqgMCCJRZgDaqzKVD2hBAAAEEEEAAAQQQQACB1gQIcrTmxl4IIIAAAh4BOhCpFgggUGYB2qgylw5pQwABBBBAAAEEEEAAAQRaEyDI0ZobeyGAAAIIEOSgDiCAQGQCBDkiKzCSiwACCCCAAAIIIIAAAghkECDIkQGJTeIU6Ovrk5GRkTgTT6oRiExg2rRp8uabb0aWapKLAAJ1EaCNqktJk08EEEAAAQQQQAABBBCoowBBDqvUJ02aJOfOnatjPahUnidPnixnzpwZy9OFF14op0+frlQeyQwCZRA4//zzR9tMu93UdlT/d/bs2TIkkTQggECNBd73vveNtkVuG6Vt1zvvvFNjGbLergDPDO0Ksj8CCCCAAAIIIIAAAsUKEOQgyFFsjerh0X7t135Nnn/+eW+gSh9G9fvDhw/3MIWcGoG4Bf7iL/5CPv/5z0+4xkxnj6/TR/+2fv360f/xQQABBDotEAq+aqDDbaMIyna6NKp7fIIc1S1bcoYAAggggAACCCAQpwBBDoIccdZcJ9XnnXfeWMerdnC8++67Y50ZF1xwwdhb5fpQ+t5771Uiz2QCgW4I6PWj10zaaA23wyfU0ajXql6ffBBAAIGiBOzfAOaY7v3ebaOy7FNU+jhO9QQIclSvTMkRAggggAACCCCAQNwCBDkIckRdg+1OCv1ve4ocX6erCXAQ7Ii62El8hwVCnX8XXXSRnDp1ynv2pA4fXR/nZz/7mXcECEHHDhcmh0egggIXX3yx/PSnP00NvtpZT2qjQkHZn//5n5fh4eEKCpKldgUIcrQryP4IIIAAAggggAACCBQrQJCDIEexNapLR0sKbpgkhB5AtTODYEeXCorTRCEQmrc+z9oaeTp8Qh2KzJMfRXUhkQj0RCA0qkzX3Xr77bdT05S1jXr/+98/Gsx1R68xCi2VuFYbZK1PtUIhswgggAACCCCAAAII9FCAIAdBjh5Wv/yntoMbaaMx0h5A8xwrf0rZA4FyC9jBPjswqB2JZ86cyZ34tOstdEDtoNTpq+wORd3WHZmVO0HsgAAC0QuE2qmNGzfKn/zJn+TKXytt1Ne+9jVZu3Yt7VMu6Xps3Ep9qocMuUQAAQQQQAABBBBAoDcCBDkIcvSm5uU8aysBiawPoK0cO2fy2RyBngt0OpiQ9XpLgyg6+JJ2Pr5HAIHyCHz5y1+WP/3TP+1IUKGINirUPm3evFluuumm8kCSko4LFFGfOp5IToAAAggggAACCCCAQI0ECHIQ5Ch1dW9naqm8D6BZpsAqNRaJQ8AR6Oa0UHmvtyyFVcQ0WlnOwzYIINA7AV3rR0ePdXp6qKLbqND0WVOnTh1dg4hPtQWKrk/V1iJ3CCCAAAIIIIAAAgh0XoAgB0GOzteyFs7QTnDDnK7VB1CCHS0UGLuUQkA713Ruenfqp7Sp3YpIfKvXW55zhxZE1zn0R0ZG8hyKbRFAoIcCoQDsBz7wATlx4kRHUtbJNqq/v1/++7//O9dC6B3JJAftmkAn61PXMsGJEEAAAQQQQAABBBCokABBDoIcparO+mbk2bNnR9PUbsdsuw+gdoeqdsjougF8ECibQKizsNuL5LZ7veV1Db1FnWex9LznZHsEEGhdIBSkfO+991o/aI49u9lG9TqvOVjYtEWBbtanFpPIbggggAACCCCAAAII1EqAIAdBjlJUeJ2WxgQR9MHxV37lV+Tf//3f20pbEQ+gV1555Wg6zJvx2rH6zjvvtJUudkagHYFf+qVfkldeecU7WuPP/uzP5KGHHmrn8C3vW8T11urJ77vvPtmwYYPX5IorrpDnn3++1UOzHwIItChw9dVXy7/+67+WZnRDr9qoUCD6uuuuk6effrpFXXbrtUCv6lOv8835EUAAAQQQQAABBBAoqwBBDoIcpaib+rCoH10c+fTp04WkqcgH0MmTJ4/OGa4fdyqgQhLLQRDIKGCuFf3/Mo1aKPJ6y0gR3MztVOSabVeU/RHIL2C3VXpN9voFgTK0Ue46Q7RN+etVWfYoQ30qiwXpQAABBBBAAAEEEECgDAIEOcpQCqRBZs2aJcePHy+9xOzZs+Xo0aOlTycJrK7A3Llz5cc//nF1M1hwzn7xF39R/vM//7Pgo3I4BBBIE1iwYIEcPHgwbbPafv/xj39cvvWtb9U2/2QcAQQQQAABBBBAAAEEEChSgCBHkZocCwEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBLomQJCja9ScCAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBIoUIMhRpCbHQgABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAga4JEOToGjUnQgABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAgSIFCHIUqcmxMgscHD4oA1sH5I5r7pB1H1uXeT82RAABBBBAAAEEEEAgr8ADD4isWycyf77Ijh0i8+blPQLbI4AAAggggAACCCCAQFkFCgtyvPWWyO23ixw5IrJ9u8iMGf4s79sncu21498NDEzc/uWXRZYtE3nuucZ27sOI+f6uu0SWL594Hj3/ihXNf3/mGZFFi8b/Zh501q4VeeQRkSlTmrc36bT3S9vHHMHsax/7jTcaaR0amphecw473256dS9jrP+taT50qNnSPXKZH+JiCnIMvzksC7cslKMnj44R33/d/QRnytqqka5KCWh7vnVr8n2lUhkmMwggEIUAbVMUxTSWSC2vhx8uPrhhfrtv2tT8nBGXDqlFAAEEEEAAAQQQQCB+gcKCHHbwYts2f/BBgwS7djU/YOjDwe7djQCJfkyAwu7k1wDBo4+K3HlnIxgRCnKYv1999cTAhZ770kvH02UCFnpOX0AhFOTQbfXzpS+F3wDzBUNMkEMDLffe6684dpDDF3xxgxx2YMZ8198fPn6ZqmtMQY4bd94oV3zwirGghkn74l9YLI8vfbxMrKQFgcoJaHuq7XFS8LxymSZDCCBQegHaptIXUVMCtbyGh/0vNrWTE9/zQjvHY18EEEAAAQQQQAABBBBoTaCwIIcJYMycKTJ37sSHCNPJv3KlPwCiyc/aUe8LcmQ5vk1kp3fSpIkdaKEghz4g9fWJTJvmDyZo2u67T2T69MbZzCiRPEGOyy5rBILcYBFBjtYqeSf22vCdDbLlB1tk/+r90j+tvxOn4JgIICAidCRSDRBAoIwCtE1lLJVwmghyxFVepBYBBBBAAAEEEEAAgbwChQQ57ADDnDkit946cTh42hRTmvAsgQDdznesvA8v5uFUR1VoegcHm4MWSUEO3fYLX/C/WWxGjLz6avMbY1nyZudL93dHvVQ1yKFluv7b68fq7s4bdsrg5YN563JXtyfI0VXuSp7Mnbpvw4bxNig06k2n8TNtlWnDdFTZZz87PhWeOwrMnOeb3xT56lcb2/lGr7WDrKOb1jy1Rvas2FNY0M+dtlDTZ09vaNrDzZsbKQ9Na3jLLY2p/XQ7DRx/5CON6RB1ukNtZ3V+dv0YN3sawDJP+ddOebEvAnkEqtRW5cl3aFvapiIUu3cMX3nZ90l7ZLemynd/dKec1fu1ji7XUejmHmRyZO/vTp/rTtFr/66/6qrGfSg0jW73xDgTAggggAACCCCAAAJxChQS5LDnub344sZIDXdaJvOA8Npr4flw7U6rpE44N8iRdxSHFpX9Bt6ePY01POxzJgU5HnxQ5O67RT760eZRKZqO225rjOR44on2ghyLFzeOrUEjMxqkikGOk6dPir2+hU4NteeVPTK0ckgW9C8o7VWl6Tw+clx2L98tfZP7SptOElZOAbd9cYOg5t/m+tdcmCn9THtgOmbsThPTNtpBW3OuTnbYdyLIYUrO97a0ry1051sPrXHk+7vdiet2fjFVVjmvIVLVHYGqtVVFqtE2FanZ+WP5XobS+4beZ82afb51O8w1YI+uPny4MX2uLlwemq7KVz/cFxjs5x77RYfOa3AGBBBAAAEEEEAAAQSqJ9B2kMM3xVRoMca0NSeU135byrcouW7jBjlaWfTPfviYOnXioulJQQ7tZHzySZHvfa95Wi7Nt74ZrKND3Iep0MLjvg5Ks6C6+2BVxSCHu67FyOkRWbJ9iczqm5V7vQsdXWGPCHEv16IWCzfnKep41WtWyFGSQGhUl9tu2m2QHs8dIecb7aHb6X72tr4OmqJLqNtBDl9HlBvs9gV87PuHHQgybeuBA81BeOZaL7qmcLyYBKrYVhXp7+vEpm0qUrjYY2UZ8e3eR7KMwvbdJ0L3Dvd45t5z5AjrThVb2hwNAQQQQAABBBBAoI4CbQc5tCNJp0qxF+JOCzrYQ8NDby7ZQ7zdodtZgxzuMPGkN3TdY6YFOU6daoy00ICGvgFmHlR0zRH9dyjIkWXhcRPk0ArpC8bo383b3KbSZl3PpCyVPGnh8TKPktC07Xhhhyz75WW5gzBlsScdvRUIdX64wQlz/b/4YiO9n/hE88ix0HzwbvvbqbkYA+4AACAASURBVI76bgUV3XyGgr1uGxiaIjH0d18HWNq9rLc1ibMj0FmBqrRVnVKibeqUbGeOmxbksF/EMs8mWe4BoeeF0ChAOx2aU3eUZmdyz1ERQAABBBBAAAEEEKi+QNtBDjeQYJOlzStrgh1J25njJ414SJuuytcplvYG3okTItde2zyFlfuApP/WjwY69GFG/63pnTGjuCCH/daXmf9Xz1n1IMezx58t1aLeJijjTq9V/SaCHBYt4M5v7x7fnjbPdLBcffXEaz4tyOGOCCt6HQ473d0cyeGuxeH6mfvJ0aPja29oQNp8CHIUXaM5XlUFqtBWmdGh+47tGyumRZcsKmSqyVCQw12jwZyYtqm3V4ovyGG/dKXlc889ImvWjE+563v5wM1F2ktROq2V/cn68lJvtTg7AggggAACCCCAAALxCbQV5EgKLmR5MFAu39D+tAcIt5MqaRonPVbWIIe9nU5lcv31yUEOexSLrsFx6aXjb1oXNZJD028eoPbubSxGrp+qBzlaWe+iU2+WmwDH9IumlyrwEl9zQ4rN9exOPRWSsTtg7PnAdfu0IMemTY2Omk6N5LDT3IsgR3//+ELtPj9GcnC9IdCeQNbfcaY9Wreucb4yt1XtiTTvHQpy0DYVqVzcsdzf5b57ozudVJb7JyM5iisjjoQAAggggAACCCCAQDsCbQU5kh6As8xjm7XDzx0u7uu8SnoQyRrk0PSYY192WWNudvvtZ/cByRy3r0/kueeap+wqMshhOhA0wDFzpsjcudUJcrhrcgy/OSwLtyyU1b++WtZ97P96TNqp4W3ua94C1cOwyHibmOw+KpA28sww2e3r978v8vDDzetFhNbkSFrbwyyuWnRRdDPIoWkPrftk54sgR9GlzPHqJlDFtqrIMgyNCN66NXl9BdqmIksh+7Hc3+W+l6zctZyyPMu0siaHTm2rIwzTXtLKnju2RAABBBBAAAEEEEAAgbaCHGnz29oPgDr90333iXzlK43pnPTj/rjXdS5uu62x3bx544XjPkiGHhDN1FbuOh/mIWXOnPHgQOgtaD2r/fZ0UpBDtzUPN+45iw5ypC3aHuuaHDr9084bdsrg5YNiAgrHRo6VZsSEGcWx5VNbRtPIB4EiBExbZbcv2pY8/XRjdILbsRJqw/TNaXu6P98i41neRC0iT506RtJCvnabrm3g+vUiq1c37h90JHaqRDhunQRoq8KlTdsU15Xg/i537xHmPjs0JGL/pjfXgD1C6fBhEZ2GKnSvCS0onnUdl7hkSS0CCCCAAAIIIIAAAuUQaDnIEepAsrPldq7ZHfVmO3daA/shw2zjBhCSzu3bX4/jC0KEFgW0j5EW5DDbmgXITZpDQQ59eHI/xiDN1Dxo+dYwiTXIseaqNXLg+AEx82XPnj67NAEOLSd7LQ7fJXv/dfeXYsRJOZoTUpFHwF3PyLRRoc4RN4BhOks+8xmRT396/Mxumxp7kMNeg8Nem8lt6+fPbx7pQpAjT21kWwSSO/NXrBj/nraqYUHbFNdV43sxy74P6z1Ep3nU7XTUo/6uNx93fRr3mcI+jvvcYKZx02O5v98ZyRFXHSK1CCCAAAIIIIAAAuUWaDnIUe5skToEEECg2gJJo9GqnXNyhwACMQnQVsVUWqQVAQQQQAABBBBAAAEEEIhTgCBHnOVGqhFAoOYCdBzWvAKQfQQiEaCtiqSgSCYCCCCAAAIIIIAAAgggELEAQY6IC4+kI4BAfQXoOKxv2ZNzBGISoK2KqbRIKwIIIIAAAggggAACCCAQpwBBjjjLjVQjgEDNBeg4rHkFIPsIRCJAWxVJQZFMBBBAAAEEEEAAAQQQQCBiAYIcVuH19fXJyMhIxMVJ0hFAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQqI8AQQ4R+dCHPiQ/+clPxkr9wgsvlNOnT9enFpBTBBCIRmDSpEly7ty5aNLb64Ti1esS4Px1FeDaSy55fOK+Mii/uMuP1COAAAIIIIAAAghUT6D2QY7zzjvP22GoDy+XXXaZvPjii9UrdXKEAALRCtCxkq/o8MrnxdYIFCXAtUeQo6i6VMbjUL/LWCqkCQEEEEAAAQQQQKDOArUNctjBDf3vs2fPinlgueCCC0b/rR/923vvvVfnOkLeEUCgRAJ0rOQrDLzyebE1AkUJcO0R5CiqLpXxONTvMpYKaUIAAQQQQAABBBCos0Dtghx2cMMNYLgPLOeff/5YgINgR50vE/KOQHkE6FjJVxZ45fNiawSKEuDaI8hRVF0q43Go32UsFdKEAAIIIIAAAgggUGeB2gQ5sgQsQg8sWfatcyUi7wgg0D0BOlbyWeOVz4utEShKgGuPIEdRdamMx6F+l7FUSBMCCCCAAAIIIIBAnQUqH+SYPHmynDlzZrSM00ZjpD2wJI0CqXMlIu8IINA9gbR2qnspieNMeMVRTqSyegJcewQ5qlerx3NE/a5y6ZI3BBBAAAEEEEAAgRgFKh3ksIMSF154oZw+fTqxjLI+sBDsiLGqk2YEqiGQtZ2qRm7bzwVe7RtyBARaEeDaI8jRSr2JZR/qdywlRToRQAABBBBAAAEE6iJQySCHb1HxLAWa94Gl1fNkSQvbIIAAAj6BvO1U3RXxqnsNIP+9EuDaI8jRq7rXjfNSv7uhzDkQQAABBBBAAAEEEMguUKkgR7sjLFp9YCHYkb3CsSUCCLQn0Go71d5Z490br3jLjpTHLcC1R5Aj7hpM+VW5/MgbAggggAACCCCAQPUEKhHkKGph8HYfyO1gh6bp3XffrV6NIUcIINBTgXbbqZ4mvgcnx6sH6JwSgf9bB+3cuXNYBARom+KuGpRf3OVH6hFAAAEEEEAAAQSqJxB1kOOCCy6Qs2fPjpZK2qLiWYquiAeWK664Ql566SUxD/aaxnfeeSfL6dkGAQQQSBUoop1KPUmFNsCrQoVJVqIS4NpLLi58oqrOExJL+cVdfqQeAQQQQAABBBBAoHoCUQc59AFDPzNnzpTXXnut7dIp8oFl8uTJcubMmdE08SZj20XDARBA4P8Eimyn6oCKVx1KmTyWUYBrjyBHGetlUWmifhclyXEQQAABBBBAAAEEEChGIOogx5IlS2T37t3FSHToKB/60IcKCcB0KHkcFgEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQACBaAWiDnJEq07CEUAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAoG0BghxtE3IABBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQ6IUAQY5eqHNOBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQaFuAIEfbhBwAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEeiFAkKMX6pwTAQQQQCAo8MADIuvWicyfL7Jjh8i8eWAhgAACvRegbep9GZACBBBAAAEEEEAAAQQQQMAnQJCjw/Vi1w93ySPPPiK7l++Wvsl9HT4bh0cAgbILbN8usnWriP7/jBllT23306cuDz9cfHDj5ZdFli0T2bRJZNGi7ueLMyIQmwBtVXOJ0TbFVoNJLwIIIIAAAggggAACCNRJgCBHh0r74PBBGdg6ICdPn5RFlywiyNEhZw6LQGwC+ibwvn0EOULlpj7DwyKPPCIyZUpxpavm114r8swzBDmKU+VIVRagrWouXdqmKtd28oYAAggggAACCCCAAAKxCxDk6EAJbvjOBtn7o72jgY2b//lmOT5ynCBHB5w5JAIxCtBxmFxqdCTGWKtJcxUFaKsIclSxXpMnBBBAAAEEEEAAAQQQqKZAlEEODSKs//b6sRK5/7r7Zd3H1pWyhG7ceSNBjlKWDIlCoLsCZrqk554bP+/AwPiIjrfeErn9dpHNmxvfu+tRmP1vuUXk0KHGdtu2iXzkI41pmO66S+TVVxtrWehn7drGaAjdVkcw+I7ZXYHks/l8TB50RIeZC98cxTci4403RJYvFxkaamy1YYPInXc2u/r212loVqzwl4v+1ZSN/vdVVzVs7bSVyZG0INCuAG1VsyBtU7s1qlr7x/QMUi15coMAAggggAACCCCAQLJAdEEOXePihddfGAtq6L+XPrFUdt6wUwYvHyxdeRPkKF2RkCAEeirgezva7kQ30zS587/bHW12B7/v72ZqJs2oGygo+1RZvpEcajFnzvg0U7658U2eNfCjgQ79HD7cmPJKFy4PTVflKw/9265d4+uC2AEoDZzce29PqxAnR6ArArRVzcy0TV2pdqU+SWzPIKXGJHEIIIAAAggggAACCBQsEF2Qw83/yOkRWbJ9iczqmyWPL308F4/7Npa7cxEjRAhy5CoSNkag8gK+jkNfp70ZlbByZaPT3gQzBgebO9l9fzed8gcONC/gHcO6FFmmq3JtzL91QfFQAMKX95CHezzjeeQIa6lU/gIlg2MCtFXpQQ63utA21esCaucZpF5S5BYBBBBAAAEEEEAAgc4LRB3kGH5zWBZuWShHTx4t7eLeBDk6X4k5AwIxCbgdh75RHJof8/f+/kbHvQlm6LRUZqSCbhf6uy9YYLbdtKm8i2+nBTnskStmVEWWfPkCGklrDtjpUGedSkw/RS+IHlPdJa31EqCtyhfkoG2q1/URwzNIvUqE3CKAAAIIIIAAAgjUXSC6IIc9+mL29NmyZ8Ueuempm0bLURf67pvcV6oyJchRquIgMQj0XCDUcWjW4nATaKabOnp0fO2NugU57PU41OOee0TWrGkEajQApAGMW29tHrXiOoaCHMPD/sCFXU5TpxLk6PmFQwK6LkBblR7koG3qerXs6QljewbpKRYnRwABBBBAAAEEEECgywJRBTkODh+Uga0Dcsc1d4ytyWGGircS5GC6qi7XNk6HAAKjC2jb62K4IzZCRHUdyeELTrjTSWWZhouRHFx8COQToK1KDnLQNuWrT7FvXfQzSOwepB8BBBBAAAEEEEAAgbIJRBXk8C0yboaLX9J3CSM5yla7SA8CCEwQCM1zv3Vr8noPdQ1y+NYrcdch6dSaHGY9lNCUYlRvBKosQFuVHOSgbapy7Z+YtxifQepVQuQWAQQQQAABBBBAoO4CUQU5TEDjmlnXjC4ybkZx7Du2jzU56l6TyT8CkQgkLTI+Z8741Enasb5+vcjq1SLz5tV3TQ43uGMCGkNDImZNDi16dV2xQmTbtvE1Sw4fFpkyJewXWlA861oEkVQ5kolASwK0VclBDtqmlqpVtDvF+AwSLTYJRwABBBBAAAEEEECgBYGoghyaP/Mmlcnr1z/1ddlyaMvoP1mTo4UawC4IINBVAdOxrmtwDAyMj96wO+81QfPnN68xUdeRHHYAw7jowukaiDBrcpgCNNPHmH/bQRD3OM88M774uj2vvm5n1kHRAIl+GMnR1UuEk5VEgLaquSC0nXDX8DHBVdqmklTaDicjtmeQDnNweAQQQAABBBBAAAEESiUQXZCjVHokBgEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBHomQJCjZ/ScGAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBNoRIMjRjh77IoAAAggggAACCCCAAAIIIIAAAggggAACCCCAQM8ECHL0jJ4TI4AAAggggAACCCCAAAIIIIAAAggggAACCCCAQDsCBDna0WNfBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQ6JkAQY6e0XNiBBBAIL/ApEmT5Ny5c/l3rOkeeNW04Ml2zwW49pKLAJ+eV1ESgAACCCCAAAIIIIAAAhUSIMhRocIkKwggUH0BOsbylTFe+bzYGoGiBLj2CHIUVZc4DgIIIIAAAggggAACCCCQJkCQI02I7xFAAIESCdBxmK8w8MrnxdYIFCXAtUeQo6i6xHEQQAABBBBAAAEEEEAAgTQBghxpQnyPAAIIlEiAjsN8hYFXPi+2RqAoAa49ghxF1SWOgwACCCCAAAIIIIAAAgikCRDkSBPiewQQQKBEAnQc5isMvPJ5sTUCRQlw7RHkKKoucRwEEEAAAQQQQAABBBBAIE2AIEeaEN8jgAACJRKg4zBfYeCVz4utEShKgGuPIEdRdYnjIIAAAggggAACCCCAAAJpAgQ50oT4HgEEECiRAB2H+QoDr3xebI1AUQJcewQ5iqpLHAcBBBBAAAEEEEAAAQQQSBMgyJEmxPcIIIBAiQToOMxXGHjl82JrBIoS4NojyFFUXeI4CCCAAAIIIIAAAggggECaAEGONCG+RwABBEokQMdhvsLAK58XWyNQlADXHkGOouoSx0EAAQQQQAABBBBAAAEE0gQIcqQJ8T0CCCBQIgE6DvMVBl75vNgagaIEuPYIchRVlzgOAggggAACCCCAAAIIIJAmQJAjTYjvEUAAgRIJ0HGYrzDwyufF1ggUJcC1R5CjqLrEcRBAAAEEEEAAAQQQQACBNAGCHGlCfI8AAgiUSICOw3yFgVc+L7ZGoCgBrj2CHEXVJY6DAAIIIIAAAggggAACCKQJEORIE+J7BBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQKKUAQY5SFguJQgABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAgTQBghxpQnyPAAIIIIAAAggggAACCCCAAAIIIIAAAggggAACpRQgyFHKYiFRCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAgggkCZAkCNNiO8RQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEECglAIEOUpZLCQKAQSqJPDAAyLr1onMny+yY4fIvHlVyl258nJw+KAMbB2QO665Q9Z9bF25EkdqECi5AG1VyQuI5CGAAAIIIIAAAggggAACCHgFCHJQMRBAAIEOCmzfLvLww8UHN15+WWTZMpFNm0QWLepgBiI7NEGOyAqM5JZGgLaqu0Wx64e75JFnH5Hdy3dL3+S+7p6csyGAAAIIIIAAAggggAACFRMgyFGxAiU7CCBQLgF9M3p4WOSRR0SmTCkubfv2iVx7rcgzzxDksFUJchRXxzhSvQRoq7pT3qaNOnn6pCy6ZBFBju6wcxYEEEAAAQQQQAABBBCouABBjooXMNlDAIHeCtBx2F1/ghzd9eZs1RGgrep8WW74zgbZ+6O9o4GNm//5Zjk+cpwgR+fZOQMCCCCAAAIIIIAAAgjUQIAgRw0KmSwigED3Bcx0Us89N37utWvHR3SYue/Nt74RGW+8IbJ8ucjQUGOrDRtE7rxT5PbbRTZvbs6Tvb9OO7Nixfj3AwMi+rcZMxp/e+utxjH0c9VVIpouO23d1yrujHaQQ4+6/tvrxw6+84adMnj5YHEn40gIVECAtqo3hXjjzhsJcvSGnrMigAACCCCAAAIIIIBABQUIclSwUMkSAgiUR8D3drQGHObMGZ9myjcXvpmOatu2RqBDP4cPN6a80oXLQ9NV6fn0OzuooX/btWt8XRAT5NBAiQZO7r23PF7tpsSeCub+6+4fW3xcOxT3vLJHhlYOyYL+Be2ehv0RqJwAbVV3i5QgR3e9ORsCCCCAAAIIIIAAAghUW4AgR7XLl9whgECPBbJMAWNGbKxc2QhomH/rguKhAIQvyBEKfLjHM0GOI0eagyE9pirk9CbIsfgXFsvjSx8fO+bI6RFZsn2JzOqb1fT3Qk7KQRCogABtVXcLkSBHd705GwIIIIAAAggggAACCFRbgCBHtcuX3CGAQI8F0joO7alizKgK87dNm8KLivsCGr5RHCb7djr0b2a6qqIXRO8xtyStyUGnYq9Lh/OXWYC2qrulQ3vUXW/OhgACCCCAAAIIIIAAAtUWIMhR7fIldwgg0GMBX8ehvR6HroVxzz0ia9Y0Aho6ckMDGLfeOj69lC8LoSDH8PD4uh/2fnYAZOrU+gY5nj3+rOxfvV/6p/X3uGZwegTKJUBb1d3yIMjRXW/OhgACCCCAAAIIIIAAAtUWIMhR7fIldwgg0GMBt+PQF5xwp5MKTTtlZ4WRHP6CZSRHjys8p49WgLaqu0VHkKO73pwNAQQQQAABBBBAAAEEqi1AkKPa5UvuEECgxwJux6FvkXEzPdXgYGMkR6fW5DBrfpg1OZSmqtNVuWtyDL85LAu3LJTVv756bDHyHlcNTo9AqQRoq7pbHAQ5uuvN2RBAAAEEEEAAAQQQQKDaAgQ5ql2+5A4BBHos4HYcmoDGXXc1LzI+NCRi1uTQJGswZMUKkW3bGtvp5/BhkSlTRObNE3GPo9+HFhR31+qoQ5Dj5OmTsvOGnTJ4+aCYRcePjRxjqqoeXw+cvrwCtFXdLRuCHN315mwIIIAAAggggAACCCBQbQGCHNUuX3KHAAI9FvDNc28CGJq0+fNFdIFx3c6syWGSbKakMv+2gyB2IET/+5lnxhcpt9f80O903Q97xEYdghxrrlojB44fkH3H9o3yzZ4+mwBHj68FTl9uAdqq7pYPQY7uenM2BBBAAAEEEEAAAQQQqLYAQY5qly+5QwABBBBAAAEEEEAAAQQQQAABBBBAAAEEEECgsgIEOSpbtGQMAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAIFqCxDkqHb5kjsEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBCorQJCjskVLxhBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQqLYAQY5qly+5QwABBBBAAAEEEEAAAQQQQAABBBBAAAEEEECgsgIEOSpbtGQMAQSqKDBp0iQ5d+5cFbNGnhBAoEICtFUVKkyyggACCCCAAAIIIIAAAgiUXIAgR8kLiOQhgAACtgAdh9QHBBCIQYC2KoZSIo0IIIAAAggggAACCCCAQDUECHJUoxzJBQII1ESAjsOaFDTZRCByAdqqyAuQ5COAAAIIIIAAAggggAACEQkQ5IiosEgqAgggQMchdQABBGIQoK2KoZRIIwIIIIAAAggggAACCCBQDQGCHNUoR3KBAAI1EaDjsCYFTTYRiFyAtiryAiT5CCCAAAIIIIAAAggggEBEAgQ5IioskooAAgjQcUgdQACBGARoq2IoJdKIAAIIIIAAAggggAACCFRDgCBHNcqRXCCAQE0E6DisSUGTTQQiF6CtirwAST4CCCCAAAIIIIAAAgggEJEAQY6ICoukIoAAAnQcUgcQQCAGAdqqGEqJNCKAAAIIIIAAAggggAAC1RAgyFGNciQXCCBQEwE6DmtS0GQTgcgFaKsiL0CSjwACCCCAAAIIIIAAAghEJECQI6LCIqkIIIAAHYfUAQQQiEGAtiqGUiKNCCCAAAIIIIAAAggggEA1BAhyVKMcyQUCCNREgI7DmhQ02UQgcgHaqsgLkOQjgAACCCCAAAIIIIAAAhEJEOSIqLBIKgIIIEDHIXUAAQRiEKCtiqGUSCMCCCCAAAIIIIAAAgggUA0BghzVKEdygQACCCCAAAIIIIAAAggggAACCCCAAAIIIIBA7QQIctSuyMkwAggggAACCCCAAAIIIIAAAggggAACCCCAAALVECDIUY1yJBcIIIAAAggggAACCCCAAAIIIIAAAggggAACCNROgCBH7YqcDCOAAAIIIIAAAggggAACCCCAAAIIIIAAAgggUA0BghzVKEdygQACCCCAAAIIIIAAAggggAACCCCAAAIIIIBA7QQIctSuyMkwAggggAACCCCAAAIIIIAAAggggAACCCCAAALVECDIUY1yJBcIIIAAAggggAACCCCAAAIIIIAAAggggAACCNROgCBH7YqcDCOAAAIIIIAAAggggAACCCCAAAIIIIAAAgggUA0BghzVKEdygQACCCCAAAIIIIAAAggggAACCCCAAAIIIIBA7QQIctSuyMkwAgjEKLDhOxtk/bfXjyX9/uvul3UfWxdjVkgzAghUXGDXD3fJ0ieWjuVy5w07ZfDywYrnmuwhgAACCCCAAAIIIIAAAgj0SoAgR6/kOS8CCCCQUUA7DF94/YWxoIbpQKTjMCMgmyGAQNcEbtx5o+x5ZY8MrRySBf0LRs+78eBGWXXlKumb3Ne1dHAiBBBAAAEEEEAAAQQQQACB+ggQ5KhPWZNTBBCoiMDI6RFZsn2JzOqbJY8vfbwiuSIbCCAQuwAB2NhLkPQjgAACCCCAAAIIIIAAAnEKEOSIs9xINQII1FRg+M1hWbhloRw9eVQWXbJIdi/fzdvRNa0LZBuBsgnotHpbfrBF9q/eL/3T+suWPNKDAAIIIIAAAggggAACCCBQUQGCHBUtWLKFAALVEbDX45g9fbbsWbFHbnrqptEMEuSoTjmTEwRiF9Cpqo6PHKddir0gST8CCCCAAAIIIIAAAgggEJkAQY7ICozkIoBAvQQODh+Uga0Dcsc1d4ytyWGmqyLIUa+6QG4RKLuABjmePf4sIznKXlCkDwEEEEAAAQQQQAABBBComABBjooVKNlBAIFqCfjmuDdTVl3SdwlvTFeruMkNAlELsCZH1MVH4hFAAAEEEEAAAQQQQACBaAUIckRbdCQcAQTqIGACGtfMumZ0kXEzimPfsX2syVGHCkAeEYhIwLRPz7/+vAytHJIF/QtGU7/x4EZZdeUq1g+KqCxJKgIIIIAAAggggAACCCAQkwBBjphKi7QigEAtBczb0SbzX//U12XLoS2j/2RNjlpWCTKNQKkFdNqqHS/sGEvjzht2yuDlg6VOM4lDAAEEEEAAAQQQQAABBBCIV4AgR7xlR8oRQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEKi1AEGOWhc/mUcAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAIF4Bghzxlh0pRwABBBBAAAEEEEAAAQQQQAABBBBAAAEEEECg1gIEOWpd/GQeAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAIF4BQhyxFt2pBwBBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAgVoLEOSodfGTeQQQQAABBBBAAAEEEEAAAQQQQAAB+kC7HAAAASdJREFUBBBAAAEE4hUgyBFv2ZFyBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQRqLUCQo9bFT+YRQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEIhXgCBHvGVHyhFAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQqLUAQY5aFz+ZRwABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAgXgGCHPGWHSlHAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQKDWAgQ5al38ZB4BBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAgXgFCHLEW3akHAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQACBWgsQ5Kh18ZN5BBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQTiFfj//yWqF+rJ4XIAAAAASUVORK5CYII=)

第三部分以输出形式展示

![image-20211128231807349](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211128231807349.png)

![image-20211128231825172](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211128231825172.png)

![image-20211128231840234](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211128231840234.png)

第四部分为输出翻译的结果

![image-20211128231853641](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211128231853641.png)

## 其他

自动生成的语法分析表

```python
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "NUMBER PRINT VARIABLEprogram : statementsstatements : statements statement\n                  | statement statement : assignment\n                  | operation\n                  | printassignment : VARIABLE '=' NUMBERoperation : VARIABLE '=' expr\n    expr : expr '+' term\n            | expr '-' term\n            | term\n    term : term '*' factor\n            | term '/' factor\n            | factor\n    factor : VARIABLE\n            | NUMBER\n    print : PRINT '(' values ')'\n    values : VARIABLE\n                | values ',' VARIABLE\n    "
    
_lr_action_items = {'VARIABLE':([0,2,3,4,5,6,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26,27,28,29,],[7,7,-3,-4,-5,-6,-2,12,18,-15,-7,-8,-11,-14,12,12,12,12,-17,30,-9,-16,-10,-12,-13,]),'PRINT':([0,2,3,4,5,6,9,12,13,14,15,16,23,25,26,27,28,29,],[8,8,-3,-4,-5,-6,-2,-15,-7,-8,-11,-14,-17,-9,-16,-10,-12,-13,]),'$end':([1,2,3,4,5,6,9,12,13,14,15,16,23,25,26,27,28,29,],[0,-1,-3,-4,-5,-6,-2,-15,-7,-8,-11,-14,-17,-9,-16,-10,-12,-13,]),'=':([7,],[10,]),'(':([8,],[11,]),'NUMBER':([10,19,20,21,22,],[13,26,26,26,26,]),'*':([12,13,15,16,25,26,27,28,29,],[-15,-16,21,-14,21,-16,21,-12,-13,]),'/':([12,13,15,16,25,26,27,28,29,],[-15,-16,22,-14,22,-16,22,-12,-13,]),'+':([12,13,14,15,16,25,26,27,28,29,],[-15,-16,19,-11,-14,-9,-16,-10,-12,-13,]),'-':([12,13,14,15,16,25,26,27,28,29,],[-15,-16,20,-11,-14,-9,-16,-10,-12,-13,]),')':([17,18,30,],[23,-18,-19,]),',':([17,18,30,],[24,-18,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statements':([0,],[2,]),'statement':([0,2,],[3,9,]),'assignment':([0,2,],[4,4,]),'operation':([0,2,],[5,5,]),'print':([0,2,],[6,6,]),'expr':([10,],[14,]),'term':([10,19,20,],[15,25,27,]),'factor':([10,19,20,21,22,],[16,16,16,28,29,]),'values':([11,],[17,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statements','program',1,'p_program','main.py',63),
  ('statements -> statements statement','statements',2,'p_statements','main.py',70),
  ('statements -> statement','statements',1,'p_statements','main.py',71),
  ('statement -> assignment','statement',1,'p_statement','main.py',82),
  ('statement -> operation','statement',1,'p_statement','main.py',83),
  ('statement -> print','statement',1,'p_statement','main.py',84),
  ('assignment -> VARIABLE = NUMBER','assignment',3,'p_assignment','main.py',91),
  ('operation -> VARIABLE = expr','operation',3,'p_operation','main.py',100),
  ('expr -> expr + term','expr',3,'p_expr','main.py',113),
  ('expr -> expr - term','expr',3,'p_expr','main.py',114),
  ('expr -> term','expr',1,'p_expr','main.py',115),
  ('term -> term * factor','term',3,'p_term','main.py',126),
  ('term -> term / factor','term',3,'p_term','main.py',127),
  ('term -> factor','term',1,'p_term','main.py',128),
  ('factor -> VARIABLE','factor',1,'p_factor','main.py',139),
  ('factor -> NUMBER','factor',1,'p_factor','main.py',140),
  ('print -> PRINT ( values )','print',4,'p_print','main.py',152),
  ('values -> VARIABLE','values',1,'p_values','main.py',161),
  ('values -> values , VARIABLE','values',3,'p_values','main.py',162),
]
```

yacc.py在生成分析表时会创建出一个调试文件

文件中出现的不同状态，代表了有效输入标记的所有可能的组合，这是依据文法规则得到的。当得到输入标记时，分析器将构造一个栈，并找到匹配的规则。每个状态跟踪了当前输入进行到语法规则中的哪个位置，在每个规则中，`’.’`表示当前分析到规则的哪个位置，而且，对于在当前状态下，输入的每个有效标记导致的动作也被罗列出来。

```
Created by PLY version 3.11 (http://www.dabeaz.com/ply)

Grammar

Rule 0     S' -> program
Rule 1     program -> statements
Rule 2     statements -> statements statement
Rule 3     statements -> statement
Rule 4     statement -> assignment
Rule 5     statement -> operation
Rule 6     statement -> print
Rule 7     assignment -> VARIABLE = NUMBER
Rule 8     operation -> VARIABLE = expr
Rule 9     expr -> expr + term
Rule 10    expr -> expr - term
Rule 11    expr -> term
Rule 12    term -> term * factor
Rule 13    term -> term / factor
Rule 14    term -> factor
Rule 15    factor -> VARIABLE
Rule 16    factor -> NUMBER
Rule 17    print -> PRINT ( values )
Rule 18    values -> VARIABLE
Rule 19    values -> values , VARIABLE

Terminals, with rules where they appear

(                    : 17
)                    : 17
*                    : 12
+                    : 9
,                    : 19
-                    : 10
/                    : 13
=                    : 7 8
NUMBER               : 7 16
PRINT                : 17
VARIABLE             : 7 8 15 18 19
error                : 

Nonterminals, with rules where they appear

assignment           : 4
expr                 : 8 9 10
factor               : 12 13 14
operation            : 5
print                : 6
program              : 0
statement            : 2 3
statements           : 1 2
term                 : 9 10 11 12 13
values               : 17 19

Parsing method: LALR

state 0

    (0) S' -> . program
    (1) program -> . statements
    (2) statements -> . statements statement
    (3) statements -> . statement
    (4) statement -> . assignment
    (5) statement -> . operation
    (6) statement -> . print
    (7) assignment -> . VARIABLE = NUMBER
    (8) operation -> . VARIABLE = expr
    (17) print -> . PRINT ( values )

    VARIABLE        shift and go to state 7
    PRINT           shift and go to state 8

    program                        shift and go to state 1
    statements                     shift and go to state 2
    statement                      shift and go to state 3
    assignment                     shift and go to state 4
    operation                      shift and go to state 5
    print                          shift and go to state 6

state 1

    (0) S' -> program .



state 2

    (1) program -> statements .
    (2) statements -> statements . statement
    (4) statement -> . assignment
    (5) statement -> . operation
    (6) statement -> . print
    (7) assignment -> . VARIABLE = NUMBER
    (8) operation -> . VARIABLE = expr
    (17) print -> . PRINT ( values )

    $end            reduce using rule 1 (program -> statements .)
    VARIABLE        shift and go to state 7
    PRINT           shift and go to state 8

    statement                      shift and go to state 9
    assignment                     shift and go to state 4
    operation                      shift and go to state 5
    print                          shift and go to state 6

state 3

    (3) statements -> statement .

    VARIABLE        reduce using rule 3 (statements -> statement .)
    PRINT           reduce using rule 3 (statements -> statement .)
    $end            reduce using rule 3 (statements -> statement .)


state 4

    (4) statement -> assignment .

    VARIABLE        reduce using rule 4 (statement -> assignment .)
    PRINT           reduce using rule 4 (statement -> assignment .)
    $end            reduce using rule 4 (statement -> assignment .)


state 5

    (5) statement -> operation .

    VARIABLE        reduce using rule 5 (statement -> operation .)
    PRINT           reduce using rule 5 (statement -> operation .)
    $end            reduce using rule 5 (statement -> operation .)


state 6

    (6) statement -> print .

    VARIABLE        reduce using rule 6 (statement -> print .)
    PRINT           reduce using rule 6 (statement -> print .)
    $end            reduce using rule 6 (statement -> print .)


state 7

    (7) assignment -> VARIABLE . = NUMBER
    (8) operation -> VARIABLE . = expr

    =               shift and go to state 10


state 8

    (17) print -> PRINT . ( values )

    (               shift and go to state 11


state 9

    (2) statements -> statements statement .

    VARIABLE        reduce using rule 2 (statements -> statements statement .)
    PRINT           reduce using rule 2 (statements -> statements statement .)
    $end            reduce using rule 2 (statements -> statements statement .)


state 10

    (7) assignment -> VARIABLE = . NUMBER
    (8) operation -> VARIABLE = . expr
    (9) expr -> . expr + term
    (10) expr -> . expr - term
    (11) expr -> . term
    (12) term -> . term * factor
    (13) term -> . term / factor
    (14) term -> . factor
    (15) factor -> . VARIABLE
    (16) factor -> . NUMBER

    NUMBER          shift and go to state 13
    VARIABLE        shift and go to state 12

    expr                           shift and go to state 14
    term                           shift and go to state 15
    factor                         shift and go to state 16

state 11

    (17) print -> PRINT ( . values )
    (18) values -> . VARIABLE
    (19) values -> . values , VARIABLE

    VARIABLE        shift and go to state 18

    values                         shift and go to state 17

state 12

    (15) factor -> VARIABLE .

    *               reduce using rule 15 (factor -> VARIABLE .)
    /               reduce using rule 15 (factor -> VARIABLE .)
    +               reduce using rule 15 (factor -> VARIABLE .)
    -               reduce using rule 15 (factor -> VARIABLE .)
    VARIABLE        reduce using rule 15 (factor -> VARIABLE .)
    PRINT           reduce using rule 15 (factor -> VARIABLE .)
    $end            reduce using rule 15 (factor -> VARIABLE .)


state 13

    (7) assignment -> VARIABLE = NUMBER .
    (16) factor -> NUMBER .

  ! reduce/reduce conflict for VARIABLE resolved using rule 7 (assignment -> VARIABLE = NUMBER .)
  ! reduce/reduce conflict for PRINT resolved using rule 7 (assignment -> VARIABLE = NUMBER .)
  ! reduce/reduce conflict for $end resolved using rule 7 (assignment -> VARIABLE = NUMBER .)
    VARIABLE        reduce using rule 7 (assignment -> VARIABLE = NUMBER .)
    PRINT           reduce using rule 7 (assignment -> VARIABLE = NUMBER .)
    $end            reduce using rule 7 (assignment -> VARIABLE = NUMBER .)
    *               reduce using rule 16 (factor -> NUMBER .)
    /               reduce using rule 16 (factor -> NUMBER .)
    +               reduce using rule 16 (factor -> NUMBER .)
    -               reduce using rule 16 (factor -> NUMBER .)

  ! VARIABLE        [ reduce using rule 16 (factor -> NUMBER .) ]
  ! PRINT           [ reduce using rule 16 (factor -> NUMBER .) ]
  ! $end            [ reduce using rule 16 (factor -> NUMBER .) ]


state 14

    (8) operation -> VARIABLE = expr .
    (9) expr -> expr . + term
    (10) expr -> expr . - term

    VARIABLE        reduce using rule 8 (operation -> VARIABLE = expr .)
    PRINT           reduce using rule 8 (operation -> VARIABLE = expr .)
    $end            reduce using rule 8 (operation -> VARIABLE = expr .)
    +               shift and go to state 19
    -               shift and go to state 20


state 15

    (11) expr -> term .
    (12) term -> term . * factor
    (13) term -> term . / factor

    +               reduce using rule 11 (expr -> term .)
    -               reduce using rule 11 (expr -> term .)
    VARIABLE        reduce using rule 11 (expr -> term .)
    PRINT           reduce using rule 11 (expr -> term .)
    $end            reduce using rule 11 (expr -> term .)
    *               shift and go to state 21
    /               shift and go to state 22


state 16

    (14) term -> factor .

    *               reduce using rule 14 (term -> factor .)
    /               reduce using rule 14 (term -> factor .)
    +               reduce using rule 14 (term -> factor .)
    -               reduce using rule 14 (term -> factor .)
    VARIABLE        reduce using rule 14 (term -> factor .)
    PRINT           reduce using rule 14 (term -> factor .)
    $end            reduce using rule 14 (term -> factor .)


state 17

    (17) print -> PRINT ( values . )
    (19) values -> values . , VARIABLE

    )               shift and go to state 23
    ,               shift and go to state 24


state 18

    (18) values -> VARIABLE .

    )               reduce using rule 18 (values -> VARIABLE .)
    ,               reduce using rule 18 (values -> VARIABLE .)


state 19

    (9) expr -> expr + . term
    (12) term -> . term * factor
    (13) term -> . term / factor
    (14) term -> . factor
    (15) factor -> . VARIABLE
    (16) factor -> . NUMBER

    VARIABLE        shift and go to state 12
    NUMBER          shift and go to state 26

    term                           shift and go to state 25
    factor                         shift and go to state 16

state 20

    (10) expr -> expr - . term
    (12) term -> . term * factor
    (13) term -> . term / factor
    (14) term -> . factor
    (15) factor -> . VARIABLE
    (16) factor -> . NUMBER

    VARIABLE        shift and go to state 12
    NUMBER          shift and go to state 26

    term                           shift and go to state 27
    factor                         shift and go to state 16

state 21

    (12) term -> term * . factor
    (15) factor -> . VARIABLE
    (16) factor -> . NUMBER

    VARIABLE        shift and go to state 12
    NUMBER          shift and go to state 26

    factor                         shift and go to state 28

state 22

    (13) term -> term / . factor
    (15) factor -> . VARIABLE
    (16) factor -> . NUMBER

    VARIABLE        shift and go to state 12
    NUMBER          shift and go to state 26

    factor                         shift and go to state 29

state 23

    (17) print -> PRINT ( values ) .

    VARIABLE        reduce using rule 17 (print -> PRINT ( values ) .)
    PRINT           reduce using rule 17 (print -> PRINT ( values ) .)
    $end            reduce using rule 17 (print -> PRINT ( values ) .)


state 24

    (19) values -> values , . VARIABLE

    VARIABLE        shift and go to state 30


state 25

    (9) expr -> expr + term .
    (12) term -> term . * factor
    (13) term -> term . / factor

    +               reduce using rule 9 (expr -> expr + term .)
    -               reduce using rule 9 (expr -> expr + term .)
    VARIABLE        reduce using rule 9 (expr -> expr + term .)
    PRINT           reduce using rule 9 (expr -> expr + term .)
    $end            reduce using rule 9 (expr -> expr + term .)
    *               shift and go to state 21
    /               shift and go to state 22


state 26

    (16) factor -> NUMBER .

    *               reduce using rule 16 (factor -> NUMBER .)
    /               reduce using rule 16 (factor -> NUMBER .)
    +               reduce using rule 16 (factor -> NUMBER .)
    -               reduce using rule 16 (factor -> NUMBER .)
    VARIABLE        reduce using rule 16 (factor -> NUMBER .)
    PRINT           reduce using rule 16 (factor -> NUMBER .)
    $end            reduce using rule 16 (factor -> NUMBER .)


state 27

    (10) expr -> expr - term .
    (12) term -> term . * factor
    (13) term -> term . / factor

    +               reduce using rule 10 (expr -> expr - term .)
    -               reduce using rule 10 (expr -> expr - term .)
    VARIABLE        reduce using rule 10 (expr -> expr - term .)
    PRINT           reduce using rule 10 (expr -> expr - term .)
    $end            reduce using rule 10 (expr -> expr - term .)
    *               shift and go to state 21
    /               shift and go to state 22


state 28

    (12) term -> term * factor .

    *               reduce using rule 12 (term -> term * factor .)
    /               reduce using rule 12 (term -> term * factor .)
    +               reduce using rule 12 (term -> term * factor .)
    -               reduce using rule 12 (term -> term * factor .)
    VARIABLE        reduce using rule 12 (term -> term * factor .)
    PRINT           reduce using rule 12 (term -> term * factor .)
    $end            reduce using rule 12 (term -> term * factor .)


state 29

    (13) term -> term / factor .

    *               reduce using rule 13 (term -> term / factor .)
    /               reduce using rule 13 (term -> term / factor .)
    +               reduce using rule 13 (term -> term / factor .)
    -               reduce using rule 13 (term -> term / factor .)
    VARIABLE        reduce using rule 13 (term -> term / factor .)
    PRINT           reduce using rule 13 (term -> term / factor .)
    $end            reduce using rule 13 (term -> term / factor .)


state 30

    (19) values -> values , VARIABLE .

    )               reduce using rule 19 (values -> values , VARIABLE .)
    ,               reduce using rule 19 (values -> values , VARIABLE .)

WARNING: 
WARNING: Conflicts:
WARNING: 
WARNING: reduce/reduce conflict in state 13 resolved using rule (assignment -> VARIABLE = NUMBER)
WARNING: rejected rule (factor -> NUMBER) in state 13
```