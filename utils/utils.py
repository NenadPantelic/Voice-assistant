
import time, json
import uuid


def loggingException(exception):
    print("Exception message: {}".format(exception))

def getCurrentTimestamp():
    return time.time()

def generateUUID():
   return str(uuid.uuid4())

#semantic processing
def loadWordsDictionaries(languageWordFiles):
    languageWords = {}
    for language in languageWordFiles:
        with open(languageWordFiles.get(language, "en")) as f:
            languageWords[language] = json.load(f)
    return languageWords

def loadJsonData(jsonFilePath):
    with open(jsonFilePath) as f:
        data = json.load(f)
    return data


def flattenDictionaryValues(dictionaryValues):
    flattenedList = []
    for list in dictionaryValues:
        flattenedList.extend(list)
    return flattenedList