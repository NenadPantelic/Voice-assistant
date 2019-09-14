
from config.constants import EXCEPTION_MESSAGES, OK

class ExceptionHandler:

    @staticmethod
    def hasException(actionResultCode):
        return actionResultCode != OK
    @staticmethod
    def checkExceptionExistence(actionResultCode, language):
        message = None
        if ExceptionHandler.hasException(actionResultCode) != OK:
            message = ExceptionHandler.getExceptionMessage(actionResultCode, language)
        return message

    @staticmethod
    def getExceptionMessage(exceptionCode, language):
        return EXCEPTION_MESSAGES[exceptionCode][language]

