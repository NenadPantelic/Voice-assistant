import json
import time
import uuid


def logging_exception(exception):
    print("Exception message: {}".format(exception))


def get_current_timestamp():
    return time.time()


def generate_uuid():
    return str(uuid.uuid4())


# semantic processing
def load_words_dictionaries(language_word_files):
    language_words = {}
    for language in language_word_files:
        with open(language_word_files.get(language, "en")) as f:
            language_words[language] = json.load(f)
    return language_words


def load_json_data(jsonFilePath):
    with open(jsonFilePath) as f:
        data = json.load(f)
    return data


def flatten_dictionary_values(dictionary_values):
    return [element for element in dictionary_values]
