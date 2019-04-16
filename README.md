# Lexer
```
This repo stores a python script which provide the capability to convert NFA to DFA.
also it is able to analyze the input code then output the lexical token sequence.
```
#### Installation
```
# 1. Install  graphviz
You should install graphviz firstly which provide the capability to visualize the automota.
Check this link to download the correct version for your platform.
> https://www.graphviz.org/download/
Remeber you should make sure that `dot` command is in your PATH environment.
# 2. Install python requirements
pip install graphviz
```

#### Usage
```
# Modify input code
vim code.c
# Start analysis
python main.py
# Then the token sequence will be printed in console, including the error reporting
# Also, you can check this folder `output` to view the automota transition graph.
```

#### Example
```
---------------- Code Begins ----------------
/*
Multilines comment
*//* Inline comment */
int main () {
    int
    a = 1;
    int             b = 1e8;
    float    c = 0.4;
    int d[] = {1, 2, 3} ;

    char e[] = "Hello world" ;

    c = 1.0 + 3 - 1e8 * 0.5 / 0.005;

    int f = 0xdeadbeef;
    int g = 01234567;

    printf ("Goodbye world!");
}

---------------- Code Ends ----------------
TOKEN: <comment, /*
Multilines comment
*/>
TOKEN: <comment, /* Inline comment */>
TOKEN: <keywords, int>
TOKEN: <identifier, main>
TOKEN: <left round bracket, (>
TOKEN: <right round bracket, )>
TOKEN: <left curly bracket, {>
...
TOKEN: <identifier, printf>
TOKEN: <left round bracket, (>
TOKEN: <string, "Goodbye world!">
TOKEN: <right round bracket, )>
TOKEN: <semicolon, ;>
TOKEN: <right curly bracket, }>
```

#### TODO
- [x] Import NFA from JSON file
- [x] Merge seperated NFA together
- [x] Convert NFA to DFA by subset construction
- [x] Error detection