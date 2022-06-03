global i
i = 0
global flag
flag = True


class Node:
    def __init__(self, val=None):
        self.val = val
        self.l_child = []

    def add_child(self, node):
        self.l_child.append(node)


def E(p):
    print("E->TG")
    T1 = Node('T')
    G1 = Node('G')
    p.add_child(T1)
    p.add_child(G1)
    T(T1)
    G(G1)


def T(T):
    print("T->FS")
    F1 = Node('F')
    S1 = Node('S')
    T.add_child(F1)
    T.add_child(S1)
    F(F1)
    S(S1)


def G(g):
    global i
    if src[i] == "+":
        i += 1
        print("G->+TG")
        plus = Node("+")
        T1 = Node("T")
        G1 = Node("G")
        g.add_child(plus)
        g.add_child(T1)
        g.add_child(G1)
        T(T1)
        G(G1)
    else:
        print("G->e")
        e = Node("e")
        g.add_child(e)


def S(p):
    global i
    if src[i] == "*":
        print("S->*FS")
        time = Node("*")
        F1 = Node("F")
        S1 = Node("S")
        p.add_child(time)
        p.add_child(F1)
        p.add_child(S1)
        i += 1
        F(F1)
        S(S1)
    else:
        print("S->e")
        e = Node("e")
        p.add_child(e)


def F(p):
    global i
    global flag
    if src[i] == "(":
        i += 1
        left = Node("(")
        E1 = Node("E")
        E(E1)
        p.add_child(left)
        p.add_child(E1)
        if src[i] == ")":
            i += 1
            print("F->(E)")
            right = Node(")")
            p.add_child(right)
        else:
            flag = False
    elif src[i] == "id":
        print("F->id")
        id = Node("id")
        p.add_child(id)
        i += 1
    else:
        flag = False


src = "id + ( id + id ) * id"
src = src.split() + ["#"]
root = Node('E')
E(root)
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


if src[i] == "#" and flag:
    put2str(root)
    print("[" + res + "]")
else:
    print("input error!")
