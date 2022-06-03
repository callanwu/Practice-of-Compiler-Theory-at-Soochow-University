from collections import defaultdict
from graphviz import Digraph
star = '*'
line = '|'
dot = '·'
leftBracket, rightBracket = '(', ')'
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)]
epsilon = 'e'
class FA:
    def init(self, sta, sym, trans, startsta, finalsta):
        self.states = sta
        self.symbol = sym
        self.transitions = trans
        self.startstate = startsta
        self.finalstates = finalsta
    def __init__(self, symbol=set([])):
        self.states = set()
        self.symbol = symbol  # input symbol 输入符号表
        self.transitions = defaultdict(defaultdict)
        self.startstate = None
        self.finalstates = []
    def getMove(self, state, skey):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if skey in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates
    def setStart(self, state):
        self.startstate = state
        self.states.add(state)

    def addFinal(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addTransition(self, fromstate, tostate, inputch):  # add only one 仅添加一条映射关系
        if isinstance(inputch, str):
            inputch = set([inputch])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions and tostate in self.transitions[fromstate]:
            self.transitions[fromstate][tostate] = \
                self.transitions[fromstate][tostate].union(inputch)
        else:
            self.transitions[fromstate][tostate] = inputch

    def newBuildFromEqualStates(self, equivalent, pos):
        # change states' number after merging
        # 在最小化合并状态后修改状态的表示数字
        rebuild = FA(self.symbol)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setStart(pos[self.startstate])
        for s in self.finalstates:
            rebuild.addFinal(pos[s])
        return rebuild

    def mywrite(self):
        with open("ouput.txt", "w", encoding="utf-8") as x:
            x.write("start state:" + str(self.startstate) + "\n")
            final = ""
            for i in self.finalstates:
                final += str(i) + " "
            x.write("accepting states:" + final + "\n")
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    tmp = ''
                    for s in tostates[state]:
                        tmp += s + '|'
                    x.write(str(fromstate) + "\t"  + tmp[:-1] + "\t" +str(state) + "\n")
class MinDfa:
    def __init__(self, nfa):
        self.dfa = nfa
    def displayminDFA(self):
        self.minDFA.display('mindfa.gv', 'min_deterministic_finite_state_machine')
    @staticmethod
    def reNumber(states, pos):  # renumber the sets' number begin from 1
        cnt = 1
        change = dict()
        for st in states:
            if pos[st] not in change:
                change[pos[st]] = cnt
                cnt += 1
            pos[st] = change[pos[st]]

    def minimise(self):  # segmentation 分割法, 生成新的状态集合
        states = list(self.dfa.states)
        tostate = dict(set())  # Move(every state, every symbol)
        # initialization 预处理出每个状态经一个输入符号可以到达的下一个状态
        for st in states:
            for sy in self.dfa.symbol:
                if st in tostate:
                    if sy in tostate[st]:
                        tostate[st][sy] = tostate[st][sy].union(self.dfa.getMove(st, sy))
                    else:
                        tostate[st][sy] = self.dfa.getMove(st, sy)
                else:
                    tostate[st] = {sy: self.dfa.getMove(st, sy)}
                if len(tostate[st][sy]):
                    tostate[st][sy] = tostate[st][sy].pop()
                else:
                    tostate[st][sy] = 0
        equal = dict()  # state sets 不同分组的状态集合
        pos = dict()  # record the set which state belongs to 记录状态对应的分组

        # initialization 2 sets, nonterminal states and final states
        equal = {1: set(), 2: set()}
        for st in states:
            if st not in self.dfa.finalstates:
                equal[1] = equal[1].union(set([st]))
                pos[st] = 1
        for fst in self.dfa.finalstates:
            equal[2] = equal[2].union(set([fst]))
            pos[fst] = 2

        unchecked = []
        cnt = 3  # the number of sets
        unchecked.extend([[equal[1], 1], [equal[2], 2]])
        while len(unchecked):
            [equalst, id] = unchecked.pop()
            for sy in self.dfa.symbol:
                diff = dict()
                for st in equalst:
                    if tostate[st][sy] == 0:
                        if 0 in diff:
                            diff[0].add(st)
                        else:
                            diff[0] = set([st])
                    else:
                        if pos[tostate[st][sy]] in diff:
                            diff[pos[tostate[st][sy]]].add(st)
                        else:
                            diff[pos[tostate[st][sy]]] = set([st])
                if len(diff) > 1:
                    for k, v in diff.items():
                        if k:
                            for i in v:
                                equal[id].remove(i)
                                if cnt in equal:
                                    equal[cnt] = equal[cnt].union(set([i]))
                                else:
                                    equal[cnt] = set([i])
                            if len(equal[id]) == 0:
                                equal.pop(id)
                            for i in v:
                                pos[i] = cnt
                            unchecked.append([equal[cnt], cnt])
                            cnt += 1
                    break
        if len(equal) == len(states):
            self.minDFA = self.dfa
        else:
            MinDfa.reNumber(states, pos)
            self.minDFA = self.dfa.newBuildFromEqualStates(equal, pos)
if __name__ == '__main__':
    adic = defaultdict(defaultdict)
    with open("input.txt", "r", encoding="utf-8") as x:
        lines = x.readlines()
    startsta = int(lines[0].split(":")[1])
    finalstates = [int(lines[1].split(":")[1])]
    sta = set([])
    symbol = set([])
    for i in range(2, len(lines)):
        lines[i] = lines[i].strip()
        a, b, c = lines[i].split()
        if b != "e":
            symbol.add(b)
        sta.add(int(a))
        sta.add(int(c))
        adic[int(a)][int(c)] = b
    P = FA(symbol)
    P.init(sta, symbol, adic, startsta, finalstates)
    D = MinDfa(P)
    D.minimise()
    D.minDFA.mywrite()