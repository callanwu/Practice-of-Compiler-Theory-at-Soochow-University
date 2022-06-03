from collections import defaultdict
star = '*'
line = '|'
dot = '·'
leftBracket, rightBracket = '(', ')'
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)]
epsilon = 'e'
class FA:
    def __init__(self, symbol=set([])):
        self.states = set()
        self.symbol = symbol  # input symbol 输入符号表
        self.transitions = defaultdict(defaultdict)
        self.startstate = None
        self.finalstates = []
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
    def addFinal(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)
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
    def init(self, sta, sym, trans, startsta, finalsta):
        self.states = sta
        self.symbol = sym
        self.transitions = trans
        self.startstate = startsta
        self.finalstates = finalsta
    def getEpsilonClosure(self, findstate):
        allstates = set()
        states = [findstate]
        while len(states):
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tos in self.transitions[state]:
                    if epsilon in self.transitions[state][tos] and \
                            tos not in allstates:
                        states.append(tos)
        return allstates
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
class NFA2DFA:
    def __init__(self, nfa):
        self.buildDFA(nfa)
    def buildDFA(self, nfa):  # subset method 子集法
        allstates = dict()  # visited subset
        eclosure = dict()  # every state's ε-closure
        state1 = nfa.getEpsilonClosure(nfa.startstate)
        eclosure[nfa.startstate] = state1
        cnt = 1  # the number of subset, dfa state id
        dfa = FA(nfa.symbol)
        dfa.setStart(cnt)
        states = [[state1, dfa.startstate]]  # unvisit
        allstates[cnt] = state1
        cnt += 1
        while len(states):
            [state, fromindex] = states.pop()
            for ch in dfa.symbol:
                trstates = nfa.getMove(state, ch)
                for s in list(trstates):  # 转化为list, 相当于使用了一个临时变量
                    if s not in eclosure:
                        eclosure[s] = nfa.getEpsilonClosure(s)
                    trstates = trstates.union(eclosure[s])
                if len(trstates):
                    if trstates not in allstates.values():
                        states.append([trstates, cnt])
                        allstates[cnt] = trstates
                        toindex = cnt
                        cnt += 1
                    else:
                        toindex = [k for k, v in allstates.items() if v == trstates][0]
                    dfa.addTransition(fromindex, toindex, ch)
            for value, state in allstates.items():
                if nfa.finalstates[0] in state:
                    dfa.addFinal(value)
            self.dfa = dfa
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
    P.init(sta,symbol,adic,startsta,finalstates)
    D = NFA2DFA(P)
    D.dfa.mywrite()