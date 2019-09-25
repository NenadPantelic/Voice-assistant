from service_executor import ServiceExecutor
from services.speech.text_processor_service import TextProcessor
from services.speech.tts_service import *
from services.speech.stt_service import *
# efrom config.constants import *
from controller import Controller
from services.webapi.imdb_service import IMDBService

langs = None
# INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"

speaker = Speaker()
srec = SpeechRecognizer(language="en-US")

if __name__ == "__main__":
    with open(r'data/languages.json') as json_file:
        langs = json.load(json_file)
        # speaker.speak(INIT_MESSAGE)
        # time.sleep(10)
        # l = srec.recognize_from_microphone()
        # langChoice = l.get_result().lower()
        # only Serbian and English will be available
        # print(langChoice)
        '''
        if "english" in langChoice or "default" in langChoice:
            langChoice = "en-US"
        elif "serbian" in langChoice:
            langChoice = "sr-RS"
        else:
            langChoice = None

        if langChoice is not None:
            srec.set_language(langChoice)
            speaker.set_language(langChoice)
            while True:
                command = srec.recognize_from_microphone().lower()
                speaker.speak("Command executed", str(get_current_timestamp()) + ".mp3")
        else:
            print(langChoice)

        '''

keywordsFiles = dict(en=ENGLISH_KEYWORDS)
keywords = {lang: load_json_data(keywordsFiles[lang]) for lang in keywordsFiles}

sp = TextProcessor()
from services.command_resolver import CommandResolver
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
    "system":OSService()

}
commands = load_json_data(ENGLISH_COMMANDS)

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
