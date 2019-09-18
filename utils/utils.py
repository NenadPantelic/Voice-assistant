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

#letters conversion
def convert_or_return_text(text, language):
    return convert_latinic_to_cyrilic(text) if language == "sr" else text

def convert_latinic_to_cyrilic(text):
    latinic_symbols = ['a', 'b', 'v', 'g', 'd', 'đ', 'e', 'ž', 'z', 'i', 'j', 'k', 'l', 'ǉ', 'm', 'n', 'ǌ', 'o',\
                       'p', 'r', 's', 't', 'ć', 'u', 'f', 'h', 'c', 'č', 'dž', 'š']
    cyrilic_symbols = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п',
                       'р', 'с', 'т', 'ћ', 'у', \
                       'ф', 'х', 'ц', 'ч', 'џ', 'ш']
    converted_text = ""
    conversion_map = {latinic_symbols[i]: cyrilic_symbols[i] for i in range(len(latinic_symbols))}
    for char in text:
        converted_text = converted_text + (conversion_map[char] if char.isalpha() else char)
    return converted_text

