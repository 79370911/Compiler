from colorama import Fore, Back, Style

class GrammarSymbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        # if self.symbol == "":
        #     # TODO: !!! Notice that epsilon is not a syntax symbol, neither terminal nor non-terminal
        #     # We should not handle epsilon here
        #     return "epsilon"
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

class Terminal(GrammarSymbol):
    def __str__(self):
        return "%s%s%s" % (Fore.RED, super(Terminal, self).__str__(), Style.RESET_ALL)

class NonTerminal(GrammarSymbol):
    def __str__(self):
        return "%s%s%s" % (Fore.BLUE, super(NonTerminal, self).__str__(), Style.RESET_ALL)

class Derivation:
    def __init__(self, symbols):
        self.symbols = symbols

    def __str__(self):
        return "".join([str(i) for i in self.symbols])

class Epsilon():
    def __str__(self):
        return "%s%s%s" % (Fore.MAGENTA, "epsilon", Style.RESET_ALL)

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

    def getProduction(self, head):
        for p in self.P:
            if head == p.head:
                return p
        return None

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
            for d in self.getProduction(symbol).body:
                if isinstance(d, Epsilon):
                    return True
        return False

    def getStartSymbol(self):
        return self.P[0].head

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
            production = self.getProduction(symbol)
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

    def getFollow(self, symbol):
        raise NotImplementedError()

    def getSelect(self, symbol):
        raise NotImplementedError()

    def getParsingTable(self):
        raise NotImplementedError()

    def parse(self, tokens):
        raise NotImplementedError()

    def visualize(self):
        for p in self.P:
            print(p)

    def visualizeFirst(self):
        for k, v in self.firstCache.items():
            if isinstance(k, NonTerminal):
                print("%s => %s" % (k, ",".join([str(i) for i in v])))

