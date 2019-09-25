# - *- coding: utf- 8 - *-


import logging

logging.basicConfig(level=logging.DEBUG, filename="voice_assistant.log", \
                   format='%(asctime)s: %(levelname)s - %(message)s',\
                   datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging

#logging  - debug, info, warning, error, critical

PROVIDED_LANGUAGES = {
    "english": "en-US",
    "serbian": "sr-RS",
    "default": "en-US"

}

LANGUAGES_IN_SERBIAN = "data/langs_in_serbian.json"
LANG_CODES = "data/langs_codes.json"
RECOGNITION_METHODS = {

    "bing": "recognize_bing",
    "google": "recognize_google",
    "google_cloud": "recognize_google_cloud",
    "houndify": "recognize_houndify",
    "ibm": "recognize_ibm",
    "sphinx": "recognize_sphinx",
    "wit": "recognize_wit",
    "azure": "recognize_azure"

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

# tts audio config

PATH_TO_AUDIO_DIR = r"data/audio/"
DEFAULT_AUDIO_FILE = PATH_TO_AUDIO_DIR + "temporary.mp3"

# semantic processor
ENGLISH_DICTIONARY_PATH = "data/words/words-en.json"
SERBIAN_DICTIONARY_PATH = "data/words/words-sr.json"

# keywords
ENGLISH_KEYWORDS = "data/keywords/keywords-en.json"
SERBIAN_KEYWORDS = "data/keywords/keywords-sr.json"

LANG_KEYWORDS = {
    "en": ENGLISH_KEYWORDS,
    "sr": SERBIAN_KEYWORDS
}

# answers
ENGLISH_ANSWERS = "data/answers/answers-en.json"

# commands
ENGLISH_COMMANDS = "data/commands/commands-en.json"
# ENGLISH_COMMANDS = "data/commands/commands-sr.json"
# TODO: refactor path variables to be in dictionary form for simpler usage

# INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating language. Default option is English(USA)!"
SUCCESS = 1
FAIL = 0

# exception constants
DEFAULT_EXCEPTION = 100
# speech recognition - 2xx
UNKNOWN_SPEECH_VALUE_EXCEPTION = 201
REQUEST_SPEECH_EXCEPTION = 202

TEXT_TO_SPEECH_EXCEPTION = 301

NO_GOOGLE_RESULT = 403

# exception messages
EXCEPTION_MESSAGES = {
    UNKNOWN_SPEECH_VALUE_EXCEPTION: {
        "en": "Speech cannot be analyzed and/or recognized!",
        "sr": "Ваш говор не може бити обрађен или препознат!"
    },
    REQUEST_SPEECH_EXCEPTION: {
        "en": "Request error problem. Check API limits and connectivity status!",
        "sr": "Проблеми са слањем захтева. Проверите АПИ лимите и статус мреже!"
    },

    DEFAULT_EXCEPTION: {
        "en": "",
        "sr": "Дошло је до неке грешке. Оригинална порука грешке на енглеском је: "
    },
    TEXT_TO_SPEECH_EXCEPTION: {
        "en": "",
        "sr": "Дошло је до неке грешке. Оригинална порука грешке на енглеском је: "

    },

    NO_GOOGLE_RESULT: {
        "en": "Hmm, Google cannot find anything that matches your query. Are you sure you query is valid?",
        "sr": "Nažalost, Google ne može da nađe ništa vezano za tvoj upit. Da li si siguran da je tvoj upit validan?"
    }
}
GENERIC_MESSAGE_EN = "Some internal error occurred. Check log for more details!"
GENERIC_MESSAGE_SR = "Došlo je do interne greške. Proverite log fajl za više detalja!"
EXCEPTION_MESSAGES = {
    "KeyError": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    },
    "TypeError": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    },
    "ValueError": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    },
    "AssertionError": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    },
    "IndexError": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    },
    UNKNOWN_SPEECH_VALUE_EXCEPTION: {
        "en": "Speech cannot be analyzed and/or recognized!",
        "sr": "Ваш говор не може бити обрађен или препознат!"
    },
    REQUEST_SPEECH_EXCEPTION: {
        "en": "Request error problem. Check API limits and connectivity status!",
        "sr": "Проблеми са слањем захтева. Проверите АПИ лимите и статус мреже!"
    },

    DEFAULT_EXCEPTION: {
        "en": "",
        "sr": "Дошло је до неке грешке. Оригинална порука грешке на енглеском је: "
    },
    TEXT_TO_SPEECH_EXCEPTION: {
        "en": "",
        "sr": "Дошло је до неке грешке. Оригинална порука грешке на енглеском је: "

    },

    NO_GOOGLE_RESULT: {
        "en": "Hmm, Google cannot find anything that matches your query. Are you sure you query is valid?",
        "sr": "Nažalost, Google ne može da nađe ništa vezano za tvoj upit. Da li si siguran da je tvoj upit validan?"
    }
}

# credentials

OWM_API_KEY = "5ab8013f8b3c54d28b8f8035ffd40f0a"
OMDB_API_KEY = '56674ea0'

PROXY_MAIL = "lindo.voice.assistant@gmail.com"
MAIL_PASSWORD = "mizcechlykbgsfhx"

# weather params
# NOTE: only some of params are included (most important ones)
WEATHER_PARAMS = {'clouds', 'detailed_status', 'dewpoint', 'heat_index', 'humidex', 'humidity', 'pressure', 'rain', \
                  'reference_time', 'snow', 'status', 'sunrise_time', 'sunset_time', 'temperature',
                  'visibility_distance', \
                  'weather_code', 'weather_icon_name', 'weather_icon_url', 'wind'}

# format <name in json response>: (json_subvalue or alias, child/alias, display name)
# hr stands for croatian language beacuse OWM API doesn't support serbian, so instead of serbian (sr),
# croatian language is used (hr)

WEATHER_PARAMETERS = {
    "clouds": ("clouds", "alias", {"en": "clouds", "hr": "oblačnost"}),
    "pressure": ("press", "child", {"en": "pressure", "hr": "pritisak"}),
    "wind": ("speed", "child", {"en": "wind speed", "hr": "brzina vetra"}),
    # "snow":("snow", "child", ),
    "humidity": ("humidity", "alias", {"en": "humidity", "hr": "vlažnost vazduha"}),
    "temperature_min": ("temp_min", "child", {"en": "minimum temperature", "hr": "minimalna dnevna temperatura"}),
    "temperature_max": ("temp_max", "child", {"en": "maximum temperature", "hr": "maksimalna dnevna temperatura"}),
    "temperature": ("temp", "child", {"en": "temperature", "hr": "prosečna dnevna temperatura"}),
    "detailed_status": ("detailed_status", "alias", {"en": "detailed status", "hr": "detaljniji opis"})
    # "rain":{}

}

# social networks urls

FACEBOOK_BASE_URL = "https://www.facebook.com/"
TWITTER_BASE_URL = "https://twitter.com/"
INSTAGRAM_BASE_URL = "https://instagram.com/"
LINKEDIN_BASE_URL = "https://www.linkedin.com/in/"
