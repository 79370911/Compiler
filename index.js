var fs = require('fs');

function getInputAlphabet(nfaTrans) {
    var result = new Set()
    Object.keys(nfaTrans).forEach(key => {
        Object.keys(nfaTrans[key]).forEach(c => {
            // Cause epsilon is not a type of input
            // So there is no need to add it to alphabet
            if (c != "") {
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
                dfaTrans.set(T, transition)
            })

            markedDfaStates.add(T)
        } else {
            break
        }
    }
    return dfaTrans
}



function main() {
    // Read NFA
    var NTrans = require('./nfa.json')

    // Convert NFA to DFA
    dfaTrans = subsetContruction(NTrans)
    console.log(dfaTrans)

    // Read code
    // fs.readFile('program.c', 'utf8', function(err, contents) {
    //     console.log(contents);
    // });

    // Parse code
}

main()