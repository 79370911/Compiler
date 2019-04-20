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

print("Production of E:")
print(grammar.getProductionOfNonTerminal(NonTerminal("E")))
print("Terminals:")
print(",".join([str(i) for i in grammar.getTerminals()]))
print("NonTerminals:")
print(",".join([str(i) for i in grammar.getNonTerminals()]))
print("Start Symbol:")
print(grammar.getStartSymbol())

print("First set:")
for s in grammar.getNonTerminals().union(grammar.getTerminals()):
    grammar.getFirst(s)
grammar.visualizeFirst()

print("Follow set:")
grammar.buildFollow()
grammar.visualizeFollow()

print("Select set:")
grammar.buildSelect()
grammar.visualizeSelect()

# print(grammar.getParsingTable())

# tokens = []
# print(grammar.parse(tokens))

# TODO: // Define Follow class
# TODO: // Define Predictive Analysis table class
# TODO: // Implement visualize method