from colorama import Fore, Back, Style
from tabulate import tabulate
from anytree import Node, RenderTree

class GrammarSymbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, GrammarSymbol):
            return self.symbol == other.symbol
        else:
            return False

    def __hash__(self):
        return hash(self.symbol)

class Terminal(GrammarSymbol):
    def __init__(self, symbol, description="UNKNOWN", line=0, column=0):
        self.symbol = symbol
        self.description = description
        self.line = line
        self.column = column

    def __str__(self):
        return "%s%s%s" % (Fore.RED, super(Terminal, self).__str__(), Style.RESET_ALL)

    def __lt__(self, other):
        return self.symbol < other.symbol

    def __eq__(self, other):
        if isinstance(other, Terminal):
            return self.symbol == other.symbol
        else:
            return self.symbol == other

    # def __eq__(self, other):
    #     if isinstance(other, str):
    #         return self.symbol == other
    #     else:
    #         return self.symbol == other.symbol and self.description == other.description

    def __hash__(self):
        return hash("%s, %s" % (self.symbol, self.description))    


class NonTerminal(GrammarSymbol):
    def __str__(self):
        return "%s%s%s" % (Fore.BLUE, super(NonTerminal, self).__str__(), Style.RESET_ALL)

    def __lt__(self, other):
        return self.symbol < other.symbol

class Endmark():
    def __str__(self):
        return "%s$%s" % (Fore.YELLOW, Style.RESET_ALL)

    def __eq__(self, other):
        if isinstance(other, Endmark):
            return True
        return False

    def __hash__(self):
        return hash("$")

class Derivation:
    def __init__(self, symbols):
        self.symbols = symbols

    def __str__(self):
        return " ".join([str(i) for i in self.symbols])

class Synch:
    def __str__(self):
        return "synch"

class Epsilon():
    def __str__(self):
        return "%s%s%s" % (Fore.MAGENTA, "epsilon", Style.RESET_ALL)

    def __eq__(self, other):
        if isinstance(other, Epsilon):
            return True
        return False

    def __hash__(self):
        return hash("")

class Production:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __str__(self):
        return "%s -> %s" % (self.head, " | ".join([str(i) for i in self.body]))

class InvalidSymbolException(Exception): pass

