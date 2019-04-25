# Parser


#### Usage
```
python parser.py
```

#### Data Structure Defination
1. Syntax
```python
# We only need to provide all productions of G
# And the parser will calculate the Terminal/Non-Terminal Set
# By the way, the first item in the list will be regard as the Start symbol
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
    ...
]
```
2. Token Sequences
```python
tokens = [
    # Declaration of function
    pmodel.Terminal("int", description="int", line=1, column=3),
    pmodel.Terminal("main", description="identifier", line=1, column=3),
    pmodel.Terminal("(", description="(", line=1, column=3),
    pmodel.Terminal(")", description=")", line=1, column=3),
    pmodel.Terminal("{", description="{", line=1, column=3),
    ...
]
```
