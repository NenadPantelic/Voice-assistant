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


def flatten_lists(jagged_array):
    flattened_list = []
    for element in jagged_array:
        flattened_list.extend(element)
    return flattened_list


def convert_list_to_str(list_to_convert):
    return ' '.join(list_to_convert)
