import json

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
        speaker.speak(INIT_MESSAGE)
        #time.sleep(10)
        l = srec.recognizeFromMicrophone()
        langChoice = l.getResult().lower()
        #only Serbian and English will be available
        print(langChoice)
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

sp = SemanticProcessor()
print(sp.filterOutWords(sp.filterOutSpecialChars('Linda, you should listen what I am speaking to you')))

