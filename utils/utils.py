import json
import time
import uuid


def logging_exception(exception):
    print("Exception message: {}".format(exception))


def get_current_timestamp():
    return time.time()


def generate_uuid():
    return str(uuid.uuid4())


# data load
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


def convert_commands_json_array_to_dict(json_array):
    resulting_map = {}
    for element in json_array:
        resulting_map[element["command_id"]] = element
    return resulting_map


# letters conversion
def convert_or_return_text(text, language):
    return convert_latin_to_cyrillic(text) if language == "sr" else text


def convert_latin_to_cyrillic(text):
    latin_symbols = ['a', 'b', 'v', 'g', 'd', 'đ', 'e', 'ž', 'z', 'i', 'j', 'k', 'l', 'ǉ', 'm', 'n', 'ǌ', 'o', \
                     'p', 'r', 's', 't', 'ć', 'u', 'f', 'h', 'c', 'č', 'dž', 'š']
    cyrillic_symbols = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п',
                        'р', 'с', 'т', 'ћ', 'у', \
                        'ф', 'х', 'ц', 'ч', 'џ', 'ш']
    converted_text = ""
    conversion_map = {latin_symbols[i]: cyrillic_symbols[i] for i in range(len(latin_symbols))}
    for char in text:
        converted_text = converted_text + (conversion_map[char] if char.isalpha() else char)
    return converted_text


def convert_instance_type_to_str(type):
    return str(type).split("'")[1]
