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

    def addTransition_dict(self, transitions):  # add dict to dict 将一个字典的内容添加到另一个字典
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addTransition(fromstate, state, tostates[state])

    def newBuildFromNumber(self, startnum):
        # change the states' representing number to start with the given startnum
        # 改变各状态的表示数字，使之从 startnum 开始
        translations = {}
        for i in self.states:
            translations[i] = startnum
            startnum += 1
        rebuild = FA(self.symbol)
        rebuild.setStart(translations[self.startstate])
        rebuild.addFinal(translations[self.finalstates[0]])
        # 多个终结状态不方便合并操作, 同时提供的合并操作可以保证只产生一个终结状态
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]


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

class Regex2NFA:
    def __init__(self, regex):
        self.regex = regex
        self.buildNFA()

    def displayNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministic_finite_state_machine')

    @staticmethod
    def getPriority(op):
        if op == line:
            return 1
        elif op == dot:
            return 2
        elif op == star:
            return 3
        else:  # left bracket 左括号
            return 0

    @staticmethod
    def basicstruct(inputch):  # Regex = a -> NFA
        state1 = 0
        state2 = 1
        basic = FA(set([inputch]))
        basic.setStart(state1)
        basic.addFinal(state2)
        basic.addTransition(state1, state2, inputch)
        return basic

    @staticmethod
    def linestruct(a, b):  # Regex = a | b -> NFA
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 0
        state2 = m2
        lineFA = FA(a.symbol.union(b.symbol))
        lineFA.setStart(state1)
        lineFA.addFinal(state2)
        lineFA.addTransition(lineFA.startstate, a.startstate, epsilon)
        lineFA.addTransition(lineFA.startstate, b.startstate, epsilon)
        lineFA.addTransition(a.finalstates[0], lineFA.finalstates[0], epsilon)
        lineFA.addTransition(b.finalstates[0], lineFA.finalstates[0], epsilon)
        lineFA.addTransition_dict(a.transitions)
        lineFA.addTransition_dict(b.transitions)
        return lineFA

    @staticmethod
    def dotstruct(a, b):  # Regex = a · b -> NFA
        [a, m1] = a.newBuildFromNumber(0)
        [b, m2] = b.newBuildFromNumber(m1 - 1)
        state1 = 0
        state2 = m2 - 1
        dotFA = FA(a.symbol.union(b.symbol))
        dotFA.setStart(state1)
        dotFA.addFinal(state2)
        dotFA.addTransition_dict(a.transitions)
        dotFA.addTransition_dict(b.transitions)
        return dotFA

    @staticmethod
    def starstruct(a):  # Regex = a* -> NFA
        [a, m1] = a.newBuildFromNumber(1)
        state1 = 0
        state2 = m1
        starFA = FA(a.symbol)
        starFA.setStart(state1)
        starFA.addFinal(state2)
        starFA.addTransition(starFA.startstate, a.startstate, epsilon)
        starFA.addTransition(starFA.startstate, starFA.finalstates[0], epsilon)
        starFA.addTransition(a.finalstates[0], starFA.finalstates[0], epsilon)
        starFA.addTransition(a.finalstates[0], a.startstate, epsilon)
        starFA.addTransition_dict(a.transitions)
        return starFA

    def buildNFA(self):
        tword = ''
        pre = ''
        symbol = set()
        # explicitly add dot to the expression 显式地为正则式添加连接符
        for ch in self.regex:
            if ch in alphabet:
                symbol.add(ch)
            if ch in alphabet or ch == leftBracket:
                if pre != dot and (pre in alphabet or pre in [star, rightBracket]):
                    tword += dot
            tword += ch
            pre = ch
        self.regex = tword
        # convert infix expression to postfix expression 将中缀表达式转换为后缀表达式
        tword = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                tword += ch
            elif ch == leftBracket:
                stack.append(ch)
            elif ch == rightBracket:
                while (stack[-1] != leftBracket):
                    tword += stack[-1]
                    stack.pop()
                stack.pop()  # pop left bracket 弹出左括号
            else:
                while (len(stack) and Regex2NFA.getPriority(stack[-1]) >= Regex2NFA.getPriority(ch)):
                    tword += stack[-1]
                    stack.pop()
                stack.append(ch)
        while (len(stack) > 0):
            tword += stack.pop()
        self.regex = tword
        # build ε-NFA from postfix expression 由后缀表达式构建ε-NFA
        self.automata = []
        for ch in self.regex:
            if ch in alphabet:
                self.automata.append(Regex2NFA.basicstruct(ch))
            elif ch == line:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.linestruct(a, b))
            elif ch == dot:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.dotstruct(a, b))
            elif ch == star:
                a = self.automata.pop()
                self.automata.append(Regex2NFA.starstruct(a))
        self.nfa = self.automata.pop()
        self.nfa.symbol = symbol

if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as x:
        regex = x.read()
    a = Regex2NFA(regex)
    a.nfa.mywrite()