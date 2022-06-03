ACTION = []
GOTO = []
grams = []
FIRST = {}
FOLLOW = {}
with open("data.txt", "r", encoding="utf-8") as x:
    grams = [i.strip().replace("id", "b") for i in x.readlines()]
dot_grams = []
VN = []
VN2Int = {}  # 非终结符映射
VT2Int = {}  # 终结符映射
VT = []
Vs = ["#"]
items = []

NodeSymbol = []


class Node:
    def __init__(self, val=None):
        self.val = val
        self.l_child = []

    def add_child(self, node):
        self.l_child.append(node)


location = 0  # 输入位置
status_stack = []  # 状态栈
symbol_stack = []  # 符号栈
now_state = ''  # 栈顶状态
input_ch = ''  # 栈顶字符
input_str = ''  # 输入串
now_step = 0  # 当前步骤


# print(grams)


# ------------------预处理---------------#

# 划分终结符和非终结符
def get_v():
    vn_num = 0
    vt_num = 0
    for s in grams:
        x, y = s.split("->")
        # print(x,y)
        if x not in VN:
            VN.append(x)
            VN2Int.update({x: vn_num})
            vn_num = vn_num + 1
        for v in y:
            if v.isupper():
                if v not in VN:
                    VN.append(v)
                    VN2Int.update({v: vn_num})
                    vn_num = vn_num + 1
            else:
                if v not in VT:
                    VT.append(v)
                    VT2Int.update({v: vt_num})
                    vt_num = vt_num + 1

    for vn in VN:
        Vs.append(vn)
    for vt in VT:
        Vs.append(vt)

    VT.append("#")
    VT2Int.update({"#": vt_num})
    print("得到非终结符集合：" + str(VN))
    print("得到终结符集合：" + str(VT))
    print("所有的符号集合" + str(Vs))


def dot_gram():
    # 为所有产生式加点
    dot_grams.append("S->.E")
    dot_grams.append("S->E.")

    for gram in grams:
        ind = gram.find("->")
        for i in range(len(gram) - ind - 1):
            tmp = gram[:ind + 2 + i] + "." + gram[ind + 2 + i:]
            # print(tmp)
            dot_grams.append(tmp)


# print(str(dot_grams))


# ------------构造DNF代码---------------------#

def get_VN_gram(v):
    # 返回非终结符产生的A->.aBb形式
    res = []
    for gram in dot_grams:
        ind = gram.find("->")
        if gram[0] == v and gram[ind + 2] == ".":
            res.append(gram)
    return res


# print(get_VN_gram("A"))


def get_CLOSURE(tmp):
    # 生成闭包
    CLOSURE = []
    for it in tmp:
        if it not in CLOSURE:
            CLOSURE.append(it)
        x, y = it.split(".")
        if y == "":
            continue
        v = y[0]
        if v in VN:
            res = get_VN_gram(v)
            for re in res:
                if re not in CLOSURE:
                    CLOSURE.append(re)
                    tmp.append(re)
    return CLOSURE


def is_inItems(new_item):
    # 判断item是否已经存在, 存在返回位置，不存在返回-1

    if new_item is None:
        return -1

    new_set = set(new_item)
    num = 0
    for item in items:
        old_set = set(item)
        if old_set == new_set:
            return num
        num = num + 1

    return -1


def go(item, v):
    # 生成并返回下一个item
    tmp = []
    for it in item:
        x, y = it.split(".")
        if y != "":
            if y[0] == v:
                new_it = x + y[0] + "." + y[1:]
                tmp.append(new_it)

    if len(tmp) != 0:
        new_item = get_CLOSURE(tmp)
        return new_item


def get_items():
    # 构建item的集合

    # 初始化,生成I0
    item = []
    init_s = "S->.E"
    item.append(init_s)
    dot_gram()

    for it in item:
        v = it[it.find(".") + 1]
        if v in VN:
            res = get_VN_gram(v)
            for re in res:
                if re not in item:
                    item.append(re)

    # print("I0 is :" + str(item))
    items.append(item)

    num = 0
    for item in items:
        for v in Vs:
            # print("item is %s," % str(item) + "v is %s" % v)
            new_item = go(item, v)
            # 判断状态不为空，且不存在于原状态中
            if new_item is not None:
                if is_inItems(new_item) == -1:
                    # print("添加了%s" % str(new_item))
                    items.append(new_item)

    # print_items()


