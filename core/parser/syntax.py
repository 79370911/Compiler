#!/usr/bin/env python
# encoding:utf-8

import string
from .model import Production, Derivation, Terminal, NonTerminal, Epsilon

# '''
# Grammar:
# E -> A(E, E),
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
#             Terminal(i),
#         ]) for i in string.ascii_lowercase
#     ]),
# ]


# '''
# E -> TE'
# E' -> +TE' | epsilon
# T -> FT'
# T' -> *FT' | epsilon
# F -> (E) | id
# '''

# productions = [
#     # E -> TE'
#     Production(NonTerminal("E"), [
#         Derivation([
#             NonTerminal("T"),
#             NonTerminal("E'"),
#         ]),
#     ]),
#     # E' -> +TE' | epsilon
#     Production(NonTerminal("E'"), [
#         Derivation([
#             Terminal("+"),
#             NonTerminal("T"),
#             NonTerminal("E'"),
#         ]),
#         Epsilon(),
#     ]),
#     # T -> FT'
#     Production(NonTerminal("T"), [
#         Derivation([
#             NonTerminal("F"),
#             NonTerminal("T'"),
#         ]),
#     ]),
#     # T' -> *FT' | epsilon
#     Production(NonTerminal("T'"), [
#         Derivation([
#             Terminal("*"),
#             NonTerminal("F"),
#             NonTerminal("T'"),
#         ]),
#         Epsilon(),
#     ]),
#     # F -> (E) | id
#     Production(NonTerminal("F"), [
#         Derivation([
#             Terminal("("),
#             NonTerminal("E"),
#             Terminal(")"),
#         ]),
#         Derivation([
#             Terminal("ID"),
#         ]),
#     ]),
# ]

