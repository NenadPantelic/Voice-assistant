from services.common.service_executor import ServiceExecutor
from services.common.text_processor_service import TextProcessor
from services.speech.tts_service import Speaker
from services.speech.stt_service import SpeechRecognizer
from controller import Controller
from services.webapi.imdb_service import IMDBService
from config.config import COMMANDS, logger
from utils.utils import load_json_data

from services.common.command_resolver import CommandResolver
from services.webapi.owm_service import WeatherForecastService
from services.webapi.translation_service import TranslationService
from services.webapi.mail_service import MailService
from services.websearch.browser_search_service import BrowserService
from services.webapi.wikipedia_service import  WikipediaService
from services.system.os_service import OSService
from time import sleep

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
    while True:
        try:
            logger.debug("New command session....")
            controller.listen_and_execute()
        except KeyboardInterrupt:
            controller.finalize()
