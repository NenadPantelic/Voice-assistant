import json
from services.tts_service import  *
from services.stt_service import *
from utils.utils import  *
from config.constants import  *
langs = None
#INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"

speaker = Speaker()
srec = SpeechRecognizer(language="en-US")

if __name__ == "__main__":
    with open(r'data/languages.json') as json_file:
        langs = json.load(json_file)
        speaker.speak(INIT_MESSAGE)
        langChoice = srec.recognizeFromMicrophone().lower()
        #only Serbian and English will be available
        print(langChoice)
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





