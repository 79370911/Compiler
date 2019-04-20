from colorama import Fore, Back, Style

class GrammarSymbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        if self.symbol == "":
            # TODO: !!! Notice that epsilon is not a syntax symbol, neither terminal nor non-terminal
            # We should not handle epsilon here
            return "epsilon"
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

class Production:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __str__(self):
        return "%s -> %s" % (self.head, " | ".join([str(i) for i in self.body]))

class Grammar:
    def __init__(self, P):
        self.P = P
        self.T = self.getTerminals()
        self.N = self.getNonTerminals()
        self.S = self.getStartSymbol()

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
                for s in d.symbols:
                    if isinstance(s, NonTerminal):
                        nonterminals.add(s)
        return nonterminals

    def getStartSymbol(self):
        return self.P[0].head

    def getFirst(self, nonTerminal):
        raise NotImplementedError()

    def getFollow(self, nonTerminal):
        raise NotImplementedError()

    def getSelect(self, nonTerminal):
        raise NotImplementedError()

    def getParsingTable(self):
        raise NotImplementedError()

    def parse(self, tokens):
        raise NotImplementedError()

    def visualize(self):
        for p in self.P:
            print(p)

