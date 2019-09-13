import json

from controller import Controller
from services.speech.semantic_processor import SemanticProcessor
from services.speech.tts_service import  *
from services.speech.stt_service import *
from config.constants import  *
langs = None
#INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"

speaker = Speaker()
srec = SpeechRecognizer(language="en-US")

if __name__ == "__main__":
    with open(r'data/languages.json') as json_file:
        langs = json.load(json_file)
        #speaker.speak(INIT_MESSAGE)
        #time.sleep(10)
        #l = srec.recognizeFromMicrophone()
        #langChoice = l.getResult().lower()
        #only Serbian and English will be available
        #print(langChoice)
        '''
        if "english" in langChoice or "default" in langChoice:
            langChoice = "en-US"
        elif "serbian" in langChoice:
            langChoice = "sr-RS"
        else:
            langChoice = None

        if langChoice is not None:
            srec.setLanguage(langChoice)
            speaker.setLanguage(langChoice)
            while True:
                command = srec.recognizeFromMicrophone().lower()
                speaker.speak("Command executed", str(getCurrentTimestamp()) + ".mp3")
        else:
            print(langChoice)

        '''

keywordsFiles = dict(en=ENGLISH_KEYWORDS)
keywords = {lang:loadJsonData(keywordsFiles[lang]) for lang in keywordsFiles}

sp = SemanticProcessor()
from services.command_resolver import CommandResolver
from services.websearch import wikipedia_search
#from services.websearch import * #import WikipediaService

servicePool = {

    "wikipedia": wikipedia_search.WikipediaService("en")

}
commands = loadJsonData(ENGLISH_COMMANDS)

sr = CommandResolver(sp, commands, keywords['en'])
#sr.calculateServiceScores(words)
controller = Controller(srec, speaker, sr, servicePool=servicePool)
#print(controller.determineExecutor("Linda, who is Who is Vladimir Putin"))
controller.determineExecutor("Linda, who is Who is Vladimir Putin")

