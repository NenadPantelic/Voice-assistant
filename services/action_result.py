class ActionResult:
    def __init__(self, result, status):
        self.__result = result
        self.__status = status

    # getters
    def get_result(self):
        return self.__result

    def get_status(self):
        return self.__status

    #setters
    def set_result(self, result):
        self.__result = result

    def set_status(self, status):
        self.__status = status