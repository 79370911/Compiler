#!/usr/bin/env python
# encoding:utf-8

import sys
import string
import colors
'''
Grammar:
E -> A(E, E)
E -> epsilon
A -> a|b|...|z

First(E) = {a, b, ... , z, epsilon}
First(A) = {a, b, ... , z}

Follow(E) = {',', )}
Follow(A) = {(}

Select(E -> A(E, E)) = {a, b, ... , z}
Select(E -> epsilon) = {',', )}
Select(A -> a|b|...|z) = {a, b, ... , z}
'''

class GrammarSymbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        if self.symbol == "":
            return "epsilon"
        return self.symbol

class Terminal(GrammarSymbol):
    def __str__(self):
        return "%s%s%s" % (colors.RED, super(Terminal, self).__str__(), colors.RESET)

class NonTerminal(GrammarSymbol):
    def __str__(self):
        return "%s%s%s" % (colors.BLUE, super(NonTerminal, self).__str__(), colors.RESET)

class Derivation:
    def __init__(self, symbols):
        self.symbols = symbols

    def __str__(self):
        return "".join([str(i) for i in self.symbols])

class Production:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __str__(self):
        return "%s -> %s" % (self.head, " | ".join([str(i) for i in self.body]))

class Grammar:
    def __init__(self, P):
        self.P = P
        self.T = self.getTerminals()
        self.N = self.getNonTerminals()
        self.S = self.getStartSymbol()

    def getProduction(self, head):
        for p in self.P:
            if head == p.head:
                return p
        return None

    def getTerminals(self):
        terminals = set()
        for p in self.P:
            if isinstance(p, Terminal):
                terminals.add(p.head)
        return terminals

    def getNonTerminals(self):
        nonterminals = set()
        for p in self.P:
            if isinstance(p, NonTerminal):
                nonterminals.add(p.head)
        return nonterminals

    def getStartSymbol(self):
        pass

productions = [
    # E -> A(E, E) | epsilon
    Production(NonTerminal("E"), [
        Derivation([
            NonTerminal("A"),
            Terminal("("),
            NonTerminal("E"),
            Terminal(","),
            NonTerminal("E"),
            Terminal(")"),
        ]),
        Derivation([
            Terminal("")
        ]),
    ]),
    # A -> a | b | ... | z
    Production(NonTerminal("A"), [
        Derivation([
            Terminal(i)
        ]) for i in string.ascii_lowercase
    ])
]

for i in productions:
    sys.stdout.write(str(i))
    print()
