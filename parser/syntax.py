#!/usr/bin/env python
# encoding:utf-8

import string
from model import Production, Derivation, Terminal, NonTerminal

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