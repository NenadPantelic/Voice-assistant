from config.constants import LANG_KEYWORDS, logger
from exceptions.exceptions import VoiceAssistantException
from utils.utils import load_json_data, convert_commands_json_array_to_dict


class CommandResolver:

    def __init__(self, text_processor, commands, language="en"):
        self._text_processor = text_processor
        self._language = None
        self._keywords = None
        self._commands = convert_commands_json_array_to_dict(commands)
        self._command = None
        self._next_command_id = None
        self.set_language(language)

    def set_language(self, language):
        assert (isinstance(language, str))
        # try:
        logger.debug("Command resolver language = {}.".format(language))
        self._language = language
        keywords = load_json_data(LANG_KEYWORDS[language])
        self.set_keywords(keywords)
        # except KeyError:
        #    raise ValueError("Language is not supported. Use English or Serbian.")

    def set_processor_language(self, language):
        assert (isinstance(language, str))
        self._text_processor.set_language(language)

    def set_keywords(self, keywords):
        assert (isinstance(keywords, list))
        self._keywords = convert_commands_json_array_to_dict(keywords)

    def set_next_command_id(self, command_id):
        assert (isinstance(command_id, str))
        self._next_command_id = command_id

    def calculate_command_scores(self, word_list):
        assert (isinstance(word_list, list))
        scores = {}
        for command_id, command in self._keywords.items():
            words = command["words"]
            scores[command_id] = sum([words.get(word, 0) * word_list.count(word) \
                                      for word in words if word in word_list])
        return scores

    def get_command(self, text):
        assert (text is None or isinstance(text, str))
        init = True
        word_list = []
        if text is not None:
            word_list = self._text_processor.preprocess_text(text)
            init = False

        self.determine_command(init, word_list)
        target_command = self._command
        if target_command["has_args"]:
            arg = ' '.join(word_list)
            if target_command["process_input_text"]:
                arg = self._text_processor.filter_out_keywords(word_list,
                                                               self._keywords[self._command["command_id"]][
                                                                   "words"].keys())
            target_command.update({"arg": arg})
        logger.debug("Command for execution = {}".format(target_command))
        return target_command

    def determine_command(self, init=False, word_list=[]):
        assert (isinstance(init, bool) and isinstance(word_list, list))
        if init:
            self._command = self.find_command_by_tag("initial")
        elif self._next_command_id is None:
            score_map = self.calculate_command_scores(word_list)
            max_score = max(score_map.values())
            candidate_commands = list(filter(lambda x: x[1] == max_score, score_map.items()))
            if len(candidate_commands) > 1:
                self._command = self.find_command_by_tag("ambiguous")
            else:
                self._command = self._commands[candidate_commands[0][0]]
        else:
            self._command = self.find_command_by_id(self._next_command_id)

        if self._command is None:
            self._command = self.find_command_by_tag("invalid")

        self._next_command_id = self._command["next_command_id"]
        logger.debug("Next command's id = {}".format(self._next_command_id))

    def find_command_by_tag(self, tag):
        # currently there is only one command by tag, in future, if there is more than one command per tag, use command
        # id as identifier
        # return first one
        try:
            return list(filter(lambda x: x["tag"] == tag, self._commands.values()))[0]
        except IndexError:
            raise VoiceAssistantException("Command with the given tag = {} cannot be found. Check commands tag.".
                                          format(tag))

    def get_command_keywords(self, commandId):
        words = [command["words"] for command in self._keywords if command["command_id"] == commandId]
        return words[0] if len(words) == 1 else None

    def find_command_by_id(self, commandId):
        return self._commands.get(commandId, None)