# ---------------构造LR(0)表代码--------------#
def initail():
    for str in grams:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        FIRST[part_begin] = ""
        FOLLOW[part_begin] = "#"


def getFirst():
    for str in grams:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        if not part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + part_end[0]


def getFirst_2():
    for str in grams:
        part_begin = ''
        part_end = ''
        part_begin += str.split('->')[0]
        part_end += str.split('->')[1]
        if part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + FIRST.get(part_end[0])


def getFirst_3():
    while (1):
        test = FIRST
        getFirst_2()
        for i, j in FIRST.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FIRST[i] = temp
        if test == FIRST:
            break


def getFOLLOW_3():
    while (1):
        test = FOLLOW
        getFollow()
        ##去除重复项
        for i, j in FOLLOW.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FOLLOW[i] = temp
        if test == FOLLOW:
            break


##计算follow集的第一部分，先计算 S -> A b 类型的
def getFollow():
    for str in grams:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        ##如果是 S->a 直接推出终结符 则 continue
        if len(part_end) == 1:
            continue
        ##否则执行下面的操作
        else:
            # 将->后面的分开再倒序
            temp = []
            for i in part_end:
                temp.append(i)
            temp.reverse()
            # 如果非终结符在句型的末端则把"#" 加入进去
            if temp[0].isupper():
                FOLLOW[temp[0]] = FOLLOW.get(temp[0]) + FOLLOW.get(part_begin)
                temp1 = temp[0]
                for i in temp[1:]:
                    if not i.isupper():
                        temp1 = i
                    else:
                        if temp1.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp1).replace("e", "")
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp1
                        temp1 = i
            else:
                temp1 = temp[0]
                for i in temp[1:]:
                    if not i.isupper():
                        temp1 = i
                    else:
                        if temp1.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp1)
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp1
                        temp1 = i


def init_lr_table():
    for h in range(len(items)):
        ACTION.append([])
        GOTO.append([])
        for w1 in range(len(VT) + 1):
            ACTION[h].append("  ")
        for w2 in range(len(VN)):
            GOTO[h].append("  ")


def lr_is_legal():
    # 判别lr是否合法
    has_protocol = 0  # 是否存在规约项目
    has_shift = 0  # 是否存在移进项目
    for item in items:
        for it in item:
            x, y = it.split(".")
            if y == "":
                if has_protocol != 0 or has_shift != 0:
                    return False
                has_protocol = 1
            else:
                if y[0] in VT:
                    has_shift = 1
    return True


def find_gram(it):
    x, y = it.split(".")
    mgram = x + y
    try:
        ind = grams.index(mgram)
        return ind
    except ValueError:
        return -1


dot_gram()
print(dot_grams[1])
print(find_gram(dot_grams[1]))


def get_lr_table():
    initail()
    getFirst()
    getFirst_2()
    getFirst_3()
    getFirst_3()
    getFollow()
    getFOLLOW_3()
    # 构建lr分析表
    init_lr_table()
    lr_is_legal()
    i = 0
    j = 0
    for item in items:
        for it in item:
            x, y = it.split(".")
            if y == "":  # 判断是否写入ACTION
                if it == "S->E.":
                    ACTION[i][len(VT) - 1] = "acc"
                ind = find_gram(it)
                if ind != -1:
                    for j in FOLLOW[x[0]]:
                        k = VT2Int[j]
                        ACTION[i][k] = "r" + str(ind + 1)
            else:
                next_item = go(item, y[0])
                # print("go(%s, %s)-->%s" % (str(item), y[0], str(next_item)))
                ind = is_inItems(next_item)
                if ind != -1:  # 判断是否写入GOTO
                    if y[0] in VT:
                        j = VT2Int[y[0]]
                        ACTION[i][j] = "s" + str(ind)
                    if y[0] in VN:
                        j = VN2Int[y[0]]
                        GOTO[i][j] = ind
        i = i + 1
    print_lr_table()


# -----------------规约------------------#
def is_end():
    if input_str[location:len(input_str)] == '#':
        if symbol_stack[-1] == 'E' and symbol_stack[-2] == '#':
            output()
            return True
        else:
            return False
    else:
        return False
    return True


