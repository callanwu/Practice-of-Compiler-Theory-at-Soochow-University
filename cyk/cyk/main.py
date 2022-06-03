class Node:
    def __init__(self, val=None):
        self.val = val
        self.l_child = []

    def add_child(self, node):
        self.l_child.append(node)


class my_CYK(object):
    def __init__(self, non_ternimal, terminal, rules_prob, start_prob):
        self.non_terminal = non_ternimal
        self.terminal = terminal
        self.rules_prob = rules_prob
        self.start_symbol = start_prob

    def parse_sentence(self, sentence):
        word_list = sentence.split()
        best_path = [[{} for _ in range(len(word_list))] for _ in range(len(word_list))]
        for i in range(len(word_list)):  # 下标为0开始
            for j in range(len(word_list)):
                for x in self.non_terminal:  # 初始化每个字典，每个语法规则概率及路径为None，避免溢出和空指针
                    best_path[i][j][x] = {'prob': 0.0, 'path': {'split': None, 'rule': None}}
        for i in range(len(word_list)):  # 下标为0开始
            for x in self.non_terminal:  # 遍历非终端符，找到并计算此条非终端-终端语法的概率
                if word_list[i] in self.rules_prob[x].keys():
                    best_path[i][i][x]['prob'] = self.rules_prob[x][word_list[i]]  # 保存概率
                    best_path[i][i][x]['path'] = {'split': None, 'rule': word_list[i]}  # 保存路径
                    # 生成新的语法需要加入
                    for y in self.non_terminal:
                        if x in self.rules_prob[y].keys():
                            best_path[i][i][y]['prob'] = self.rules_prob[x][word_list[i]] * self.rules_prob[y][x]
                            best_path[i][i][y]['path'] = {'split': i, 'rule': x}
        for l in range(1, len(word_list)):
            # 该层结点个数
            for i in range(len(word_list) - l):  # 第一层：0,1,2
                j = i + l  # 处理第二层结点，（0,j=1）,(1,2),(2,3)   1=0+1,2=1+1.3=2+1
                for x in self.non_terminal:  # 获取每个非终端符
                    tmp_best_x = {'prob': 0, 'path': None}

                    for key, value in self.rules_prob[x].items():  # 遍历该非终端符所有语法规则
                        if key[0] not in self.non_terminal:
                            break
                        # 计算产生的分裂点概率，保留最大概率
                        for s in range(i, j):  # 第一个位置可分裂一个（0,0--1,1)
                            # for A in best_path[i][s]
                            if len(key) == 2:
                                tmp_prob = value * best_path[i][s][key[0]]['prob'] * best_path[s + 1][j][key[1]]['prob']
                            else:
                                tmp_prob = value * best_path[i][s][key[0]]['prob'] * 0
                            if tmp_prob > tmp_best_x['prob']:
                                tmp_best_x['prob'] = tmp_prob
                                tmp_best_x['path'] = {'split': s, 'rule': key}  # 保存分裂点和生成的可用规则
                    best_path[i][j][x] = tmp_best_x  # 得到一个规则中最大概率
        treenode = Node("")
        back(best_path, 0, 3, 'S',treenode)
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


non_terminal = set()
start_symbol = 'S'
terminal = set()
rules_prob = {}


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


def main(sentence):
    read_data("data.txt")
    cyk = my_CYK(non_terminal, terminal, rules_prob, start_symbol)
    cyk.parse_sentence(sentence)


if __name__ == "__main__":
    main("fish people fish tanks")
