#!/usr/bin/python
# -*- coding: UTF-8 -*-

resultado=""
producciones = {

	"P D P" : 1,
	"P F P" : 2,
	"P S P" : 3,
	"P SC P" : 4,
	"P  " : 5,

	"D var T id ;" : 6,
	
	"T int" : 7,
	"T string": 8,
	"T boolean" : 9,
	
	"F function T' id ( A ) { C }" : 10,
	
	"T' T" : 11,
	"T'  " : 12,
	
	"A  " : 13,
	"A T id A'" : 14,
	
	"A'  " : 15,
	"A' , T id A'": 16,

	"C D C" : 17,
	"C S C" : 18,
	"C  " :19,
	"C SC C" : 20,

	"S if ( E ) S" : 21,
	"S id O" : 22,
	"S print ( E ) ;": 23,
	"S input ( E ) ;" : 24,
	"S return X ;" : 25,

	"O = E ;" : 26,
	"O |= E ;" : 27,
	"O ( L ) ;" : 28,

	"L  " : 29,
	"L id L'": 30,

	"L'  " :31,
	"L' , id L'" : 32,
	"X E": 33,
	"X  ": 34,

	"SC for ( B ; E ; B' ) { C }": 35,

	"B id = E" : 36,
	"B  " : 37,

	"B' id B''" : 38,
	"B'  " : 39,

	"B'' = E": 40,
	"B'' |= E": 41,

	"E K E'" : 42,

	"E'  ": 43,
	"E' > K E'" : 44,

	"K ! K" : 45,
	"K U" : 46,

	"U V U'" : 47,

	"U'  " : 48,
	"U' + V U'": 49,

	"V id J": 50,
	"V cte_entera" : 51,
	"V cadena" : 52,
	"V ( E )" : 53,

	"J ( L )" : 54,
	"J  " : 55
}

