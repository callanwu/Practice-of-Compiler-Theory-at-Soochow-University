

| 院系   | 年级专业           | 姓名   | 学号       | 实验时间   |
| ------ | ------------------ | ------ | ---------- | ---------- |
| 计科院 | 19计算机科学与技术 | 吴家隆 | 1915404063 | 2021.10.25 |

------

编程语言：**python3.9**

# 实验内容

## 概率上下文无关文法

PCFG在GFG的基础上引入了P，加上了每个规则的概率。

PCFG中定义一棵句法树的概率为所有用到的规则概率的乘积，一般来说，概率值大的更可能是正确的句法树。 

## CYK算法

CYK算法是一个基于“动态规划”算法设计思想，用于测试串w对于一个上下文无关文法L的成员性的一个算法。CYK算法可以在O(n^5^)的时间内得出结果。CYK算法是由三个独立发现同样思想本质的人（J. Cocke、 D. Younger和T. Kasami）来命名的。

![image-20211109210757027](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211109210757027.png)

------

![img](file:///C:\Users\JIALON~1\AppData\Local\Temp\ksohtml\wps78BE.tmp.jpg)

基于上述文法和CYK算法，编程求句子**fish people fish tanks**的**最优分析树**。

# 实验步骤

## 数据预处理

首先规范要处理的文法格式，句法产生式每个终结符或者非终结符用空格隔开，在产生式后面加入**prob:** 表示发生的概率

```txt
S -> NP VP prob:0.9
S -> VP prob:0.1
VP -> V NP prob:0.5
VP -> V prob:0.1
VP -> V @VP_V prob:0.3
VP -> V PP prob:0.1
@VP_V -> NP PP prob:1.0
NP -> NP NP prob:0.1
NP -> NP PP prob:0.2
NP -> N prob:0.7
PP -> P NP prob:1.0
N -> people prob:0.5
N -> fish prob:0.2
N -> tanks prob:0.2
N -> rods prob:0.1
V -> people prob:0.1
V -> fish prob:0.6
V -> tanks prob:0.3
P -> with prob:1.0
```

在实验中规定以下变量来存储产生式

```python
non_terminal = set()
start_symbol = 'S'
terminal = set()
rules_prob = {}
```

| non_terminal | start_symbol | terminal | rules_prob                   |
| ------------ | ------------ | -------- | ---------------------------- |
| 非终结符     | 初始非终结符 | 终结符   | 产生语法规则集合（包含概率） |

使用了read_data(filename)函数对data.txt进行读取，并给上述变量完成数据初始化

```python
def read_data(filename):
    with open(filename, "r", encoding="utf-8") as x:
        data = x.readlines()
        for i in data:
            productions, prob = i.split("prob:")
            prob = float(prob)
            start, generations = productions.split("->")
            start = start.strip()
            generation = generations.split()
            if start not in non_terminal:
                non_terminal.add(start)
            if len(generation) == 1 and generation[0].islower():
                terminal.add(generation[0])
            if start not in rules_prob:
                new_adic = {}
                if len(generation) > 1:
                    new_adic[tuple(generation)] = prob
                    rules_prob[start] = new_adic
                if len(generation) == 1:
                    new_adic[generation[0]] = prob
                    rules_prob[start] = new_adic
            else:
                if len(generation) > 1:
                    rules_prob[start][tuple(generation)] = prob
                if len(generation) == 1:
                    rules_prob[start][generation[0]] = prob
```

## CYK算法

### 概述

给定一个句子s 和一个上下文无关文法PCFG，G=(T, N, S, R, P),定义一个跨越单词 i到j的概率最大的语法成分π: π(i,j,X)(i,j∈1…n ,X∈N)，目标是找到一个属于π[1,n,S]的所有树中概率最大的那棵。

1. T代表终端符集合
2. N代表非终端符集合
3. S代表初始非端结符
4. R代表产生语法规则集
5. P 代表每条产生规则的统计概率

伪代码:

```c++
function CKY(words, grammar):
    score = new double[(words)+1][(words)+1][(nonterms)]
    back = new Pair[(words)+1][(words)+1][(nonterms)]
    for i=0; i<(words); i++
        for A in nonterms
            if A -> words[i] in grammar
                score[i][i+1][A] = P(A -> words[i])
        boolean added = true
        while added
            added = false
            for A, B in nonterms
                if score[i][i+1][B] > 0 && A->B in grammar
                    prob = P(A->B)*score[i][i+1][B]
                    if prob > score[i][i+1][A]
                        score[i][i+1][A] = prob
                        back[i][i+1][A] = B
            added = true
    for span = 2 to words
        for begin = 0 to words - span
            end = begin + span
            for split = begin+1 to end-1
                for A,B,C in nonterms
                    prob=score[begin][split][B]*score[split][end][C]*P(A->BC)
                        if prob > score[begin][end][A]
                            score[begin]end][A] = prob
                            back[begin][end][A] = new Triple(split,B,C)
                boolean added = true
                while added
                    added = false
                    for A, B in nonterms
                        prob = P(A->B)*score[begin][end][B];
                            if prob > score[begin][end][A]
                                score[begin][end][A] = prob
                                back[begin][end][A] = B
                    added = true
    //返回最佳路径树
    return buildTree(score, back)
```

 score存放最大概率，back存放分裂点信息以便回溯，在接下来的具体算法实现，将用特别的数据结构实现数据信息的存储。

| score\[0][0] | score\[0][1]     | **score\[0][2]** | score\[0][3]     |
| ------------ | ---------------- | ---------------- | ---------------- |
|              | **score\[1][1]** | **score\[1][2]** | **score\[1][3]** |
|              |                  | **score\[2][2]** | **score\[2][3]** |
|              |                  |                  | **score\[3][3]** |

用矩阵的方式存储信息，以每个单词作为对角线上的元素，也就是树结构的叶结点。运用动态规划的思想进行填表，直到右上角计算出来，整棵树的结点信息就全部计算处理。

### 构建

在本实验中，构建了my_CYK(object)类来执行cyk算法，在\__init__中初始化了非终结符，终结符，初始非终结符，产生语法规则集合

```python
class my_CYK(object):
    def __init__(self, non_ternimal, terminal, rules_prob, start_prob):
        self.non_terminal = non_ternimal
        self.terminal = terminal
        self.rules_prob = rules_prob
        self.start_symbol = start_prob
```

parse_sentence（self,sentence）函数对输入的sentence进行分析，将字典和列表两种数据结构结合，实现概率的存储和路径信息的保存。

```python
word_list = sentence.split()
best_path = [[{} for _ in range(len(word_list))] for _ in range(len(word_list))]
for i in range(len(word_list)):
    for j in range(len(word_list)):
        for x in self.non_terminal:
            best_path[i][j][x] = {'prob': 0.0, 'path': {'split': None, 'rule': None}}
```

### 叶节点

本次实验的文法规则满足右部或者是两个非终端符或者是一个终端符的条件，所以是**CNF（乔姆斯基范式）**。

- 遍历非终端符，找到并计算此条非终端-终端语法的概率
- 生成新的语法需要加入

```python
for i in range(len(word_list)):
    for x in self.non_terminal:
        if word_list[i] in self.rules_prob[x].keys():
            best_path[i][i][x]['prob'] = self.rules_prob[x][word_list[i]] 
            best_path[i][i][x]['path'] = {'split': None, 'rule': word_list[i]} 
            for y in self.non_terminal:
                if x in self.rules_prob[y].keys():
                    best_path[i][i][y]['prob'] = self.rules_prob[x][word_list[i]] * self.rules_prob[y][x]
                    best_path[i][i][y]['path'] = {'split': i, 'rule': x}
```

### 非叶节点

```python
for l in range(1, len(word_list)):
    for i in range(len(word_list) - l):
        j = i + l
        for x in self.non_terminal:
            tmp_best_x = {'prob': 0, 'path': None}

            for key, value in self.rules_prob[x].items():
                if key[0] not in self.non_terminal:
                    break     
                for s in range(i, j): 
                    if len(key) == 2:
                        tmp_prob = value * best_path[i][s][key[0]]['prob'] * best_path[s + 1][j][key[1]]['prob']
                    else:
                        tmp_prob = value * best_path[i][s][key[0]]['prob'] * 0
                    if tmp_prob > tmp_best_x['prob']:
                        tmp_best_x['prob'] = tmp_prob
                        tmp_best_x['path'] = {'split': s, 'rule': key} 
            best_path[i][j][x] = tmp_best_x 
```

 扩展的CYK算法需要处理一元语法规则，判断key的len值可以避免一元规则计算时候的数组越界。

 此步骤结束之后得到上三角每个结点的最大概率语法规则和分裂点路径，用于接下来路径回溯得到语法树。

### 构建语法树

构建经典的节点类

```python
class Node:
    def __init__(self, val=None):
        self.val = val
        self.l_child = []

    def add_child(self, node):
        self.l_child.append(node)
```

代码中使用到构建语法树的部分

```python
treenode = Node("")
back(best_path, 0, 3, 'S',treenode)
```

回溯算法

```python
def back(best_path, left, right, root, freenode,ind=0):
    node = best_path[left][right][root]
    if node['path']['split'] is not None:
        childnode = Node(root)
        freenode.add_child(childnode)
        if len(node['path']['rule']) == 2:
            back(best_path, left, node['path']['split'], node['path']['rule'][0], childnode,ind + 1)
            back(best_path, node['path']['split'] + 1, right, node['path']['rule'][1], childnode,ind+1)
        else:
            back(best_path, left, node['path']['split'], node['path']['rule'][0], childnode,ind + 1)
    else:
        childnode = Node(root)
        freenode.add_child(childnode)
        leafnode = Node(node['path']['rule'])
        childnode.add_child(leafnode)
```

### 结果打印

将构建的语法树打印成字符串形式，使用中括号嵌套的形式

```python
print("prob = ", best_path[0][len(word_list) - 1][self.start_symbol]['prob'])
global res
res = ''
def put2str(node):
    global res
    if node:
        res += node.val
    if node.l_child:
        for i in node.l_child:
            res += "["
            put2str(i)
            res += "]"
put2str(treenode)
print(res)
```

# 实验结果

score部分

| fish                                                         | people                                                       | fish                                                         | tanks                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **N -> fish** 0.2<br />**V -> fish** 0.6<br />**NP -> N** 0.14<br />**VP -> V** 0.06<br />**S -> VP** 0.006 | **NP ->NP NP** 0.0049<br />**VP -> V NP** 0.105<br />**S -> VP** 0.0105 | **NP ->NP NP** 6.86e-5<br />**VP -> V NP** 0.00147<br />**S -> NP VP** 8.82e-4 | **NP -> NP NP** 9.604e-7<br />**VP -> V NP** 2.058e-5<br />**S -> NP VP** 1.8522e-4 |
|                                                              | **N -> people** 0.5<br />**V -> people** 0.1<br />**NP ->N** 0.35<br />**VP -> V** 0.01<br />**S -> VP** 0.001 | **NP -> NP NP** 0.0049<br />**VP -> V NP** 0.007<br />**S -> NP VP** 0.0189 | **NP -> NP NP** 6.86e-5<br />**VP -> V NP** 9.8e-5<br />**S -> NP VP** 0.01323 |
|                                                              |                                                              | **N -> fish** 0.2<br />**V -> fish** 0.6<br />**NP -> N** 0.14<br />**VP -> V** 0.06<br />**S -> VP** 0.006 | **NP ->NP NP** 0.00196<br />**VP -> V NP** 0.042<br />**S -> VP** 0.0042 |
|                                                              |                                                              |                                                              | **N -> tanks** 0.2<br />**V -> tanks** 0.3<br />**NP -> N** 0.14<br />**VP -> V** 0.03<br />**S ->VP** 0.003 |

程序运行结果如图

![image-20211109211241286](C:\Users\jialongwu\AppData\Roaming\Typora\typora-user-images\image-20211109211241286.png)

最优分析树字符串形式
$$
[S[NP[NP[N[fish]]][NP[N[people]]]][VP[V[fish]][NP[N[tanks]]]]]
$$
生成的树状图

![img](data:image/png;base64,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)

结果正确
