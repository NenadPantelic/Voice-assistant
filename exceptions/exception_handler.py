
from config.constants import EXCEPTION_MESSAGES, OK

class ExceptionHandler:

    @staticmethod
    def checkExceptionExistence(actionResultCode, language):
        message = ""
        if actionResultCode != OK:
            message = ExceptionHandler.getExceptionMessage(actionResultCode, language)
        return message

    @staticmethod
    def getExceptionMessage(exceptionCode, language):
        return EXCEPTION_MESSAGES[exceptionCode][language]