class PredictiveParser(object):
	def is_terminal(self, sym):
		if not sym or sym[0].isupper():
			return False
		return True

	def is_nonterminal(self, sym):
		if not sym or not sym[0].isupper():
			return False
		return True

	def __init__(self, start, grammar):
		self.start = start
		self.grammar = grammar
		self.terminals = set()
		self.nonterminals = set()
		self.null_dict = self.gen_nullable()
		self.first_dict = self.gen_first()
		self.follow_dict = self.gen_follow()
		self.table = self.gen_table()

	def match(self, seq):
		seq.append('$')
		si = 0
		stack = ['$', self.start]
		top = self.start
		while top != '$':
			if top == seq[si]:
				si = si + 1
				stack.pop()
			elif (self.is_terminal(top)):
				return False
			else:
				try:
					prod = self.table[top, seq[si]]
					stack.pop()
					if prod != [""]:
						stack.extend(reversed(prod))
				except KeyError:
					return False
			top = stack[-1]
		return True

	def verbose_match(self, seq, display_stack=False):
    		global resultado
		seq.append('$')
		si = 0
		stack = ['$', self.start]
		top = self.start
		while top != '$':
			if display_stack:
				print ("Stack:", stack)
			if top == seq[si]:
				si = si + 1
				#print ("** Action: match `{0}`".format(top))
				stack.pop()
    					
			elif (self.is_terminal(top)):
				return False
			else:
				try:
					prod = self.table[top, seq[si]]
					stack.pop()
					if prod == [""]:
				#		print ("** Action: derive {0} on `{1}` to: ε".format(top, seq[si]))
						aux=str(top)+"  "
						aux = producciones.get(aux)
						resultado+=str(aux)+" "
						
						
					else:
				#		print ("** Action: derive {0} on `{1}` to: {2}".format(top, seq[si], " ".join(prod)))
						aux=str(top)+" " + str(" ".join(prod))
						aux = producciones.get(aux)
						resultado+=str(aux) + " "
						stack.extend(reversed(prod))
					with open("produciones.txt", 'w') as producc:
						producc.write("D " + resultado + "\n")
					
				except KeyError:
				#	print ("ERROR: Not able to find derivation of {0} on `{1}`".format(top, seq[si]))
					print("Se ha encontrado un {1}: No se esperaba un {1}").format(seq[si], seq[si])
					return False
			top = stack[-1]
		return True

	def gen_table(self):
		table = {}
		for head, prods in self.grammar.iteritems():
			for prod in prods:
				first_set = self.first(prod)
				for terminal in first_set - set([""]):
					table[head, terminal] = prod
				if "" in first_set:
					for terminal in self.follow_dict[head]:
						table[head, terminal] = prod
					if '$' in self.follow_dict[head]:
						table[head, '$'] = prod
		return table

	def print_table(self):
		for nonterminal in self.nonterminals:
			for terminal in self.terminals.union(set(['$'])):
				try:
					prod = self.table[nonterminal, terminal]
					print ("(" + nonterminal + ", " + terminal + ") =", )
					print (prod)
				except KeyError:
					pass

	def gen_nullable(self):
		null_dict = {"": True}
		for head, prods in self.grammar.iteritems():
			null_dict[head] = False
			self.nonterminals.add(head)
			for prod in prods:
				for symbol in prod:
					if self.is_terminal(symbol):
						null_dict[symbol] = False
						self.terminals.add(symbol)
					elif not symbol:
						null_dict[head] = True
		while True:
			changes = 0
			for head, prods in self.grammar.iteritems():
				for prod in prods:
					all_nullable = True
					for symbol in prod:
						if not null_dict[symbol]:
							all_nullable = False
							break
					if all_nullable and not (head in null_dict and null_dict[head]):
						null_dict[head] = True
						changes = changes + 1
			if changes == 0:
				return null_dict		

	def nullable(self, symbols):
		if not symbols:
			return True
		elif not self.null_dict[symbols[0]]:
			return False
		return self.nullable(symbols[1:])

	def gen_first(self):
		first_dict = {}
		for head, prods in self.grammar.iteritems():
			first_dict[head] = set()
			for prod in prods:
				for symbol in prod:
					if self.is_terminal(symbol):
						first_dict[symbol] = set([symbol])
		while True:
			changes = first_dict.copy()
			for head, prods in self.grammar.iteritems():
				for prod in prods:
					if not prod[0]:
						first_dict[head] = first_dict[head].union(set([""]))
					else:
						first_dict[head] = first_dict[head].union(first_dict[prod[0]])
					for i in xrange(1, len(prod)):
						if self.nullable(prod[:i]):
							if not prod[0]:
								first_dict[head] = first_dict[head].union(set([""]))
							else:
								first_dict[head] = first_dict[head].union(first_dict[prod[0]])
			if changes == first_dict:
				return first_dict

	def first(self, symbols):
		if not symbols:
			return set()
		if "" in symbols:
			return set([""])
		if not self.null_dict[symbols[0]]:
			return self.first_dict[symbols[0]]
		return self.first_dict[symbols[0]].union(self.first(symbols[1:]))

	def gen_follow(self):
		follow_dict = {}
		for head in self.grammar:
			if head == self.start:
				follow_dict[self.start] = set(["$"])
			else:
				follow_dict[head] = set()
		while True:
			changes = follow_dict.copy()
			for head, prods in self.grammar.iteritems():
				for prod in prods:

					for i in xrange(len(prod)-1):
						if self.is_nonterminal(prod[i]):
							follow_dict[prod[i]] = follow_dict[prod[i]].union(self.first(prod[i+1:]) - set([""]))	

					for i in reversed(xrange(len(prod))):
						if self.is_nonterminal(prod[i]) and self.nullable(prod[i+1:]):
							follow_dict[prod[i]] = follow_dict[prod[i]].union(follow_dict[head])

			if changes == follow_dict:
				return follow_dict	

