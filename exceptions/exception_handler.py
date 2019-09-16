from config.constants import EXCEPTION_MESSAGES, OK


class ExceptionHandler:

    @staticmethod
    def check_exception_existence(actionResultCode, language):
        message = None
        if actionResultCode != OK:
            message = ExceptionHandler.get_exception_message(actionResultCode, language)
        return message

    @staticmethod
    def get_exception_message(exceptionCode, language):
        return EXCEPTION_MESSAGES[exceptionCode][language]
