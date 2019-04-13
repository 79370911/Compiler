var fs = require('fs');

function getInputAlphabet(nfaTrans) {
    var result = new Set()
    Object.keys(nfaTrans).forEach(key => {
        Object.keys(nfaTrans[key]).forEach(c => {
            // Cause epsilon is not a type of input
            // So there is no need to add it to alphabet
            // c.length == 1 to distinct ACCEPT and input char
            if (c != "" && c.length == 1) {
                result.add(c)
            }
        })
    });
    return result
}

function epsilonClosure(nfaTrans, states) {
    // Push all states to stack
    var stack = new Array()
    states.forEach(x => {
        stack.push(x)
    })
    var result = new Set()
    while (true) {
        if (stack.length > 0) {
            state = stack.pop()
            // Every state has an epsilon edge pointing to itself
            result.add(parseInt(state, 10))
            if (nfaTrans[state] != undefined) {
                Object.keys(nfaTrans[state]).forEach(key => {
                    if ("" == key) {
                        nfaTrans[state][""].forEach(e => {
                            result.add(e)
                            stack.push(e)
                        })
                    }
                })
            }
        } else {
            break
        }
    }
    return result
}

function move(nfaTrans, T, input) {
    result = new Set()
    T.forEach(key => {
        nextStates = nfaTrans[key][input]
        if (nextStates != undefined) {
            nextStates.forEach(x => {
                result.add(x)
            })
        }
    })
    return result
}

function equalsSet(setA, setB) {
    var a_b = new Set([...setA].filter(x => !(setB.has(x) || setB.has(x.toString()))))
    var b_a = new Set([...setB].filter(x => !(setA.has(x) || setA.has(x.toString()))))
    return a_b.size == 0 && b_a.size == 0
}

function differenceSet(setA, setB) {
    result = new Set()
    setA.forEach(x => {
        if (!setB.has(x)) {
            result.add(x)
        }
    })
    return result
}

function subsetContruction(nfaTrans) {
    // Declarations
    var dfaStates = new Set()
    var markedDfaStates = new Set()
    var dfaTrans = new Map();
    // Parse accept states of NFA transition table
    var nfaAcceptStates = getAcceptStates(nfaTrans)
    console.log(nfaAcceptStates)

    // Get input alphabet
    var inputAlphabet = getInputAlphabet(nfaTrans)

    // initially, t-closure(s0) is the only state in Dstates, and it is unmarked;
    dfaStates.add(epsilonClosure(nfaTrans, ["0"]))

    while (true) {
        // Get all unmarked state of DFA
        var difference = differenceSet(dfaStates, markedDfaStates)

        if (difference.size > 0) {
            // WTF??? every item in entries() has the same key and value. R U kidding me?
            T = difference.entries().next().value[0]

            inputAlphabet.forEach(a => {
                // Calculate epsilon-closure(move(T, a))
                acceptStates = move(nfaTrans, T, a)
                U = epsilonClosure(nfaTrans, acceptStates)

                // Judge whether the state exists in the states of DFA
                var exists = false
                dfaStates.forEach(x => {
                    if (equalsSet(x, U)) {
                        exists = true
                    }
                })
                if (!exists) {
                    dfaStates.add(U)
                }

                // Update transition table of DFA
                if (dfaTrans.get(T) == undefined) {
                    dfaTrans.set(T, {})
                }

                transition = dfaTrans.get(T)
                transition[a] = U
                // Mark accept states of DFA transition table
                T.forEach(nfaState => {
                    nfaAcceptStates.forEach(function(v, k, m) {
                        // console.log("nfaAcceptState: " + k)
                        // console.log("nfaState: " + nfaState)
                        if (nfaState == k) {
                            // console.log("T should be an accept state")
                            // console.log(T)
                            // console.log(v)
                            transition["ACCEPT"] = v
                        }
                    })
                })
                
                // console.log(transition)

                dfaTrans.set(T, transition)
            })

            markedDfaStates.add(T)
        } else {
            break
        }
    }
    return dfaTrans
}

function elementExists(set, element) {
    set.forEach(x => {
        var result = equalsSet(x, element)
        console.log(result)
        if (result) {
            return true
        }
    })
    return false
}

function getAllStates(transitionTable) {
    var result = new Set()
    transitionTable.forEach(function (value, key, map) {
        result.add(key)
    })
    return result
}

function isAcceptState(nfaTrans, state) {
    // TODO
    return true
}

function getValueBySetKey(map, key) {
    var result = undefined
    map.forEach(function(v, k, m) {
        // Accept states
        if (Object.prototype.toString.apply(key) == "[object Set]") {
            if (equalsSet(k, key)) {
                result = v            
            }   
        }
    })
    return result
}

function visualize(transitionTable) {
    // Get all state of DFA
    states = getAllStates(transitionTable)

    // Assign label for every state
    var labels = new Map()
    var labelCharCode = "A".charCodeAt()
    states.forEach(x => {
        labels.set(x, String.fromCharCode(labelCharCode))
        labelCharCode += 1
    })
    
    // Generate dot script
    var dotScript = ""
    dotScript += "digraph dfa {\n"
    dotScript += "    rankdir=LR;\n"
    labels.forEach(function(value, key, map) {
        dotScript += "    node [shape = circle, label = \"" + value 
            // + " = {" + [...key].join(", ") + "}"
            + "\"]; " + value + ";\n"
    })
    dfaTrans.forEach(function(value, key, map) {
        Object.keys(value).forEach(y => {
            dotScript += "    " + getValueBySetKey(labels, key) + " -> " + getValueBySetKey(labels, value[y]) + " [ label = \"" + y + "\" ];\n"
        })
    })
    dotScript += "}\n"

    return dotScript
}


function DFA(dfaTrans, data) {
    // Initial state
    var state = dfaTrans.keys().next().value
    var i = 0
    while (true) {
        var input = data[i]
        s = getValueBySetKey(dfaTrans, state)[input]

        if (s != undefined) {
            state = s
            // Accept state
            if (isAcceptState(s)) {
                // TODO : when to break
                break
            }
        } else {
            console.log(Object.keys(dfaTrans.get(state)) + " expected, got: " + input)
            break
        }
    }
    if (i == data.length) {
        console.log("Succeed")
    }
}

function getAcceptStates(nfaTrans) {
    var result = new Map()
    Object.keys(nfaTrans).forEach(key => {
        Object.keys(nfaTrans[key]).forEach(c => {
            // Cause epsilon is not a type of input
            // So there is no need to add it to alphabet
            // c.length == 1 to distinct ACCEPT and input char
            if (c == "ACCEPT") {
                result.set(parseInt(key, 10), nfaTrans[key][c])
            }
        })
    });
    return result
}



function main() {
    // Read NFA
    var nfaTrans = require('./nfa.json')
    console.log(nfaTrans)

    // Convert NFA to DFA
    dfaTrans = subsetContruction(nfaTrans)
    console.log(dfaTrans)

    // Visualize tranition table
    var dotScript = visualize(dfaTrans)

    // Read code
    fs.readFile('program.c', 'utf8', function(err, data) {
        console.log(data);
        // Parse code
        DFA(dfaTrans, data)
    });

}

main()