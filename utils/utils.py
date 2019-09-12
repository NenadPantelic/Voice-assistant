
import time, json

def loggingException(exception):
    print("Exception message: {}".format(exception))

def getCurrentTimestamp():
    return time.time()

#semantic processing
def loadWordsDictionaries(languageWordFiles):
    languageWords = {}
    for language in languageWordFiles:
        with open(languageWordFiles.get(language, "en")) as f:
            languageWords[language] = json.load(f)
    return languageWords

def flattenDictionaryValues(dictionaryValues):
    flattenedList = []
    for list in dictionaryValues:
        flattenedList.extend(list)
    return flattenedList