

PROVIDED_LANGUAGES = {
        "english",
        "serbian"

}
RECOGNITION_METHODS = {

        "bing" : "recognize_bing",
        "google" : "recognize_google",
        "google_cloud" : "recognize_google_cloud",
        "houndify" : "recognize_houndify",
        "ibm" : "recognize_ibm",
        "sphinx" : "recognize_sphinx",
        "wit" : "recognize_wit",
        "azure" : "recognize_azure"

}

'''
recognize_bing(): Microsoft Bing Speech
recognize_google(): Google Web Speech API
recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
recognize_houndify(): Houndify by SoundHound
recognize_ibm(): IBM Speech to Text
recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
recognize_wit(): Wit.ai


'''

#region MESSAGES

INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"
OK = 0

#exception constants
DEFAULT_EXCEPTION = 100
#speech recognition - 2xx
UNKNOWN_SPEECH_VALUE_EXCEPTION = 201
REQUEST_SPEECH_EXCEPTION = 202


#tts audio config

PATH_TO_AUDIO_DIR = r"data/audio/"
DEFAULT_AUDIO_FILE = PATH_TO_AUDIO_DIR + "temporary.mp3"



#semantic processor
ENGLISH_DICTIONARY_PATH: str = "data/words/words-en.json"
SERBIAN_DICTIONARY_PATH = "data/words/words-sr.json"

#keywords
ENGLISH_KEYWORDS:str = "data/keywords/keywords-en.json"


#answers
ENGLISH_ANSWERS:str = "data/answers/answers-en.json"



#commands
ENGLISH_COMMANDS = "data/commands/commands-en.json"
#TODO: refactor path variables to be in dictionary form for simpler usage


