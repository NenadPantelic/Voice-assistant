class ActionResult:
    def __init__(self, result, status):
        self.__result = result
        self.__status = status

    # getters
    def getResult(self):
        return self.__result

    def getStatus(self):
        return self.__status

    #setters
    def setResult(self, result):
        self.__result = result

    def setStatus(self, status):
        self.__status = status