class Grammar:
    def __init__(self, P):
        '''
        We assume that there is only one syntax symbol at left side of every single production
        Example:
            E -> A(E, E)
            E -> epsilon
            A -> a | b | ... | z

            will be simplified like:

            E -> A(E, E) | epsilon
            A -> a | b | ... | z
        '''
        self.P = P
        self.T = self.getTerminals()
        self.N = self.getNonTerminals()
        self.S = self.getStartSymbol()
        self.firstCache = {}
        self.followCache = {}
        self.selectCache = {}
        self.parsingTable = None

    def getProductionOfNonTerminal(self, head):
        for p in self.P:
            if head == p.head:
                return p
        return None

    def getProductions(self):
        return self.P

    def getTerminals(self):
        terminals = set()
        for p in self.P:
            if isinstance(p.head, Terminal):
                terminals.add(p.head)
            for d in p.body:
                if not isinstance(d, Epsilon):
                    for s in d.symbols:
                        if isinstance(s, Terminal):
                            terminals.add(s)
        return terminals

    def getNonTerminals(self):
        nonterminals = set()
        for p in self.P:
            if isinstance(p.head, NonTerminal):
                nonterminals.add(p.head)
            for d in p.body:
                if not isinstance(d, Epsilon):
                    for s in d.symbols:
                        if isinstance(s, NonTerminal):
                            nonterminals.add(s)
        return nonterminals

    def hasEpsilonDerivation(self, symbol):
        if isinstance(symbol, NonTerminal):
            for d in self.getProductionOfNonTerminal(symbol).body:
                if isinstance(d, Epsilon):
                    return True
        return False

    def getStartSymbol(self):
        return self.P[0].head

    def buildFirst(self):
        for i in self.getNonTerminals():
            self.getFirst(i)

    def getFirst(self, symbol):
        # Cache hit
        if symbol in self.firstCache.keys():
            return self.firstCache[symbol]
        result = set()
        # 1. If X is a terminal, then FIRST(X) = {X}
        if isinstance(symbol, Terminal):
            result.add(symbol)
        else:
            # Get production
            production = self.getProductionOfNonTerminal(symbol)
            print("%s => %s" % (symbol, production))
            for d in production.body:
                # 2. If X -> epsilon is a production(Derivation of a production), then add epsilon to FIRST(X)
                if isinstance(d, Epsilon):
                    result.add(d)
                else:
                    for s in d.symbols:
                        if isinstance(s, Terminal):
                            # print("%s is a terminal" % (s))
                            result.add(s)
                        else:
                            # print("%s is a nonterminal" % (s))
                            first = self.getFirst(s)
                            # print("first of %s is %s" % (s, first))
                            result = result.union(first)
                            # print("merged result: %s" % (result))
                        if not self.hasEpsilonDerivation(s):
                            break
        # Cache result
        self.firstCache[symbol] = result
        return result

    def buildFollow(self):
        modified = True
        while modified:
            modified = self.buildFollowOnce()

    def buildFollowOnce(self):
        # Flag to detect whether the FOLLOW(s) has been modified
        modified = False
        for s in self.getNonTerminals():
            # print("Calculating FOLLOW(%s)" % (s))
            # Init
            if s not in self.followCache.keys():
                self.followCache[s] = set()

            # 1. Place $ in FOLLOW(S), where S is the start s
            if self.getStartSymbol() == s:
                if Endmark() not in self.followCache[s]:
                    modified = True
                # print("$ => FOLLOW(%s) = %s" % (s, ",".join([str(_) for _ in self.followCache[s]])))
                self.followCache[s].add(Endmark())

            # For each production of s
            p = self.getProductionOfNonTerminal(s)
            for d in p.body:
                # print("=" * 0x20)
                # print("Derivation: %s" % (d))
                if not isinstance(d, Epsilon):
                    # Normal order
                    for i in range(len(d.symbols) - 1):
                        # print("Analysing: %s -> %s" % (p.head, d))
                        m = d.symbols[i]
                        n = d.symbols[i + 1]
                        if isinstance(m, NonTerminal):
                            # print(m, n)
                            # Init follow cache for m
                            if m not in self.followCache.keys():
                                self.followCache[m] = set()
                            # 2. If there is a production A -> alpha B beta, then every thing FIRST(beta) except epsilon in FOLLOW(B)
                            first = self.getFirst(n)
                            first.discard(Epsilon())
                            before = len(self.followCache[m])
                            self.followCache[m] = self.followCache[m].union(first)
                            # print("FIRST(%s) = %s => FOLLOW(%s) = %s" % (n, ",".join([str(_) for _ in first]), m,  ",".join([str(_) for _ in self.followCache[m]])))
                            after = len(self.followCache[m])
                            if after > before:
                                modified = True

                            # 3.1. If there is a production A -> alpha B, then  everything in FOLLOW(A) is in FOLLOW(B)
                            if (i + 1 == (len(d.symbols) - 1)) and isinstance(n, NonTerminal):
                                if n not in self.followCache.keys():
                                    self.followCache[n] = set()
                                before = len(self.followCache[n])
                                self.followCache[m] = self.followCache[m].union(self.followCache[p.head])
                                # print("3.1 FOLLOW(%s) = %s => FOLLOW(%s) = %s" % (p.head, ",".join([str(_) for _ in self.followCache[p.head]]), m, ",".join([str(_) for _ in self.followCache[m]])))
                                after = len(self.followCache[n])
                                if after > before:
                                    modified = True
                    # Reverse order
                    # 3.2 If there is a production A -> alpha B beta, where FIRST(beta) contains epsilon, then everything is FOLLOW(A) is in FOLLOW(B)
                    for i in range(len(d.symbols))[::-1]:
                        m = d.symbols[i]
                        if isinstance(m, Terminal):
                            break
                        if Epsilon() not in self.getFirst(m):
                            if m not in self.followCache.keys():
                                self.followCache[m] = set()
                            before = len(self.followCache[m])
                            self.followCache[m] = self.followCache[m].union(self.followCache[p.head])
                            # print("3.2 FOLLOW(%s) = %s => FOLLOW(%s) = %s" % (p.head, ",".join([str(_) for _ in self.followCache[p.head]]), m, ",".join([str(_) for _ in self.followCache[m]])))
                            
                            after = len(self.followCache[m])
                            if after > before:
                                modified = True
                            break
                    # print("FOLLOW TABLE:")
                    # self.visualizeFollow()
                    # print()
        return modified

    def getFollow(self, symbol):
        return self.followCache[symbol]
        
    def buildSelect(self):
        for p in self.getProductions():
            for d in p.body:
                self.buildSelectForSingleProduction(p.head, d)
        
    def buildSelectForSingleProduction(self, head, body):
        key = (head, body)
        # E -> epsilon
        if isinstance(body, Epsilon):
            self.selectCache[key] = self.getFollow(head)
            return
        symbol = body.symbols[0]
        # E -> alpha
        if isinstance(symbol, Terminal):
            result = set()
            result.add(body.symbols[0])
            self.selectCache[key] = result
            return
        else:
            first = self.getFirst(symbol)
            if Epsilon() in first:
                self.selectCache[key] = self.getFollow(symbol)
                return
            else:
                self.selectCache[key] = first
                return

    def getSelect(self, key):
        return self.selectCache[key]

    def getParsingTable(self):
        if self.parsingTable == None:
            data = {}
            for k, v in self.selectCache.items():
                for value in v:
                    key = (k[0], value)
                    data[key] = k[1]
            self.parsingTable = data
        return self.parsingTable

    def getParsingTableWithSynch(self):
        for x in self.getNonTerminals():
            follow = self.getFollow(x)
            print("FOLLOW(%s) = %s" % (x, ",".join([str(_) for _ in follow])))
            for y in follow:
                self.setDerivation(x, y, Synch())
        return self.getParsingTable()

    def getParsingTableForVisualize(self):
        terminals = list(self.getTerminals())
        nonterminals = list(self.getNonTerminals())
        terminals.sort()
        nonterminals.sort()

        headers = terminals
        headers.insert(0, "Non-Terminals")
        headers.append(Endmark())
        
        data = self.getParsingTableWithSynch()

        M = len(nonterminals)
        N = len(headers)
        table = [[None for n in range(N)] for m in range(M)]

        columnMapping = {}
        i = 0
        for x in headers:
            columnMapping[x] = i
            i += 1
        self.columnMapping = columnMapping

        rowMapping = {}
        i = 0
        for x in nonterminals:
            rowMapping[x] = i
            i += 1
        self.rowMapping = rowMapping

        for k, v in data.items():
            x = rowMapping[k[0]]
            y = columnMapping[k[1]] - 1
            table[x][0] = k[0]
            if v:
                if isinstance(v, Synch):
                    table[x][y + 1] = v
                else:
                    table[x][y + 1] = "%s -> %s" % (k[0], v)
            else:
                table[x][y + 1] = None
        return table, headers

    def visualize(self):
        for p in self.P:
            print(p)

    def visualizeDict(self, d):
        keys = list(d.keys())
        keys.sort()
        for k in keys:
            if isinstance(k, NonTerminal):
                print("%s = { %s }" % (str(k), ", ".join([str(i) for i in d[k]])))
                
    def visualizeFirst(self):
        self.visualizeDict(self.firstCache)

    def visualizeFollow(self):
        self.visualizeDict(self.followCache)
    
    def visualizeSelect(self):
        for p in self.getProductions():
            for d in p.body:
                key = (p.head, d)
                select = self.getSelect(key)
                print("%s = %s => { %s }" % (p.head, d, ", ".join([str(i) for i in select])))

    def visualizeParsingTable(self):
        table, headers = self.getParsingTableForVisualize()
        print(tabulate(table, headers=headers, tablefmt='grid'))

    def parse(self, tokens):
        if not isinstance(tokens[-1], Endmark):
            tokens.append(Endmark())
        ip = 0

        startSymbol = self.getStartSymbol()

        stack = []
        stack.append(Endmark())

        root = Node(startSymbol)
        stack.append((startSymbol, root))

        print("=" * 0x20)
        print("Stack: %s" % (",".join([str(i) if isinstance(i, Endmark) else str(i[0]) for i in stack[::-1]])))
        print("Input: %s" % (",".join([str(i) for i in tokens[ip:]])))

        while len(stack) != 1:
            top, currentNode = stack.pop()

            if ip < len(tokens):
                # there are input left
                token = tokens[ip]
            else:
                token = Endmark()

            if (isinstance(top, Terminal) and isinstance(token, Terminal) and top.symbol == token.description):
                ip += 1
            else:
                if isinstance(top, NonTerminal) and isinstance(token, Terminal):
                    derivation = self.getDerivation(top, token.description)
                else:
                    derivation = self.getDerivation(top, token)
                if derivation == None:
                    # 1. M[A, a] = None, according to the panic mode, we should ignore the invalid user input.
                    if isinstance(token, Endmark):
                        break
                    else:
                        print("[%d:%d][Ignore] No derivation for %s with input %s" % (token.line, token.column, top, token))
                        stack.append((top, currentNode))
                        ip += 1
                else:
                    print("%s -> %s" % (top, derivation))
                    if isinstance(derivation, Epsilon):
                        Node(Epsilon(), parent=currentNode)
                    elif isinstance(derivation, Synch):
                        print("[%d:%d][Error] Synch derivation for %s with input %s" % (token.line, token.column, top, token))
                    else:
                        for s in derivation.symbols[::-1]:
                            node = Node(s, parent=currentNode)
                            stack.append((s, node))

            print("=" * 0x20)
            print("Stack: %s" % (",".join([str(i) if isinstance(i, Endmark) else str(i[0]) for i in stack[::-1]])))
            print("Input: %s" % (",".join([str(i) for i in tokens[ip:]])))

        if len(stack) == 1 and len(tokens[ip:]) == 1:
            print("Parsing succeed")
            for pre, fill, node in RenderTree(root):
                if isinstance(node.name, Terminal):
                    print("%s%s" % (pre, "[%d:%d] %s" % (node.name.line, node.name.column, node.name)))
                else:
                    print("%s%s" % (pre, node.name))
        else:
            print("Parsing failed")

    def getDerivation(self, nonterminal, terminal):
        table = self.getParsingTable()
        for k, v in table.items():
            if k[0] == nonterminal and k[1] == terminal:
                return v
        return None
    
    def setDerivation(self, nonterminal, terminal, derivation):
        table = self.getParsingTable()
        key = (nonterminal, terminal)
        if key not in table.keys():
            table[key] = derivation