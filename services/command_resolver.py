

def convertJsonArrayToDict(jsonArray):
    resultingMap = {}
    for element in jsonArray:
        resultingMap[element["commandId"]] = element
    return resultingMap

class CommandResolver:

    def __init__(self, textProcessor, commands, keywords):
        self.__textProcessor = textProcessor
        self.__keywords = convertJsonArrayToDict(keywords)
        self.__commands = convertJsonArrayToDict(commands)


        self.__command = None
        self.__previousCommandId = None
        self.__nextCommandId = None

    def calculateCommandScores(self, wordList):
        scores = {}
        #TODO:change input type of wordList to string (currently is list)
        wordList = ' '.join(wordList)
        for commandId, command in self.__keywords.items():
            words = command["words"]
            scores[commandId] = sum([words.get(word, 0) * wordList.count(word) \
                                                             for word in words if word in wordList])
        return scores

    #TODO: check what to use - phrases or single words
    def getCommand(self, text):
        init = True
        wordList = []
        if(text is not None):
            wordList = self.__textProcessor.preprocessText(text)
            init = False

        self.determineCommand(init, wordList)
        targetCommand = self.command
        if (targetCommand["hasArgs"]):
            arg = wordList
            if(targetCommand["processInputText"]):
                arg = self.__textProcessor.filterOutKeywords(wordList, self.__keywords[self.command["commandId"]]["words"].keys())
            targetCommand.update({"arg": arg})
        return targetCommand

    def determineCommand(self, init = False, wordList = []):
        if(init):
            self.command = self.getDefaultCommand()
        elif(self.__nextCommandId is None):
            scoreMap = self.calculateCommandScores(wordList)
            maxScore = max(scoreMap.values())
            candidateCommands = list(filter(lambda x:x[1] == maxScore, scoreMap.items()))
            if(len(candidateCommands) > 1):
                #TODO:solve scenario when multiple methods have the same score
                self.command = self.getMostProbableCommand(candidateCommands)
            else:
                self.command = self.__commands[candidateCommands[0][0]]
            self.previousCommandId = self.command["previousCommandId"]
        else:
            self.previousCommandId = self.command["commandId"]
            self.command = self.FindCommandById(self.nextCommandId)

        self.nextCommandId = self.command["nextCommandId"]

    def getMostProbableCommand(self, commands):
        pass

    def getDefaultCommand(self):
        #one command with no service and method should be set
        return list(filter(lambda x: x["service"] is None and x["method"] is None, self.__commands.values()))[0]

    #helper method
    def getCommandKeywords(self, commandId):
        words =  [command["words"] for command in self.__keywords if command["commandId"] == commandId]
        return words[0] if len(words) == 1 else None

    def FindCommandById(self, commandId):
        return self.__commands.get(commandId, None)









