from pprint import pprint
import pandas as pd

class StateNFA:
    def __init__(self, name, alph):
        '''A Node Class for a state which is a part of an NFA'''
        self.name = name
        self.next = {}
        for symbol in alph:
            self.next[symbol] = []

class StateDFA:
    def __init__(self, name, alias, alph):
        '''A Node Class for a state which is a part of a DFA'''
        self.name = name
        self.alias = alias
        self.next = {}
        for symbol in alph:
            self.next[symbol] = None

class NFA:
    def __init__(self, alphabets, startstate):
        '''A Class for NFA and keeping it organised'''
        self.states = {}
        self.alph = alphabets + ["ε"]
        self.trn = {}       # transitions
        self.start = startstate
        self.end = []
        self.df = pd.DataFrame(self.trn).T
        self.addState(startstate)
    
    def addState(self, name):
        '''
        Adds a state to the NFA
        '''
        self.states[name] = StateNFA(name, self.alph)
        self.trn[name] = {}
        for symbol in self.alph:
            self.trn[name][symbol] = []
        self.next(name, "ε", name)
        self.df = pd.DataFrame(self.trn).T
    
    def next(self, state, symbol, goto):
        '''
        Define transition to next state.
        Call this function multiple times if there are more than one states.
        '''
        self.trn[state][symbol].append(goto)
        state = self.states[state]
        goto = self.states[goto]
        state.next[symbol].append(goto)
        self.df = pd.DataFrame(self.trn).T
        
    def closure(self, state, symbol = "ε"):
        state = nfa.states[state]
        r = state.next[symbol]
        rd = []
        
        while r != rd:
            for s in r:
                if s not in rd:
                    for temp in s.next[symbol]:
                        if temp not in r:
                            r.append(temp)
                    rd.append(s)
        
        fuck = sorted([s.name for s in r])
        return fuck
        
    def ε_closure(self, l, symbol = "ε"):
        ts = []
        for i in l:
            ts += self.closure(i, symbol)
        ts = sorted(list(set(ts)))
        return ts

class DFA:
    def __init__(self, alphabets):
        '''A Class for DFA and keeping it organised'''
        self.states = {}
        self.aliases = {}
        self.alph = alphabets
        self.trn = {}       # transitions
        self.start = None
        self.end = []
        self.df = pd.DataFrame(self.trn).T
    
    def addState(self, name, alias):
        '''
        Adds a state to the DFA
        '''
        self.states[name] = StateDFA(name, alias, self.alph)
        self.trn[name] = {}
        self.states[name].alias = alias
        self.aliases[name] = alias
        self.df = pd.DataFrame(self.trn).T
    
    def next(self, state, symbol, goto):
        '''
        Define transition to next state
        '''
        self.trn[state][symbol] = goto
        state = self.states[state]
        goto = self.states[goto]
        state.next[symbol] = goto
        self.df = pd.DataFrame(self.trn).T

def NFA_to_DFA(nfa):
    '''
    Knows when to add which state from the to_add list and adds them
    to the DFA with the help of the ADD() function. This function actually
    sews the whole code at one place and organises all the functions.
    '''
    n = 0
    to_add = []
    dfaAlphabets = nfa.alph
    dfaAlphabets.remove("ε")
    dfa = DFA(alphabets = dfaAlphabets)
    to_add, n = ADD(["0"], to_add, n, nfa, dfa)
    while len(to_add):
        to_add, n = ADD(list(dfa.aliases[to_add[0]]), to_add, n, nfa, dfa)
        to_add = to_add[1:]
    x = []
    for key, value in dfa.aliases.items():
        for g in nfa.end:
            if g in value: x.append(key)
    x = sorted(list(set(x)))
    dfa.end = x
    return dfa

def makeAlias(r):
    '''Function to make an alias name for a state'''
    ret = ""
    for i in r:
        ret += i
    return ret


def ADD(state, to_add, n, nfa, dfa):
    '''
    Helps to find the transition states for a state which is there in
    the DFA according to the NFA provided. It also ads that to the DFA.
    '''
    a = nfa.ε_closure(state, symbol = "ε")
    alias = makeAlias(a)
    if alias not in dfa.aliases.values():
        dfa.addState(f"q{n}", alias)
        to_add.append(f"q{n}")
        n += 1
    parent = list(dfa.aliases.keys())[list(dfa.aliases.values()).index(alias)]
    for symbol in dfa.alph:
        b = nfa.ε_closure(nfa.ε_closure(a, symbol))
        alias = makeAlias(b)
        if alias not in dfa.aliases.values():
            dfa.addState(f"q{n}", alias)
            to_add.append(f"q{n}")
            n+=1
        child = list(dfa.aliases.keys())[list(dfa.aliases.values()).index(alias)]
        dfa.next(parent, symbol, child)
    return to_add, n


## Example
# Making the NFA....
# Step 1:- 
nfa = NFA(alphabets = ["a", "b"], startstate = "0")
nfa.addState("1")
nfa.addState("2")
nfa.addState("3")
nfa.addState("4")
nfa.addState("5")
nfa.addState("6")
nfa.addState("7")
nfa.addState("8")
nfa.addState("9")
nfa.addState("A")

nfa.next("0", "ε", "1")
nfa.next("0", "ε", "7")
nfa.next("1", "ε", "2")
nfa.next("1", "ε", "4")
nfa.next("2", "a", "3")
nfa.next("3", "ε", "6")
nfa.next("4", "b", "5")
nfa.next("5", "ε", "6")
nfa.next("6", "ε", "1")
nfa.next("6", "ε", "7")
nfa.next("7", "a", "8")
nfa.next("8", "b", "9")
nfa.next("9", "b", "A")

nfa.end = ["A"]

print(f"\tInput NFA\n{nfa.df}\n")

dfa = NFA_to_DFA(nfa)
print(f"Output DFA\n{dfa.df}\n")
pprint(dfa.aliases)
print(dfa.end)
