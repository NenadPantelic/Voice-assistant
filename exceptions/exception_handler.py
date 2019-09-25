from config.constants import EXCEPTION_MESSAGES, SUCCESS, logger
from utils.utils import convert_instance_type_to_str
import traceback


class ExceptionHandler:

    @staticmethod
    def check_exception_existence(actionResultCode, language, messages):
        message = None
        if actionResultCode != SUCCESS:
            message = messages
        return message

    #def get_appropriate

    @staticmethod
    def get_exception_message(exceptionCode, language):
        return EXCEPTION_MESSAGES[exceptionCode][language]
    @staticmethod
    def get_exception_message(e, language):
        logger.warning("An exception occured.")
        exception_type = convert_instance_type_to_str(type(e))
        message = EXCEPTION_MESSAGES[exception_type][language]
        traceback_message = traceback.format_exc()
        logger.error(traceback_message)
        return message



