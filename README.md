# Compiler

#### Description
```
This repo stores a python script which provide the capability of generating parsing tree of subset of C language.
This tool take the folloing stuffs as input: 
1. token sequence as input
2. Grammar of C lanaguage syntax subset
The output consists of:
1. All productions of Grammar
2. All terminals/Non-Terminals of Grammar
3. First/Follow/Select set for all Non-Terminals
4. Parsing table
5. Every step of parsing progress
6. Parsing tree of the input code represented in ASCII diagram
In short, this is a simple lexer-parser project.
```

#### Report

[编译原理实验报告-词法分析](core/lexer/doc/编译原理实验报告-词法分析.docx)

[编译原理实验报告-语法分析](core/parser/doc/编译原理实验报告-语法分析.doc)

#### TODO

- [x] Lexer (Lab1)
- [x] Parser (Lab2)
- [ ] Intermediate Code Generation (Lab3)
- [ ] Optimization

#### Folder Structure
```
.
├── code.c # Code for analysing
├── core
│   ├── __init__.py
│   ├── lexer
│   │   ├── dfa.json
│   │   ├── doc # Report of lexer
│   │   ├── __init__.py
│   │   ├── lexer.py # Entrypoint of lexer
│   │   ├── model.py
│   │   ├── nfa
│   │   ├── nfa.json
│   │   ├── output
│   │   └── README.md
│   └── parser
│       ├── doc # Report of parser
│       ├── __init__.py
│       ├── model.py
│       └── syntax.py # Syntax rules
├── parser.py # Entrypoint of parser
├── README.md
└── requirements.txt
```
