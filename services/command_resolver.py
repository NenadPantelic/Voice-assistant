from config.constants import LANG_KEYWORDS
from utils.utils import load_json_data
def convert_json_array_to_dict(json_array):
    resulting_map = {}
    for element in json_array:
        resulting_map[element["command_id"]] = element
    return resulting_map


class CommandResolver:

    def __init__(self, text_processor, commands, language = "en"):
        self.__text_processor = text_processor
        self.__language = None
        self.__keywords = None
        #self.__keywords = convert_json_array_to_dict(language)
        self.__commands = convert_json_array_to_dict(commands)
        self.__command = None
        self.__previous_command_id = None
        self.__next_command_id = None
        self.set_language(language)


    def set_language(self, language):
        self.__language = language
        keywords = load_json_data(LANG_KEYWORDS[language])
        self.set_keywords(keywords)

    def set_processor_language(self, language):
        self.__text_processor.set_language(language)

    def set_keywords(self, keywords):
        self.__keywords = convert_json_array_to_dict(keywords)

    def calculate_command_scores(self, word_list):
        scores = {}
        # TODO:change input type of word_list to string (currently is list)
        #word_list = ' '.join(word_list)
        for command_id, command in self.__keywords.items():
            words = command["words"]
            scores[command_id] = sum([words.get(word, 0) * word_list.count(word) \
                                      for word in words if word in word_list])
        return scores

    # TODO: check what to use - phrases or single words
    def get_command(self, text):
        init = True
        word_list = []
        if text is not None:
            word_list = self.__text_processor.preprocess_text(text)
            init = False

        self.determine_command(init, word_list)
        target_command = self.__command

        if target_command["has_args"]:
            arg = ' '.join(word_list)
            if target_command["process_input_text"]:
                arg = self.__text_processor.filter_out_keywords(word_list, self.__keywords[self.__command["command_id"]][
                    "words"].keys())
            target_command.update({"arg": arg})
        return target_command

    def determine_command(self, init=False, wordList=[]):
        if init:
            self.__command = self.get_default_command()

        elif self.__next_command_id is None:
            score_map = self.calculate_command_scores(wordList)
            max_score = max(score_map.values())
            candidate_commands = list(filter(lambda x: x[1] == max_score, score_map.items()))
            if len(candidate_commands) > 1:
                # TODO:solve scenario when multiple methods have the same score
                self.__command = self.get_most_probable_command(candidate_commands)
            else:
                self.__command = self.__commands[candidate_commands[0][0]]
            self.__previous_command_id = self.__command["previous_command_id"]
        else:
            self.__previous_command_id = self.__command["command_id"]
            self.__command = self.find_command_by_id(self.__next_command_id)

        self.__next_command_id = self.__command["next_command_id"]

    def get_most_probable_command(self, commands):
        pass

    def get_default_command(self):
        # one command with no service and method should be set
        return list(filter(lambda x: x["service"] is None and x["method"] is None, self.__commands.values()))[0]

    # helper method
    def get_command_keywords(self, commandId):
        words = [command["words"] for command in self.__keywords if command["command_id"] == commandId]
        return words[0] if len(words) == 1 else None

    def find_command_by_id(self, commandId):
        return self.__commands.get(commandId, None)
