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
		self.trn = {}		# transitions
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
		# print(f"closure state = {state} symbol = {symbol}")
		state = nfa.states[state]
		r = state.next[symbol]
		#print(f"Abra Kadabra r = {[kill.name for kill in r]}")
		# print(state.name)
		rd = []
		
		while r != rd:
			# print(f"\nr = {[goo.name for goo in r]}")
			# print(f"rd = {[goo.name for goo in rd]}")
			for s in r:
				# print(f"s = {s.name}")
				if s not in rd:
					# print("s was not in rd, so proceeding")
					for temp in s.next[symbol]:
						if temp not in r:
							r.append(temp)
					rd.append(s)
		
		fuck = sorted([s.name for s in r])
		# print(f"fuck = {fuck}")
		return fuck
		
	def ε_closure(self, l, symbol = "ε"):
		ts = []
		for i in l:
			# print("ε_closure")
			ts += self.closure(i, symbol)
		ts = sorted(list(set(ts)))
		# print(f"ts = {ts}")
		# if symbol == "ε":
		# 	print("Returning ts as it is because symbol is epsilon")
		return ts
		# else:
		# 	print(f"But returning {[x for x in ts if x not in l]}")
		# 	return [x for x in ts if x not in l]

class DFA:
	def __init__(self, alphabets):
		'''A Class for DFA and keeping it organised'''
		self.states = {}
		self.aliases = {}
		self.alph = alphabets
		self.trn = {}		# transitions
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
	n = 0
	to_add = []
	dfaAlphabets = nfa.alph
	dfaAlphabets.remove("ε")
	dfa = DFA(alphabets = dfaAlphabets)
	to_add, n = ADD(["0"], to_add, n, nfa, dfa)
	while len(to_add):
		to_add, n = ADD(list(dfa.aliases[to_add[0]]), to_add, n, nfa, dfa)
		# print(to_add)
		to_add = to_add[1:]
	return dfa

def makeAlias(r):
	ret = ""
	for i in r:
		ret += i
	return ret

def ADD(state, to_add, n, nfa, dfa):
	a = nfa.ε_closure(state, symbol = "ε")
	# print(f"a = {a}")
	alias = makeAlias(a)
	if alias not in dfa.aliases.values():
		dfa.addState(f"q{n}", alias)
		# print(f"making state q{n}")
		to_add.append(f"q{n}")
		n += 1
		# print(f"n' = {n}")
	parent = list(dfa.aliases.keys())[list(dfa.aliases.values()).index(alias)]
	for symbol in dfa.alph:
		# print(f"symbol = {symbol}")
		x = nfa.ε_closure(a, symbol)
		# print(f"x = {x}")
		b = nfa.ε_closure(x)
		# print(f"b = {b}")
		alias = makeAlias(b)
		# print(f"alias(q{n}) = {alias}")
		if alias not in dfa.aliases.values():
			dfa.addState(f"q{n}", alias)
			# print(f"making state q{n}")
			to_add.append(f"q{n}")
			n+=1
			# print(f"n = {n}")
		child = list(dfa.aliases.keys())[list(dfa.aliases.values()).index(alias)]
		dfa.next(parent, symbol, child)
		
	# print(dfa.df)
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

print(f"\tInput NFA\n{nfa.df}\n")

dfa = NFA_to_DFA(nfa)
print(f"Output DFA\n{dfa.df}\n")
pprint(dfa.aliases)