class ActionResult:
    def __init__(self, result, status, language=None):
        self.__result = result
        self.__status = status
        self.__language = language

    def __str__(self):
        return "ActionResult = [result = {}, status = {}, language = {}].".format(self.get_result(), self.get_status(),
                                                                                  self.get_language())

    # getters
    def get_result(self):
        return self.__result

    def get_status(self):
        return self.__status

    def get_language(self):
        return self.__language

    # setters
    def set_result(self, result):
        self.__result = result

    def set_status(self, status):
        self.__status = status

    def set_language(self, language):
        assert isinstance(language, str)
        self.__language = language
