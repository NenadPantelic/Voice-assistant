# - *- coding: utf- 8 - *-

import logging
import os


LOG_FILE = "voice_assistant.log"
logging.basicConfig(level=logging.DEBUG, filename="voice_assistant.log",
                    format='%(asctime)s: %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging

# logging  - debug, info, warning, error, critical

PROVIDED_LANGUAGES = {
    "english": "en-US",
    "serbian": "sr-RS",
    "default": "en-US"
}

LANGUAGES_IN_SERBIAN = os.path.abspath("data/languages/langs_in_serbian.json")
LANG_CODES = "data/languages/langs_codes.json"
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

# messages
CALL_MESSAGE = {"en": "I'm ready for a new command", "sr": "Spreman sam za novu komandu."}

# commands
COMMANDS = "data/commands/commands.json"
# TODO: refactor path variables to be in dictionary form for simpler usage

# action result statuses
SUCCESS = 1
FAIL = 0
FATAL = -1

# exception messages
GENERIC_MESSAGE_EN = "Some internal error occurred. Check the log for more details!"
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
        "en": "Speech cannot be analyzed or recognized!",
        "sr": "Vaš govor ne može biti obrađen ili prepoznat!"
    },
    "speech_recognition.RequestError": {
        "en": "Request error problem. Check API limits and connectivity status!",
        "sr": "Problemi sa slanjem zahteva. Proverite API limit i status mreže!"
    },
    # TODO: handle when error occurs in speaking module - how to inform user
    "gtts.tts.gTTSError": {
        "en": "I have a problem with speaking. Probably you reached out the API limit!",
        "sr": "Imam problem sa govorom. Verovatno si probio API limit!"
    },
    "pyowm.exceptions.api_response_error.NotFoundError": {
        "en": "The weather forecast cannot be estimated. I cannot find that location!",
        "sr": "Ne mogu da procenim vremensku prognozu. Ne mogu da pronađem tu lokaciju!"
    },
    "pyowm.exceptions.api_call_error.APICallError": {
        "en": "The weather forecast cannot be estimated. I cannot find that location!",
        "sr": "Ne mogu da procenim vremensku prognozu. Ne mogu da pronađem tu lokaciju!"
    },
    "smtplib.SMTPAuthenticationError":
        {
            "en": "There is some problem with email authentication. Check your email address credentials.",
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
        "en": "There is some problem with an email connection.",
        "sr": "Postoje određeni problemi sa konekcijom ka emaila serveru."
    },
    "smtplib.SMTPServerDisconnected": {
        "en": "There is some problem with an email connection.",
        "sr": "Postoje određeni problemi sa konekcijom ka emaila serveru."
    },

    "smtplib.SMTPSenderRefused": {
        "en": "Sender's email settings are not valid.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila pošiljaoca."
    },
    "smtplib.SMTPRecipientsRefused": {
        "en": "Recipient's email settings are not valid. Check the recipient's email address.",
        "sr": "Postoje određeni problemi sa podešavanjima emaila primaoca. Proveri da li si uneo validnu adresu."
    },
    "wikipedia.exceptions.PageError": {
        "en": "I cannot find anything on Wikipedia that suits your query. Try another one or try again with more precise"
              " speech.",
        "sr": "Nisam uspeo da nađem ništa na Vikipediji što odgovara tvom zahtevu. Probaj sa nekim drugim zahtevom ili probaj"
              "ponovo, ali probaj da budeš precizniji u govoru."
    },
    "exceptions.exceptions.GoogleSearchException": {
        "en": "Google search cannot find anything that suits your query.",
        "sr": "Gugl pretraga nije našla ništa što odgovara tvom upitu."
    },
    "exceptions.exceptions.VoiceAssistantException": {
        "en": "Fatal error. The application could not proceed.",
        "sr": "Došlo je do fatalne interne greške. Aplikacija ne može nastaviti sa radom."
    },
    "exception": {
        "en": GENERIC_MESSAGE_EN,
        "sr": GENERIC_MESSAGE_SR
    }
}

# credentials
OWM_API_KEY = "5ab8013f8b3c54d28b8f8035ffd40f0a"
OMDB_API_KEY = "56674ea0"

PROXY_MAIL = "lindo.voice.assistant@gmail.com"
MAIL_PASSWORD = "mizcechlykbgsfhx"

# weather params
# NOTE: only some of params are included (most important ones)
WEATHER_PARAMS = {"clouds", "detailed_status", "dewpoint", "heat_index", "humidex", "humidity", "pressure", "rain",
                  "reference_time", "snow", "status", "sunrise_time", "sunset_time", "temperature",
                  "visibility_distance", "weather_code", "weather_icon_name", "weather_icon_url", "wind"}

# format <name in json response>: (json_subvalue or alias, child/alias, display name)
# hr stands for croatian _language because OWM API doesn't support serbian, so instead of serbian (sr),
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

# serial communication params
SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 9600
