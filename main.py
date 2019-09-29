from services.common.service_executor import ServiceExecutor
from services.common.text_processor_service import TextProcessor
from services.speech.tts_service import *
from services.speech.stt_service import *
# efrom config.constants import *
from controller import Controller
from services.webapi.imdb_service import IMDBService

from utils.utils import load_json_data

langs = None
# INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating _language. Default option is English(USA)!"

speaker = Speaker()
srec = SpeechRecognizer(language="en-US")

if __name__ == "__main__":
    print("start")

keywordsFiles = dict(en=ENGLISH_KEYWORDS)
keywords = {lang: load_json_data(keywordsFiles[lang]) for lang in keywordsFiles}

sp = TextProcessor()
from services.common.command_resolver import CommandResolver
from services.webapi import wikipedia_service
from services.webapi.owm_service import WeatherForecastService
from services.webapi.translation_service import TranslationService
from services.webapi.mail_service import MailService
from services.websearch.browser_search_service import BrowserService
# from services.websearch import * #import WikipediaService
from services.system.os_service import  OSService

service_pool = {

    "wikipedia": wikipedia_service.WikipediaService("en"),
    "owm": WeatherForecastService("en"),
    "translation": TranslationService(),
    "mail": MailService(),
    "imdb": IMDBService(),
    "browser":BrowserService(),
    "system":OSService(),
    #"arduino":ArduinoControlService()

}
commands = load_json_data(COMMANDS)

sr = CommandResolver(sp, commands, 'en')
executor = ServiceExecutor(service_pool)
# sr.calculateServiceScores(words)
controller = Controller(srec, speaker, sr, executor)
# print(controller.execute("Linda, who is Who is Vladimir Putin"))
# print(controller.execute(None))
# print(controller.execute("I'm choosing serbian."))

# print(controller.listen_and_execute(True))
print(controller.initialize())
controller.listen_and_execute()
controller.listen_and_execute()
controller.listen_and_execute()
controller.listen_and_execute()
controller.listen_and_execute()
controller.listen_and_execute()
