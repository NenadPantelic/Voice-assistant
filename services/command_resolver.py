
from config.constants import ENGLISH_COMMANDS
from utils.utils import loadWordsDictionaries, flattenDictionaryValues, loadJsonData

#languageWordFiles = dict(en=ENGLISH_DICTIONARY_PATH, sr=SERBIAN_DICTIONARY_PATH)
#keywordsFiles = dict(en=ENGLISH_KEYWORDS)



class CommandResolver:

    def __init__(self, textProcessor, commands, keywords):
        self.__textProcessor = textProcessor
        self.__keywords = keywords
        self.__commands = commands


    def calculateCommandScores(self, wordList):
        scores = {}
        #TODO:change input type of wordList to string (currently is list)
        wordList = ' '.join(wordList)
        for command in self.__keywords:
            words = command["words"]
            scores[command["commandId"]] = sum([words.get(word, 0) * wordList.count(word) \
                                                             for word in words if word in wordList])
        return scores

    #TODO: check what to use - phrases or single words
    def getCommand(self, text):
        wordList = self.__textProcessor.preprocessText(text)
        scoreMap = self.calculateCommandScores(wordList)
        maxScore = max(scoreMap.values())
        candidateMethods = [method for method in scoreMap if scoreMap[method] == maxScore]
        if(len(candidateMethods) > 1):
            #TODO:solve scenario when multiple methods have the same score
            candidateMethod = self.getMostProbableCommand(candidateMethods)
        else:
            candidateMethod = [command for command in self.__commands if command["id"] == candidateMethods[0]][0]
        print(candidateMethod)
        #targetService = candidateMethod["service"]
        #targetMethod = candidateMethod["methodName"]
        #nextCommand = candidateMethod["nex"]
        #query = self.__textProcessor.filterOutKeywords(wordList, self.__keywords[targetService][targetMethod].keys())
        #return dict(zip(["service", "method", "arg", "score"], [targetService, targetMethod, query, maxScore]))
        return candidateMethod.update({"maxScore":maxScore})

    def getMostProbableCommand(self, commands):
        pass