# 输出
def output():
    global now_step, status_stack, symbol_stack, input_str, now_state
    print('%d\t\t' % now_step, end='')
    now_step += 1
    print('%-20s' % status_stack, end='')
    print('%-50s' % symbol_stack, end='')
    print('%-30s' % input_str[location:len(input_str)], end='')


# 统计产生式右部的个数
def count_right_num(grammar_i):
    return len(grammar_i) - 3


def stipulations():
    # 根据LR(0)表进行规约

    global location
    print('----分析过程----')
    print("index\t\t", end='')
    print('%-20s' % 'Status', end='')
    print('%-50s' % 'Symbol', end='')
    print('%-30s' % 'Input', end='')
    print('Action')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()

    symbol_stack.append('#')
    status_stack.append(0)
    while not is_end():
        now_state = status_stack[-1]
        input_ch = input_str[location]
        if input_ch not in Vs:
            print(input_ch)
            print("错误字符")
            return -1
        output()
        find = ACTION[now_state][VT2Int[input_ch]]

        if find[0] == 's':  # 进入action
            num = "".join(find[1:])
            symbol_stack.append(input_ch)
            status_stack.append(int(num))
            NodeSymbol.append(Node(input_ch))
            location += 1
            print('action[%s][%s]=s%s' % (now_state, input_ch, num))

        elif find[0] == 'r':  # 进入goto
            num = "".join(find[1:])
            num = int(num)
            g = grams[num - 1]
            right_num = count_right_num(g)
            # print("\n%s"%g)
            for i in range(right_num):
                status_stack.pop()
                symbol_stack.pop()

            node = Node(g[0])
            for i in range(right_num):
                node.add_child(NodeSymbol.pop())
            node.l_child.reverse()
            NodeSymbol.append(node)

            symbol_stack.append(g[0])
            now_state = status_stack[-1]
            symbol_ch = symbol_stack[-1]
            find = GOTO[now_state][VN2Int.get(symbol_ch, -1)]
            if find == -1:
                print('分析失败')
                return -1
            status_stack.append(find)
            print('%s' % g)
        else:
            return -1
    print("\n is done")
    return 0


# ----------------print代码--------------#

def print_grams():
    print("----产生式集合----")
    num = 1
    for gram in grams:
        print("(%d)%s" % (num, str(gram)))
        num = num + 1


def print_items():
    print("----状态集合----")
    num = 0
    for it in items:
        print("(%d)%s" % (num, str(it)))
        num = num + 1


def print_lr_table():
    # 表头
    print('----LR分析表----')
    print('\t\t|\t', end='')
    print(('%4s' % '') * (len(VT) - 3), end='')
    print('Action', end='')
    print(('%4s' % '') * (len(VT) - 3), end='')
    print('\t|\t', end='')
    print(('%3s' % '') * (len(VN) - 2), end='')
    print('GOTO', end='')
    print(('%3s' % '') * (len(VN) - 2), end='')
    print('\t|')
    print('\t\t\t', end='')
    for i in VT:
        print('%3s\t' % i, end='')
    print('\t|\t', end='')
    k = 0
    for i in VN:
        print('%3s\t' % i, end='')
    print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()
    # 表体
    for i in range(len(items)):
        print('%5d\t|\t' % i, end='')
        for j in range(len(VT)):
            print('%4s' % ACTION[i][j], end='')
        print('\t|\t', end='')
        for j in range(len(VN)):
            if not GOTO[i][j] == -1:
                print('%4s' % GOTO[i][j], end='')
            else:
                print('\t', end='')
        print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()


def put2str(node):
    global res
    if node:
        res += node.val
    if node.l_child:
        for i in node.l_child:
            res += "["
            put2str(i)
            res += "]"


if __name__ == '__main__':
    get_v()  # 分割终结符和非终结符
    print_grams()  # 输出文法产生式
    get_items()  # 生成状态集合
    print_items()  # 输出状态集合
    get_lr_table()  # 生成lr分析表
    input_str = "id+(id+id)*id#"  # 待分析字符串
    input_str = input_str.replace("id", "b")
    stat = stipulations()  # 规约
    if stat == 0:
        print("\n %s 符合文法规则" % input_str)
    else:
        print("\n %s 不符合文法规则" % input_str)
    res = ""
    for i in NodeSymbol:
        put2str(i)
    res = '[' + res + ']'
    res = res.replace("b", "id")
    print(res)
