import json
import time
import uuid
from playsound import playsound


def play_audio(file_name):
    """
    Play audio file.
    :param str file_name: name of file that will be played.
    :rtype: None
    :return: void method
    """
    assert (isinstance(file_name, str))
    playsound(file_name)


def get_language_code(language_str):
    """
    Determines language code based on words in str_list. Strongly coupled with the english-serbian languages use-case
    :param language_str:
    :rtype: None or str
    :return: language code (`en`, `sr`) or None
    """
    assert (isinstance(language_str, str))
    if any(option in language_str for option in ("english", "default", "engleski", "podrazumevan")):
        lang_choice = "en"  # "en-US"
    elif any(option in language_str for option in ("serbian", "srpski")):
        lang_choice = "sr"
    else:
        lang_choice = None
    return lang_choice


def get_current_timestamp():
    """
    Returns current timestamp as str.
    :rtype: str
    :return: current timestamp (Return the current time in seconds since the Epoch)
    """
    return time.time()


def generate_uuid():
    """
    Generates random uuid (16 bytes). Used to generate commands id.
    :rtype: str
    :return: str uuid
    """
    return str(uuid.uuid4())


# data load
def load_words_dictionaries(language_word_files):
    """
    Loads json files in dictionary. Dictionary keys are language codes and values are list of dictionaries (json).
    :param tuple, list, set or dictionary language_word_files: contains language codes
    :rtype: dictionary
    :return: Returns dictionary where keys are language codes and values are list of dictionaries (json)
    """
    assert (any(isinstance(language_word_files, type_) for type_ in (tuple, list, set, dict)))
    language_words = {}
    for language in language_word_files:
        with open(language_word_files.get(language, "en")) as f:
            language_words[language] = json.load(f)
    return language_words


def load_json_data(json_file_path):
    """
    Loads json file.
    :param str json_file_path: path of json file that will be loaded
    :rtype: list
    :return: list of json (dictionary) objects
    """
    assert (isinstance(json_file_path, str))
    with open(json_file_path) as f:
        data = json.load(f)
    return data


def flatten_lists(jagged_list):
    """
    Convert list (or tuple) of lists to flattend list
    :param list, tuple or dict_keys or dict_values of lists jagged_list: list of lists that needs to be flattened.
    :rtype: list
    :return: flattened list
    """
    flattened_list = []
    for element in jagged_list:
        flattened_list.extend(element)
    return flattened_list


def convert_commands_json_array_to_dict(json_array):
    """
    Convert json list of commands to dictionary.
    :param list of dictionaries json_array: list of commands (dictionary)
    :rtype: dict
    :return:dictionary where key is command_id and values is command itself
    """
    resulting_map = {}
    for element in json_array:
        resulting_map[element["command_id"]] = element
    return resulting_map


# letters conversion
def convert_latin_to_cyrillic(text):
    """
    Converts text to cyrillic.
    :param text:  input text in latin
    :rtype: str
    :return: converted text
    """
    assert (isinstance(text, str))
    latin_symbols = ['a', 'b', 'v', 'g', 'd', 'đ', 'e', 'ž', 'z', 'i', 'j', 'k', 'l', 'ǉ', 'm', 'n', 'ǌ', 'o', 'p',
                     'r', 's', 't', 'ć', 'u', 'f', 'h', 'c', 'č', 'dž', 'š']
    cyrillic_symbols = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п',
                        'р', 'с', 'т', 'ћ', 'у',
                        'ф', 'х', 'ц', 'ч', 'џ', 'ш']
    converted_text = ""
    conversion_map = {latin_symbols[i]: cyrillic_symbols[i] for i in range(len(latin_symbols))}
    for char in text:
        converted_text = converted_text + (conversion_map[char] if char.isalpha() else char)
    return converted_text


def convert_instance_type_to_str(type_):
    """
    Returns type name (without any other str elements)
    :param type_: Type name in form <class '<type_name>'>
    :rtype: str
    :return: type name
    """
    assert (isinstance(type_, str))
    return str(type_).split("'")[1]
