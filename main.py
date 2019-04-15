#!/usr/bin/env python
# encoding:utf-8

import json
import queue
import glob
import graphviz

def reprTuple(T):
    t = list(T)
    t.sort()
    return ",".join([str(i) for i in t])

def importNFA(filename):
    data = json.load(open(filename))
    labeledNodes = {}
    nodes = []
    edges = []
    init = True
    for k, v in data.items():
        node = Node(k)
        if init:
            node.init = True
            init = False
        if "accept" in v.keys():
            node.accept = v["accept"]
        labeledNodes[k] = node
        nodes.append(node)

    for k, v in data.items():
        for c, states in v["edges"].items():
            for state in states:
                edge = Edge(labeledNodes[k], c, labeledNodes[state])
                edges.append(edge)
    
    return NFA(nodes, edges)

class Node:
    def __init__(self, label, accept=None, init=False):
        self.label = label
        self.accept = accept
        self.init = init
    
    def __str__(self):
        result = self.label
        if self.accept != None:
            result = "%s[%s]" % (result, self.accept)
        if self.init:
            result = "[INIT]%s" % (result)
        return result
    
    def __eq__(self, other):
        return self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def __gt__(self, other):
        return self.label > other.label
    
class Edge:
    def __init__(self, start, weight, end):
        self.start = start
        self.end = end
        self.weight = weight
    
    def __str__(self):
        if self.weight == "":
            return "%s > %s" % (self.start, self.end)
        else:
            return "%s (%r)> %s" % (self.start, self.weight, self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.weight == other.weight

    def __hash__(self):
        return hash("%s %s %s" % (self.start, self.weight, self.end))


class FA:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def visualize(self, filename):
        g = graphviz.Graph()
        for node in self.nodes:
            if node.accept:
                g.node(node.label, node.accept, shape='doublecircle')
            else:
                g.node(node.label, node.label)
        for edge in self.edges:
            if edge.weight != "":
                g.edge(edge.start.label, edge.end.label, repr(edge.weight))
            else:
                g.edge(edge.start.label, edge.end.label, "epsilon")
        g.render("%s.gv" % filename, "output", format="png")
    
    def toJson(self):
        raise NotImplementedError

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.toJson())

class NFA(FA):
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.init = self.getInitState()

    def getInitState(self):
        for node in self.nodes:
            if node.init:
                return node

    def getAlphabet(self):
        result = set()
        for edge in self.edges:
            if edge.weight != "":
                result.add(edge.weight)
        return result
        
    def epsilon_closure(self, states):
        stack = []
        result = set()
        if isinstance(states, set):
            for state in states:
                stack.append(state)
                result.add(state)
        else:
            stack.append(states)
            result.add(states)
        while len(stack) > 0:
            item = stack.pop()
            for edge in self.edges:
                if edge.start == item and edge.weight == "":
                    stack.append(edge.end)
                    result.add(edge.end)
        return result

    def move(self, T, c):
        result = set()
        for edge in self.edges:
            for t in T:
                if edge.start == t and edge.weight == c:
                    result.add(edge.end)
        return result

    
    def toJson(self):
        data = {}
        for edge in self.edges:
            start = edge.start
            weight = edge.weight
            end = edge.end
            # Start
            if str(start.label) not in data.keys():
                if start.accept != None:
                    data[str(start.label)] = {
                        "edges":{},
                        "accept":start.accept
                    }
                else:
                    data[str(start.label)] = {
                        "edges":{}
                    }

            # End
            if str(end.label) not in data.keys():
                if end.accept != None:
                    data[str(end.label)] = {
                        "edges":{},
                        "accept":end.accept
                    }
                else:
                    data[str(end.label)] = {
                        "edges":{}
                    }
            
            d = data[str(start.label)]
            if weight not in d["edges"].keys():
                d["edges"][weight] = []
            d["edges"][weight].append(str(end.label))
        return json.dumps(data)

