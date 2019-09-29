# - *- coding: utf- 8 - *-


import logging
import os

logging.basicConfig(level=logging.DEBUG, filename="voice_assistant.log", \
                    format='%(asctime)s: %(levelname)s - %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging

# logging  - debug, info, warning, error, critical

PROVIDED_LANGUAGES = {
    "english": "en-US",
    "serbian": "sr-RS",
    "default": "en-US"

}

LANGUAGES_IN_SERBIAN = os.path.abspath("data/langs_in_serbian.json")
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

# _tts audio config

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

# INIT_MESSAGE = "Hi, I'm Lindo voice assistant. Choose operating _language. Default option is English(USA)!"
SUCCESS = 1
FAIL = 0
FATAL = -1

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
    "speech_recognition.UnknownValueError": {
        "en": "Speech cannot be analyzed and/or recognized!",
        "sr": "Ваш говор не може бити обрађен или препознат!"
    },
    "speech_recognition.RequestError": {
        "en": "Request error problem. Check API limits and connectivity status!",
        "sr": "Проблеми са слањем захтева. Проверите АПИ лимите и статус мреже!"
    },
    # TODO: handle when error occurs in speaking module - how to inform user
    "gtts.tts.gTTSError": {
        "en": "I have a problem with speaking. Probably you reached out the API limit!",
        "sr": "Imam problem sa govorom. Verovatno si probio API limit!"
    },
    "pyowm.exceptions.api_response_error.NotFoundError":{
        "en": "Weather forecast cannot be estimated. I cannot find that location!",
        "sr": "Ne mogu da procenim vremensku prognozu. Ne mogu da pronađem tu lokaciju!"
    },
    "smtplib.SMTPAuthenticationError":
        {
            "en": "There is some problem with email authentication. Check your email credentials.",
            "sr": "Došlo je do problema sa autentifikacijom email naloga. Proveri kredencijale."
        },
    "smtplib.SMTPNotSupportedError": {
        "en": "There is some problem with email settings configuration.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila."
    },
    "smtplib.SMTPHeloError": {
        "en": "There is some problem with email settings configuration.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila."
    },
    "smtplib.SMTPDataError": {
        "en": "There is some problem with email settings configuration.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila."
    },
    "smtplib.SMTPConnectError": {
        "en": "There is some problem with email connection.",
        "sr": "Postoje određeni problemi sa konekcijom ka emaila serveru."
    },
    "smtplib.SMTPServerDisconnected": {
        "en": "There is some problem with email connection.",
        "sr": "Postoje određeni problemi sa konekcijom ka emaila serveru."
    },

    "smtplib.SMTPSenderRefused": {
        "en": "Sender's email settings are not valid.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila pošiljaoca."
    },
    "smtplib.SMTPRecipientsRefused": {
        "en": "Recipient's email settings are not valid. Check recipient email address.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila primaoca. Proveri da li si uneo validnu adresu."
    },
    "wikipedia.exceptions.PageError": {
        "en": "I cannot find anything on Wikipedia that suits your query. Try another one or try again with more precise"
              "speech.",
        "sr": "Nisam uspeo da nađem ništa na Vikipediji što odgovara tvom zahtevu. Probaj sa nekim drugim zahtevom ili probaj"
              "ponovo, ali probaj da budeš precizniji u govoru."
    },
    "exceptions.exceptions.GoogleSearchException": {
        "en": "Google search cannot find anything that suits your query.",
        "sr": "Gugl pretraga nije našla ništa što odgovara tvom upitu."
    },
    "exceptions.exceptions.VoiceAssistantException": {
        "en": "Fatal error. Application could not proceed.",
        "sr": "Došlo je do fatalne interne greške. Aplikacija ne može nastaviti sa radom."
    },
    "exception": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
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
# hr stands for croatian _language beacuse OWM API doesn't support serbian, so instead of serbian (sr),
# croatian _language is used (hr)

WEATHER_PARAMETERS = {
    "clouds": ("clouds", "alias", {"en": "clouds", "hr": "oblačnost"}),
    "pressure": ("press", "child", {"en": "pressure", "hr": "pritisak"}),
    "wind": ("speed", "child", {"en": "wind speed", "hr": "brzina vetra"}),
    # "snow":("snow", "child", ),
    "humidity": ("humidity", "alias", {"en": "humidity", "hr": "vlažnost vazduha"}),
    "temperature_min": ("temp_min", "child", {"en": "minimum temperature", "hr": "minimalna dnevna temperatura"}),
    "temperature_max": ("temp_max", "child", {"en": "maximum temperature", "hr": "maksimalna dnevna temperatura"}),
    "temperature": ("temp", "child", {"en": "temperature", "hr": "prosečna dnevna temperatura"}),
    "detailed_status": ("detailed_status", "alias", {"en": "detailed status", "hr": "detaljniji opis"}),
    "reference_time": ("reference_time", "alias", {"en": "reference time", "hr": "trenutak merenja"})
    # "rain":{}

}

# social networks urls

FACEBOOK_BASE_URL = "https://www.facebook.com/"
TWITTER_BASE_URL = "https://twitter.com/"
INSTAGRAM_BASE_URL = "https://instagram.com/"
LINKEDIN_BASE_URL = "https://www.linkedin.com/in/"

SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 9600
