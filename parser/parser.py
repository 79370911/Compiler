#!/usr/bin/env python
# encoding:utf-8

from model import NonTerminal

import colorama
import model
import syntax

colorama.init()
grammar = model.Grammar(syntax.productions)
print("Grammar:")
grammar.visualize()
print()

print("Production of E:")
print(grammar.getProductionOfNonTerminal(NonTerminal("E")))
print()

print("Terminals:")
print(",".join([str(i) for i in grammar.getTerminals()]))
print()

print("NonTerminals:")
print(",".join([str(i) for i in grammar.getNonTerminals()]))
print()

print("Start Symbol:")
print(grammar.getStartSymbol())
print()

print("First set:")
for s in grammar.getNonTerminals().union(grammar.getTerminals()):
    grammar.getFirst(s)
grammar.visualizeFirst()
print()

print("Follow set:")
grammar.buildFollow()
grammar.visualizeFollow()
print()

print("Select set:")
grammar.buildSelect()
grammar.visualizeSelect()
print()

print("Parsing Table:")
grammar.visualizeParsingTable()
print()

# tokens = []
# print(grammar.parse(tokens))