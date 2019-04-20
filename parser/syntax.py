#!/usr/bin/env python
# encoding:utf-8

import string
from model import Production, Derivation, Terminal, NonTerminal, Epsilon

# '''
# Grammar:
# E -> A(E, E)
# E -> epsilon
# A -> a | b | ... | z

# First(E) = {a, b, ... , z, epsilon}
# First(A) = {a, b, ... , z}

# Follow(E) = {',', )}
# Follow(A) = {(}

# Select(E -> A(E, E)) = {a, b, ... , z}
# Select(E -> epsilon) = {',', )}
# Select(A -> a|b|...|z) = {a, b, ... , z}
# '''

# productions = [
#     # E -> A(E, E) | epsilon
#     Production(NonTerminal("E"), [
#         Derivation([
#             NonTerminal("A"),
#             Terminal("("),
#             NonTerminal("E"),
#             Terminal(","),
#             NonTerminal("E"),
#             Terminal(")"),
#         ]),
#         Epsilon(),
#     ]),
#     # A -> a | b | ... | z
#     Production(NonTerminal("A"), [
#         Derivation([
#             Terminal(i)
#         ]) for i in string.ascii_lowercase
#     ])
# ]


'''
E -> TE'
E' -> +TE' | epsilon
T -> FT'
T' -> *FT' | epsilon
F -> (E) | id
'''

productions = [
    # E -> TE'
    Production(NonTerminal("E"), [
        Derivation([
            NonTerminal("T"),
            NonTerminal("E'"),
        ]),
    ]),
    # E' -> +TE' | epsilon
    Production(NonTerminal("E'"), [
        Derivation([
            Terminal("+"),
            NonTerminal("T"),
            NonTerminal("E'"),
        ]),
        Epsilon(),
    ]),
    # T -> FT'
    Production(NonTerminal("T"), [
        Derivation([
            NonTerminal("F"),
            NonTerminal("T'"),
        ]),
    ]),
    # T' -> *FT' | epsilon
    Production(NonTerminal("T'"), [
        Derivation([
            Terminal("*"),
            NonTerminal("F"),
            NonTerminal("T'"),
        ]),
        Epsilon(),
    ]),
    # F -> (E) | id
    Production(NonTerminal("F"), [
        Derivation([
            Terminal("("),
            NonTerminal("E"),
            Terminal(")"),
        ]),
        Derivation([
            Terminal("ID")
        ]),
    ]),
]
