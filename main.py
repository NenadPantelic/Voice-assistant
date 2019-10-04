from controller.service_executor import ServiceExecutor
from services.text_processing.text_processor_service import TextProcessor
from services.speech.tts_service import Speaker
from services.speech.stt_service import SpeechRecognizer
from controller.controller import Controller
from services.webapi.imdb_service import IMDBService
from config.config import COMMANDS, logger
from utils.utils import load_json_data

from controller.command_resolver import CommandResolver
from services.webapi.owm_service import WeatherForecastService
from services.webapi.translation_service import TranslationService
from services.webapi.mail_service import MailService
from services.websearch.browser_search_service import BrowserService
from services.webapi.wikipedia_service import  WikipediaService

speaker = Speaker()
recognizer = SpeechRecognizer(language="en-US")
sp = TextProcessor()
service_pool = {

    "wikipedia": WikipediaService("en"),
    "owm": WeatherForecastService("en"),
    "translation": TranslationService(),
    "mail": MailService(),
    "imdb": IMDBService(),
    "browser": BrowserService(),
    # "system":OSService(),
    # connect arduino for this service
    # "arduino":ArduinoControlService()

}
commands = load_json_data(COMMANDS)
command_resolver = CommandResolver(sp, commands, 'en')
executor = ServiceExecutor(service_pool)
controller = Controller(recognizer, speaker, command_resolver, executor)

if __name__ == "__main__":
    controller.initialize()
    logger.debug("NEW SESSION BEGINS")
    while True:
        try:
            logger.debug("New command session....")
            controller.inform()
            controller.listen_and_execute()
        except KeyboardInterrupt:
            logger.debug("SESSION ENDS NOW")
            controller.finalize()

