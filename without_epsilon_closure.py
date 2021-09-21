from string import ascii_uppercase # Helps to name the states automatically on entering number of states
import pandas as pd # Used only to visualize the transition states
# Go to line 130 to see detailed explanation

def tablify(fa , mode = "t"):
	'''
	Makes a table out of the input values
	'''
	dict1 =  {}
	i = 0
	for state in fa["Q"]:
		try: dict1[state] = fa["d"][i]
		except IndexError: pass
		i += 1
	if mode == "d": return dict1
	df = pd.DataFrame(dict1).T
	if mode == "t": return df


def inputNFA():
	'''
	This function asks the user specific questions and helps him to
	give an NFA as an input. This NFA will be converted to a DFA soon.
	
	Note:- This code is not writen for tackling bad user inputs.
		It will malfunction or even crash for unexpected inputs.
	'''
	# Taking input
	NFA = {}
	Qi = int(input("Enter the number of states (non-zero integer value less than 27 is expected): "))
	NFA["Q"] = [c for c in ascii_uppercase[:Qi]]
	print(f"Q = {NFA['Q']}\n")

	print("Let 'A' is the starting state.")
	NFA["q"] = "A"
	print(f"q = {NFA['q']}\n")

	E = input("Enter the alphabets with a space between them: ")
	NFA['E'] = E.split()
	print(f"E = {NFA['E']}\n")

	while True:
		F = input("Enter the final states with a space between them: ").upper()
		F = F.split()
		if set(F).issubset(set(NFA['Q'])):
			NFA["F"] = F
			break
		else: print("Final states must be a subset of Q.\n")
	print(f"F = {NFA['F']}\n")

	print("Enter the names of states below with a SPACE BETWEEN THEM. (Keep blank for null state)")
	ds = []
	for state in NFA["Q"]:
		d = []
		for alphabet in NFA["E"]:
			while True:
				a = input(f"Reading {alphabet} at state {state} takes automata to: ").upper()
				a = a.split()
				a.sort()
				# print(a)
				if set(a).issubset(set(NFA['Q'])):
					if a: d.append(a)
					else: d.append([""])
					break
				else:
					print("Please enter a valid name of state.\n")
		ds.append(d)
		# print(d)
	NFA["d"] = ds
	# print(f"d = {NFA['d']}\n")
	# PHEW! Completed taking input!
	
	NFA["table"] = tablify(NFA, "d")
	
	return NFA


def ADD(elemi, nfa, dfa):
	'''
	This function helps to find a state (elmi variable) and adds that to the DFA.
	'''
	global to_add
	dfa["table"][elemi] = []
	# print(dfa)
	table = nfa["table"]
	elem = list(elemi)
	for index in range(len(nfa["E"])):
		s = []
		for e in elem:
			for f in table[e][index]:
				for ind in f:
					if ind not in s: s.append(ind)
		s = list(set(s))
		s.sort()
		# print(s)
		text = ""
		for v in s: text += v
		if text not in to_add and text not in dfa["table"].keys():
			to_add.append(text)
		dfa["table"][elemi].append(text)
	# df = pd.DataFrame(dfa["table"]).T
	# df.columns = nfa["E"]
	# print("\n\n\tDFA\n", df, "\n")
	to_add.remove(elemi)
	# print(f"to_add = {to_add}\n")
		
	
def NFAtoDFA(nfa, dfa):
	'''
	Main Recursive Function
	'''
	global to_add
	ADD(to_add[0], nfa, dfa)
	if len(to_add):
		NFAtoDFA(nfa, dfa)

NFA = inputNFA()
print(f"\nNFA = {NFA}\n\n")
print("\tInput NFA:\n", tablify(NFA), "\n")

# Calculating

to_add = ["A"]

DFA = {}
DFA["E"] = NFA["E"] # Copying some common feature
DFA["q"] = NFA["q"] # Copying some common feature
DFA["table"] = {}

NFAtoDFA(NFA, DFA) # calling the main function which works recursively.
# We have added the first element to "to_add" manually. So it starts from there.
# Once it starts adding states, it adds the names of states it has to find in the "to_add" list.
# By finding I mean finding all the resultant states.
# How does it know which ones it has to find?
# It adds all the resultant states to "to_add" if:
#       1) It is not already in "to_add"
#       2) It has not already been found
# Once it completes finding a state, it removes that name from the "to_add" list.
# Then it keeps on calculating all the states recursively until "to_add" gets empty.


DFA["Q"] = list(DFA["table"].keys())
DFA["d"] = list(DFA["table"].values())
t = []
for f in NFA["F"]:
	for st in DFA["Q"]:
		if f in st and st not in t:
			t.append(st)
DFA["F"] = t
	
print("\n\tOutput DFA:")

print("Input Symbols are", end = " ")
for x in DFA["E"][:-1]:
	print(x + ",", end = " ")
print(f"\b\b and {DFA['E'][-1]}." )

print("States are", end = " ")
for x in DFA["Q"][:-1]:
	print("{" + x + "},", end = " ")
print("\b\b and {" + DFA['Q'][-1] + "}." )

print(f"Starting state is 'A'.")

df = pd.DataFrame(DFA["table"]).T
df.columns = NFA["E"]
print("Transitions:\n", df)

print("Final states are", end = " ")
for x in DFA["F"][:-1]:
	print("{" + x + "},", end = " ")
print("\b\b and {" + DFA['F'][-1] + "}." )
