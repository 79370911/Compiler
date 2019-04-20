#!/usr/bin/env python
# encoding:utf-8

from core.lexer import model as lmodel
from core.parser import model as pmodel
from core.parser import syntax
import colorama

def main():
    colorama.init()
    grammar = pmodel.Grammar(syntax.productions)
    print("Grammar:")
    grammar.visualize()
    print()

    print("Production of E:")
    print(grammar.getProductionOfNonTerminal(pmodel.NonTerminal("E")))
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

    # Error
    tokens = [pmodel.Terminal(i) for i in [
        "+",
        "ID",
        "*",
        "+",
        "ID",
    ]]
    # Right
    tokens = [pmodel.Terminal(i) for i in [
        "(",
        "ID",
        "+",
        "ID",
        ")",
        "*",
        "ID",
    ]]
    print(grammar.parse(tokens))


if __name__ == "__main__":
    main()