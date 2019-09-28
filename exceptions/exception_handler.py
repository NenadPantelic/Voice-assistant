from config.constants import EXCEPTION_MESSAGES, logger
from utils.utils import convert_instance_type_to_str
import traceback

class ExceptionHandler:

    @staticmethod
    def get_exception_message(e, language):
        """
        Logs traceback message and get appropriate exception message from config file.
        :param exception e: exception to be handled
        :param str language: language code
        :rtype: str
        :return: an exception message that will be delivered to the user
        """
        logger.warning("An exception occurred.")
        exception_type = convert_instance_type_to_str(type(e))
        message = EXCEPTION_MESSAGES.get(exception_type, "exception")[language]
        traceback_message = traceback.format_exc()
        logger.error(traceback_message)
        return message