class DFA(FA):
    def __init__(self, NFA):
        self.nodes = None
        self.edges = None
        self.subsetConstuction(NFA)
        self.init = self.getInitState()

    def getInitState(self):
        for node in self.nodes:
            if node.init:
                return node

    def dfaNode(self, U):
        acceptState = None
        initState = False
        for i in U:
            if i.accept != None:
                acceptState = i.accept
            if i.init:
                initState = True
        return Node(reprTuple(U), acceptState, initState)

    def paths(self, state, c):
        result = []
        for edge in self.edges:
            if edge.start == state and edge.weight == c:
                result.append(edge)
        return result

    def subsetConstuction(self, NFA):
        nodes = set()
        edges = set()
        Dstates = set()
        markedDstates = set()
        alphabet = NFA.getAlphabet()
        U = NFA.epsilon_closure(NFA.nodes[0])
        nodes.add(self.dfaNode(U))
        Dstates.add(tuple(U))
        while len(Dstates - markedDstates) > 0:
            T = Dstates.pop()
            start = self.dfaNode(T)
            for a in alphabet:
                U = NFA.epsilon_closure(NFA.move(T, a))
                if len(U) == 0:
                    continue
                # print("%s (%s)> %s" % (reprTuple(T), a, reprTuple(U)))
                Dstates.add(tuple(U))
                end = self.dfaNode(U)
                nodes.add(end)
                edges.add(Edge(start, a, end))
            markedDstates.add(T)
        self.nodes = nodes
        self.edges = edges

    def expectedChars(self, state):
        result = []
        for edge in self.edges:
            if edge.start == state:
                result.append(edge)
        return result

    def parse(self, code):
        keywords = [
            "auto", "double", "int", "struct", "break", 
            "else", "long", "switch", "case", "enum", 
            "register", "typedef", "char", "extern", "return", 
            "union", "continue", "for", "signed", "void", 
            "do", "if", "static", "while", "default", 
            "goto", "sizeof", "volatile", "const", "float", 
            "short", "unsigned"
        ]
        i = 0
        state = self.init
        print("-" * 0x10 + " Code Begins " + "-" * 0x10)
        print(code)
        print("-" * 0x10 + " Code Ends " + "-" * 0x10)
        line = 0
        column = 0
        token = ""
        blank = [" ", "\t", "\n"]
        while True:
            c = code[i]
            # Refresh new line
            if c == "\n":
                column = 0
                line += 1
            # Apply automota
            ways = self.paths(state, c)
            if len(ways) == 0:
                if state.accept == None:
                    print("[%d:%d] %s excepted, got %r" % (line, column, ",".join(["%r" % i.weight for i in self.expectedChars(state)]), c))
                else:
                    print("TOKEN: <%s, %s>" % (state.accept, token))
                    state = self.init
                    token = ""
                    while True:
                        if i < (len(code) - 1) and code[i+1] in blank:
                            i += 1
                        else:
                            break
            elif len(ways) == 1:
                nstate = ways.pop().end
                token += c
                if nstate.accept != None:
                    # There are more chars in the input stream
                    if i < (len(code) - 1):
                        nextChar = code[i+1]
                        ways = self.paths(nstate, nextChar)
                        if len(ways) == 0:
                            if token in keywords and nstate.accept == "identifier":
                                print("TOKEN: <%s, %s>" % ("keywords", token))
                            else:
                                print("TOKEN: <%s, %s>" % (nstate.accept, token))
                            state = self.init
                            token = ""
                            while True:
                                if i < (len(code) - 1) and code[i+1] in blank:
                                    i += 1
                                else:
                                    break
                        elif len(ways) == 1:
                            state = ways.pop().end
                            token += nextChar
                            i += 1
                        else:
                            print("Wrong DFA")
                    else:
                        if token in keywords and nstate.accept == "identifier":
                            print("TOKEN: <%s, %s>" % ("keywords", token))
                        else:
                            print("TOKEN: <%s, %s>" % (nstate.accept, token))
                        print("TOKEN: <%s, %s>" % (nstate.accept, token))
                        state = self.init
                        token = ""
                        while True:
                            if i < (len(code) - 1) and code[i+1] in blank:
                                i += 1
                            else:
                                break
                else:
                    state = nstate
            else:
                print("Wrong DFA")
            # Update index
            i += 1
            column += 1
            if i >= len(code):
                break

    def getRenameTable(self):
        renameTable = {}
        init = None
        for i in self.nodes:
            if i.init:
                renameTable[str(i)] = "A"
                init = i
                break
        label = ord("B")
        for i in self.nodes:
            if i == init:
                continue
            renameTable[str(i)] = chr(label)
            label += 1
        return renameTable

    def toJson(self):
        data = {}
        renameTable = self.getRenameTable()
        for edge in self.edges:
            start = edge.start
            weight = edge.weight
            end = edge.end
            if renameTable[str(start)] not in data.keys():
                if start.accept != None:
                    data[renameTable[str(start)]] = {
                        "edges":{},
                        "accept":start.accept
                    }
                else:
                    data[renameTable[str(start)]] = {
                        "edges":{}
                    }
            d = data[renameTable[str(start)]]
            if weight not in d["edges"].keys():
                d["edges"][weight] = []
            d["edges"][weight].append(renameTable[str(end)])
        return json.dumps(data)

def mergeNFA():
    filenames = glob.glob("nfa/*.json")
    init = Node(label="Init", init=True)
    result = NFA([init], [])
    for filename in filenames:
        prefix = filename.split("nfa\\")[-1]
        print("Mergeing: %s" % (filename))
        nfa = importNFA(filename)
        print("-" * 0x10 + " %s " % (filename) + "-" * 0x10)
        nfa.visualize(prefix.split(".json")[0])
        print(nfa.toJson())
        for node in nfa.nodes:
            node.label = "%s-%s" % (prefix, node.label)
            if node.init:
                node.init = False
                result.edges.append(Edge(init, "", node))
            result.nodes.append(node)
        for edge in nfa.edges:
            # print(edge)
            result.edges.append(edge)
    with open("nfa.json", "w") as f:
        f.write(result.toJson())
    print("-" * 0x10 + " %s " % (filename) + "-" * 0x10)


def main():
    # Merge NFA of all tokens to a bigger one
    mergeNFA()
    # Import NFA
    nfa = importNFA("nfa.json")
    # nfa = importNFA("nfa/comment.json")
    # nfa = importNFA("nfa/delimeter.json")
    # nfa = importNFA("nfa/identifier.json")
    # nfa = importNFA("nfa/operator.json")
    # nfa = importNFA("nfa/unsigned.json")
    # nfa = importNFA("nfa/hex.json")

    # NFA to DFA
    dfa = DFA(nfa)
    dfa.save("dfa.json")
    dfa.visualize("dfa")

    # Read code
    code = open("code.c").read()

    # Parse code
    dfa.parse(code)

if __name__ == "__main__":
    main()