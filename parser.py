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

    print("Production of Start symbol:")
    print(grammar.getProductionOfNonTerminal(grammar.getStartSymbol()))
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
    grammar.buildFirst()
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

    # print("Parsing Table:")
    # grammar.visualizeParsingTable()
    # print()

    # # Error
    # tokens = [pmodel.Terminal(i) for i in [
    #     "+",
    #     "ID",
    #     "*",
    #     "+",
    #     "ID",
    # ]]
    # # Right
    # tokens = [pmodel.Terminal(i) for i in [
    #     "(",
    #     "ID",
    #     "+",
    #     "ID",
    #     ")",
    #     "*",
    #     "ID",
    # ]]
    tokens = [
        # Declaration of function
        pmodel.Terminal("int", description="int", line=1, column=3),
        pmodel.Terminal("main", description="identifier", line=1, column=3),
        pmodel.Terminal("(", description="(", line=1, column=3),
        pmodel.Terminal(")", description=")", line=1, column=3),
        pmodel.Terminal("{", description="{", line=1, column=3),
        # Declaration of int
        # int i = 0;
        pmodel.Terminal("int", description="int", line=1, column=3),
        pmodel.Terminal("i", description="identifier", line=1, column=3),
        pmodel.Terminal("=", description="=", line=1, column=3),
        pmodel.Terminal("0", description="INT10", line=1, column=3),
        pmodel.Terminal(";", description=";", line=1, column=3),
        # Declaration of array
        # int j[0x10] = {0};
        pmodel.Terminal("int", description="int", line=1, column=3),
        pmodel.Terminal("j", description="identifier", line=1, column=3),
        pmodel.Terminal("[", description="[", line=1, column=3),
        pmodel.Terminal("0x10", description="INT16", line=1, column=3),
        pmodel.Terminal("]", description="]", line=1, column=3),
        pmodel.Terminal("=", description="=", line=1, column=3),
        pmodel.Terminal("{", description="{", line=1, column=3),
        pmodel.Terminal("0", description="INT10", line=1, column=3),
        pmodel.Terminal("}", description="}", line=1, column=3),
        pmodel.Terminal(";", description=";", line=1, column=3),
        # Assignment of array
        # j[0] = 8;
        pmodel.Terminal("j", description="identifier", line=1, column=3),
        pmodel.Terminal("[", description="[", line=1, column=3),
        pmodel.Terminal("0", description="INT10", line=1, column=3),
        pmodel.Terminal("]", description="]", line=1, column=3),
        pmodel.Terminal("=", description="=", line=1, column=3),
        pmodel.Terminal("8", description="INT10", line=1, column=3),
        pmodel.Terminal("*", description="*", line=1, column=3),
        pmodel.Terminal("2", description="INT10", line=1, column=3),
        pmodel.Terminal(";", description=";", line=1, column=3),
        # If
        # if (1) {
        pmodel.Terminal("if", description="if", line=1, column=3),
        pmodel.Terminal("(", description="(", line=1, column=3),
        pmodel.Terminal("1", description="INT10", line=1, column=3),
        pmodel.Terminal(")", description=")", line=1, column=3),
        pmodel.Terminal("{", description="{", line=1, column=3),
        # Call of fucntion
        # exit(0);
        pmodel.Terminal("exit", description="identifier", line=1, column=3),
        pmodel.Terminal("(", description="(", line=1, column=3),
        pmodel.Terminal("0", description="INT10", line=1, column=3),
        pmodel.Terminal(")", description=")", line=1, column=3),
        pmodel.Terminal(";", description=";", line=1, column=3),
        # End If
        # }
        pmodel.Terminal("}", description="}", line=1, column=3),

        # Do-While Loop
        pmodel.Terminal("do", description="do", line=1, column=3),
        pmodel.Terminal("{", description="{", line=1, column=3),
        pmodel.Terminal("i", description="identifier", line=1, column=3),
        pmodel.Terminal("=", description="=", line=1, column=3),
        pmodel.Terminal("i", description="identifier", line=1, column=3),
        pmodel.Terminal("+", description="+", line=1, column=3),
        pmodel.Terminal("1", description="INT10", line=1, column=3),
        pmodel.Terminal("}", description="}", line=1, column=3),
        pmodel.Terminal("while", description="while", line=1, column=3),
        pmodel.Terminal("(", description="(", line=1, column=3),
        pmodel.Terminal("i", description="identifier", line=1, column=3),
        pmodel.Terminal(">", description=">", line=1, column=3),
        pmodel.Terminal("10", description="INT10", line=1, column=3),
        pmodel.Terminal(")", description=")", line=1, column=3),
        
        # Return value
        pmodel.Terminal("return", description="return", line=1, column=3),
        pmodel.Terminal("0", description="INT10", line=1, column=3),
        pmodel.Terminal(";", description=";", line=1, column=3),
        pmodel.Terminal("}", description="}", line=1, column=3),
    ]
    print(grammar.parse(tokens))


if __name__ == "__main__":
    main()