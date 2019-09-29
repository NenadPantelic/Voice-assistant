class ActionResult:
    def __init__(self, result, status, language=None):
        """
        :param str result: result of service command execution
        :param int status: SUCCESS = 1 or FAIL = 0, FATAL = -1
        :param str language: lang_code (in which _language, command result should be spoken)
        """
        self._result = result
        self._status = status
        self._language = language

    def __str__(self):
        return "ActionResult = [result = {}, status = {}, _language = {}].".format(self.get_result(), self.get_status(),
                                                                                  self.get_language())

    # getters
    def get_result(self):
        return self._result

    def get_status(self):
        return self._status

    def get_language(self):
        return self._language

    # setters
    def set_result(self, result):
        self._result = result

    def set_status(self, status):
        self._status = status

    def set_language(self, language):
        assert isinstance(language, str)
        self._language = language
