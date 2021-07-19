data = {}
domains = {}
variables = []


def handleInput(lhsString):
    words = []
    wordsAndOperators = []
    tmpWord = ""
    for i in range(len(lhsString)):
        if (
            lhsString[i] != "+"
            and lhsString[i] != "-"
            and lhsString[i] != "*"
            and lhsString[i] != "("
            and lhsString[i] != ")"
        ):
            tmpWord += lhsString[i]
        else:
            if tmpWord != "":
                words.append(tmpWord)
                wordsAndOperators.append(tmpWord)
            wordsAndOperators.append(lhsString[i])
            tmpWord = ""
    words.append(tmpWord)
    wordsAndOperators.append(tmpWord)

    return words, wordsAndOperators


def readInputFile(path):
    data = {}
    with open(path, "r") as inputFile:
        firstLine = inputFile.readline()
        (data["LHS"], data["LHSAndOperators"]) = handleInput(firstLine.split("=")[0])
        data["RHS"] = firstLine.split("=")[-1]
    return data


def writeOutputFile(path, result):
    with open(path, "w") as outputFile:
        if isinstance(result, str):
            outputFile.write(result)
        else:
            outputFile.write("".join([str(v) for v in result.values()]))
    return True


def getVariables(data):
    variables = []
    for operand in data["LHS"]:
        variables += list(operand)
    variables += list(data["RHS"])
    return list(set(variables))


def getDomains(letters):
    possibleDigits = {}
    for letter in letters:
        possibleDigits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    maxOperandLength = len(data["LHS"][0])
    possibleDigits[data["LHS"][0][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for operand in data["LHS"][1:]:
        possibleDigits[operand[0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if maxOperandLength < len(operand):
            maxOperandLength = len(operand)
    if len(data["RHS"]) > maxOperandLength:
        possibleDigits[str(list(data["RHS"])[0])] = [1]
    else:
        possibleDigits[str(list(data["RHS"])[0])] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    return possibleDigits


def isSatisfied(assignedVariables):
    if len(set(assignedVariables.values())) < len(assignedVariables):
        return False

    if len(assignedVariables) == len(variables):
        unit = 1
        lhsNumbers = []
        tmpNumber = 0
        tmpWord = ""
        assignedWords = {}
        for index in range(len(data["LHS"])):
            for letter in reversed(data["LHS"][index]):
                tmpNumber += assignedVariables[letter] * unit
                tmpWord += letter
                unit = unit * 10
            lhsNumbers.append(tmpNumber)
            assignedWords[tmpWord[::-1]] = tmpNumber
            tmpNumber = 0
            tmpWord = ""
            unit = 1

        rhsNumber = 0
        unit = 1
        for letter in reversed(data["RHS"]):
            rhsNumber += assignedVariables[letter] * unit
            unit = unit * 10

        expression = data["LHSAndOperators"].copy()
        for word in assignedWords.keys():
            foundIndexes = [index for index, w in enumerate(expression) if word == w]
            for i in foundIndexes:
                expression[i] = str(assignedWords[word])
        lhsResult = eval("".join(expression))

        return lhsResult == rhsNumber

    return True


def backtrack(assignedVariables):
    if len(assignedVariables) == len(variables):
        return assignedVariables

    unassignedVariables = [v for v in variables if v not in assignedVariables]

    firstUnassignedVariable = unassignedVariables[0]
    for value in domains[firstUnassignedVariable]:
        localAssignedVariables = assignedVariables.copy()
        localAssignedVariables[firstUnassignedVariable] = value
        if isSatisfied(localAssignedVariables):
            result = backtrack(localAssignedVariables)
            if result is not None:
                return result
    return None


def sortResult(result):
    if result == None:
        return "NO SOLUTION"
    sortedKeys = sorted(result.keys())
    newResult = {}
    for key in sortedKeys:
        newResult[key] = result[key]
    return newResult


import time

start_time = time.time()

data = readInputFile("input11.txt")
variables = getVariables(data)
domains = getDomains(variables)

result = sortResult(backtrack({}))
writeOutputFile("output11.txt", result)

print("--- %s seconds ---" % (time.time() - start_time))