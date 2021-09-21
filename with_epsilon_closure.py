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
	def __init__(self, name, alph):
		'''A Node Class for a state which is a part of a DFA'''
		self.name = name
		self.next = {}
		for symbol in alph:
			self.next[symbol] = None

class NFA:
	def __init__(self, alphabets, startstate):
		'''A Class for NFA and keeping it organised'''
		self.states = {}
		self.alph = alphabets + ["ε"]
		self.trn = {}		# transitions
		self.start = startstate
		self.end = []
		self.df = None
		self.addState(startstate)
	
	def addState(self, name):
		self.states[name] = StateNFA(name, self.alph)
		self.trn[name] = {}
		for symbol in self.alph:
			self.trn[name][symbol] = []
		self.df = pd.DataFrame(self.trn).T
	
	def next(self, state, symbol, goto):
		self.trn[state][symbol].append(goto)
		state = self.states[state]
		goto = self.states[goto]
		state.next[symbol].append(goto)
		self.df = pd.DataFrame(self.trn).T


class DFA:
	def __init__(self, alphabets, startstate):
		'''A Class for DFA and keeping it organised'''
		self.states = {}
		self.alph = alphabets
		self.trn = {}		# transitions
		self.start = startstate
		self.end = []
		self.df = None
		self.addState(startstate)
	
	def addState(self, name):
		self.states[name] = StateDFA(name, self.alph)
		self.trn[name] = {}
		self.df = pd.DataFrame(self.trn).T
	
	def next(self, state, symbol, goto):
		self.trn[state][symbol] = goto
		state = self.states[state]
		goto = self.states[goto]
		state.next[symbol] = goto
		self.df = pd.DataFrame(self.trn).T
		
def add_to_closure(r, symbol, rd):
	# print(f"\nr = {r}")
	# print(f"rd = {rd}")
	for s in r:
		if s not in rd:
			if len(s.next[symbol]):
				for temp in s.next[symbol]:
					if temp not in r: r.append(temp)
				rd.append(s)
				for todo in r:
					# print("\nNext Recursion Level\n")
					r = add_to_closure(r, symbol, rd)
	return r
	
	
def closure(state, nfa, symbol = "ε"):
	state = nfa.states[state]
	r = [state]
	rd = []
	r = add_to_closure(r, symbol, rd)
	return sorted([s.name for s in r])
	

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
nfa.addState("10")

# print(nfa.df)

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
nfa.next("9", "b", "10")

print(nfa.df)

def ε_closure(l, nfa):
	ts = []
	for i in l:
		ts += closure(i, nfa)
	return sorted(list(set(ts)))

print(ε_closure(["3", "8"], nfa))

# print(nfa.states)
