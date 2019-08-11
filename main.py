import json
from services.tts_service import  *
from services.stt_service import *
langs = None
INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"

speaker = Speaker()
srec = SpeechRecognizer(language="en-US")

if __name__ == "__main__":
    with open(r'data/languages.json') as json_file:
        langs = json.load(json_file)
        speaker.speak(INIT_MESSAGE)
        print(srec.recognizeFromMicrophone())