# Grammar production of C-- language
productions = [
    # S -> func funcs 
    Production(NonTerminal("S"), [
        Derivation([
            NonTerminal("func"),
            NonTerminal("funcs"),
        ]),
    ]),
    # funcs -> func funcs 
    Production(NonTerminal("funcs"), [
        Derivation([
            NonTerminal("func"),
            NonTerminal("funcs"),
        ]),
        Epsilon(),
    ]),
    # func -> type identifier ( args ) func_body 
    Production(NonTerminal("func"), [
        Derivation([
            NonTerminal("type"),
            Terminal("identifier"),
            Terminal("("),
            NonTerminal("args"),
            Terminal(")"),
            NonTerminal("func_body"),
        ]),
    ]),
    # type -> long | void | int | float | short | char | double
    Production(NonTerminal("type"), [
        Derivation([
            Terminal("long"),
        ]),
        Derivation([
            Terminal("void"),
        ]),
        Derivation([
            Terminal("int"),
        ]),
        Derivation([
            Terminal("float"),
        ]),
        Derivation([
            Terminal("short"),
        ]),
        Derivation([
            Terminal("char"),
        ]),
        Derivation([
            Terminal("double"),
        ]),
    ]),
    # args -> type identifier arg | epsilon 
    Production(NonTerminal("args"), [
        Derivation([
            NonTerminal("type"),
            Terminal("identifier"),
            NonTerminal("arg"),
        ]),
        Epsilon(),
    ]),
    # arg -> epsilon | , type identifier arg 
    Production(NonTerminal("arg"), [
        Derivation([
            Terminal(","),
            NonTerminal("type"),
            Terminal("identifier"),
            NonTerminal("arg"),
        ]),
        Epsilon(),
    ]),
    # func_body -> ; | block 
    Production(NonTerminal("func_body"), [
        Derivation([
            Terminal(";"),
        ]),
        Derivation([
            NonTerminal("block"),
        ]),
    ]),
    # block -> { define_stmts stmts } 
    Production(NonTerminal("block"), [
        Derivation([
            Terminal("{"),
            NonTerminal("define_stmts"),
            NonTerminal("stmts"),
            Terminal("}"),
        ]),
    ]),
    # define_stmts -> epsilon | define_stmt define_stmts 
    Production(NonTerminal("define_stmts"), [
        Derivation([
            NonTerminal("define_stmt"),
            NonTerminal("define_stmts"),
        ]),
        Epsilon(),
    ]),
    # define_stmt -> type identifier init vars ; 
    Production(NonTerminal("define_stmt"), [
        Derivation([
            NonTerminal("type"),
            Terminal("identifier"),
            NonTerminal("init"),
            NonTerminal("vars"),
            Terminal(";"),
        ]),
    ]),
    # init -> epsilon | [ num_const ] | = expression 
    Production(NonTerminal("init"), [
        Derivation([
            Terminal("["),
            NonTerminal("num_const"),
            Terminal("]"),
        ]),
        Derivation([
            Terminal("="),
            NonTerminal("expression"),
        ]),
        Epsilon(),
    ]),
    # vars -> epsilon | , identifier init vars 
    Production(NonTerminal("vars"), [
        Derivation([
            Terminal(","),
            Terminal("identifier"),
            NonTerminal("init"),
            NonTerminal("vars"),
        ]),
        Epsilon(),
    ]),
    # stmts -> epsilon | stmt stmts 
    Production(NonTerminal("stmts"), [
        Derivation([
            NonTerminal("stmt"),
            NonTerminal("stmts"),
        ]),
        Epsilon(),
    ]),
    # stmt -> branch_stmt | assign_stmt | iteration_stmt | jump_stmt 
    Production(NonTerminal("stmt"), [
        Derivation([
            NonTerminal("branch_stmt"),
        ]),
        Derivation([
            NonTerminal("assign_stmt"),
        ]),
        Derivation([
            NonTerminal("iteration_stmt"),
        ]),
        Derivation([
            NonTerminal("jump_stmt"),
        ]),
    ]),
    # assign_stmt -> expression ; 
    Production(NonTerminal("assign_stmt"), [
        Derivation([
            NonTerminal("expression"),
        ]),
    ]),
    # jump_stmt -> return isnull_expr ; | break ; | continue ; 
    Production(NonTerminal("jump_stmt"), [
        Derivation([
            Terminal("return"),
            NonTerminal("isnull_expr"),
            Terminal(";"),
        ]),
        Derivation([
            Terminal("break"),
            Terminal(";"),
        ]),
        Derivation([
            Terminal("continue"),
            Terminal(";"),
        ]),
    ]),
    # iteration_stmt -> while ( logical_expression ) block_stmt | do block_stmt while ( logical_expression ) ; | for ( isnull_expr ; isnull_expr ; isnull_expr ) block_stmt 
    Production(NonTerminal("iteration_stmt"), [
        Derivation([
            Terminal("while"),
            Terminal("("),
            NonTerminal("logical_expression"),
            Terminal(")"),
            NonTerminal("block_stmt"),
        ]),
        Derivation([
            Terminal("do"),
            NonTerminal("block_stmt"),
            Terminal("while"),
            Terminal("("),
            NonTerminal("logical_expression"),
            Terminal(")"),
            Terminal(";"),
        ]),
        Derivation([
            Terminal("for"),
            Terminal("("),
            NonTerminal("isnull_expr"),
            Terminal(";"),
            NonTerminal("isnull_expr"),
            Terminal(";"),
            NonTerminal("isnull_expr"),
            Terminal(")"),
            NonTerminal("block_stmt"),
        ]),
    ]),
    # branch_stmt -> if ( logical_expression ) block_stmt result | switch ( identifier ) { case_stmt case_stmts default_stmt } 
    Production(NonTerminal("branch_stmt"), [
        Derivation([
            Terminal("if"),
            Terminal("("),
            NonTerminal("logical_expression"),
            Terminal(")"),
            NonTerminal("block_stmt"),
            NonTerminal("result"),
        ]),
        Derivation([
            Terminal("switch"),
            Terminal("("),
            Terminal("identifier"),
            Terminal(")"),
            Terminal("{"),
            NonTerminal("case_stmt"),
            NonTerminal("case_stmts"),
            NonTerminal("default_stmt"),
            Terminal("}"),
        ]),
    ]),
    # result -> epsilon | else block_stmt 
    Production(NonTerminal("result"), [
        Derivation([
            Terminal("else"),
            NonTerminal("block_stmt"),
        ]),
        Epsilon(),
    ]),
    # logical_expression -> expression bool_expression | ! expression bool_expression 
    Production(NonTerminal("logical_expression"), [
        Derivation([
            NonTerminal("expression"),
            NonTerminal("bool_expression"),
        ]),
        Derivation([
            Terminal("!"),
            NonTerminal("expression"),
            NonTerminal("bool_expression"),
        ]),
    ]),
    # bool_expression -> epsilon | lop expression bool_expression 
    Production(NonTerminal("bool_expression"), [
        Derivation([
            NonTerminal("lop"),
            NonTerminal("expression"),
            NonTerminal("bool_expression"),
        ]),
        Epsilon(),
    ]),
    # lop -> || | && 
    Production(NonTerminal("lop"), [
        Derivation([
            Terminal("||"),
        ]),
        Derivation([
            Terminal("&&"),
        ]),
    ]),
    # case_stmts -> epsilon | case_stmt case_stmts 
    Production(NonTerminal("case_stmts"), [
        Derivation([
            NonTerminal("case_stmt"),
            NonTerminal("case_stmts"),
        ]),
        Epsilon(),
    ]),
    # case_stmt -> case const : stmts 
    Production(NonTerminal("case_stmt"), [
        Derivation([
            Terminal("case"),
            NonTerminal("const"),
            Terminal(":"),
            NonTerminal("stmts"),
        ]),
    ]),
    # default_stmt -> default : stmts 
    Production(NonTerminal("default_stmt"), [
        Derivation([
            Terminal("default"),
            Terminal(":"),
            NonTerminal("stmts"),
        ]),
    ]),
    # block_stmt -> { stmts } 
    Production(NonTerminal("block_stmt"), [
        Derivation([
            Terminal("{"),
            NonTerminal("stmts"),
            Terminal("}"),
        ]),
    ]),
    # isnull_expr -> epsilon | expression 
    Production(NonTerminal("isnull_expr"), [
        Derivation([
            NonTerminal("expression"),
        ]),
        Epsilon(),
    ]),
    # expression -> value operation
    Production(NonTerminal("expression"), [
        Derivation([
            NonTerminal("value"),
            NonTerminal("operation"),
        ]),
    ]),
    # operation -> equal_op value | epsilon | compare_op value 
    Production(NonTerminal("operation"), [
        Derivation([
            NonTerminal("equal_op"),
            NonTerminal("value"),
        ]),
        Derivation([
            NonTerminal("compare_op"),
            NonTerminal("value"),
        ]),
        Epsilon(),
    ]),
    # compare_op -> > | == | <= | != | >= | < 
    Production(NonTerminal("compare_op"), [
        Derivation([
            Terminal(">"),
        ]),
        Derivation([
            Terminal(">="),
        ]),
        Derivation([
            Terminal("<"),
        ]),
        Derivation([
            Terminal("<="),
        ]),
        Derivation([
            Terminal("=="),
        ]),
        Derivation([
            Terminal("!="),
        ]),
    ]),
    # equal_op -> /= | *= | = | -= | %= | += 
    Production(NonTerminal("equal_op"), [
        Derivation([
            Terminal("+="),
        ]),
        Derivation([
            Terminal("-="),
        ]),
        Derivation([
            Terminal("*="),
        ]),
        Derivation([
            Terminal("/="),
        ]),
        Derivation([
            Terminal("%="),
        ]),
        Derivation([
            Terminal("="),
        ]),
    ]),
    # value -> item value' 
    Production(NonTerminal("value"), [
        Derivation([
            NonTerminal("item"),
            NonTerminal("value'"),
        ]),
    ]),
    # value' -> - item value' | epsilon | + item value' 
    Production(NonTerminal("value'"), [
        Derivation([
            Terminal("-"),
            NonTerminal("item"),
            NonTerminal("value'"),
        ]),
        Derivation([
            Terminal("+"),
            NonTerminal("item"),
            NonTerminal("value'"),
        ]),
        Epsilon(),
    ]),
    # item -> factor item' 
    Production(NonTerminal("item"), [
        Derivation([
            NonTerminal("factor"),
            NonTerminal("item'"),
        ]),
    ]),
    # item' -> % factor item' | / factor item' | * factor item' | epsilon 
    Production(NonTerminal("item'"), [
        Derivation([
            Terminal("%"),
            NonTerminal("factor"),
            NonTerminal("item'"),
        ]),
        Derivation([
            Terminal("/"),
            NonTerminal("factor"),
            NonTerminal("item'"),
        ]),
        Derivation([
            Terminal("*"),
            NonTerminal("factor"),
            NonTerminal("item'"),
        ]),
        Epsilon(),
    ]),
    # factor -> identifier call_func | const | ( value ) 
    Production(NonTerminal("factor"), [
        Derivation([
            Terminal("identifier"),
            NonTerminal("call_func"),
        ]),
        Derivation([
            NonTerminal("const"),
        ]),
        Derivation([
            Terminal("("),
            NonTerminal("value"),
            Terminal(")"),
        ]),
    ]),
    # call_func -> epsilon | ( es ) 
    Production(NonTerminal("call_func"), [
        Derivation([
            Terminal("("),
            NonTerminal("es"),
            Terminal(")"),
        ]),
        Epsilon(),
    ]),
    # es -> isnull_expr isnull_es 
    Production(NonTerminal("es"), [
        Derivation([
            NonTerminal("isnull_expr"),
            NonTerminal("isnull_es"),
        ]),
    ]),
    # isnull_es -> epsilon | , isnull_expr isnull_es 
    Production(NonTerminal("isnull_es"), [
        Derivation([
            Terminal(","),
            NonTerminal("isnull_expr"),
            NonTerminal("isnull_es"),
        ]),
        Epsilon(),
    ]),
    # const -> STR | CHAR | FLOAT | num_const 
    Production(NonTerminal("const"), [
        Derivation([
            Terminal("STR"),
        ]),
        Derivation([
            Terminal("CHAR"),
        ]),
        Derivation([
            Terminal("FLOAT"),
        ]),
        Derivation([
            NonTerminal("num_const"),
        ]),
    ]),
    # num_const -> INT10 | INT8 | INT16 
    Production(NonTerminal("num_const"), [
        Derivation([
            Terminal("INT8"),
        ]),
        Derivation([
            Terminal("INT10"),
        ]),
        Derivation([
            Terminal("INT16"),
        ]),
    ]),
]