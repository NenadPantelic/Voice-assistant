from exceptions.exception_handler import ExceptionHandler

from config.constants import LANG_CODES, LANGUAGES_IN_SERBIAN, SUCCESS, FAIL, logger, FATAL
from services.common.action_result import ActionResult
from utils.utils import load_json_data, convert_latin_to_cyrillic, get_language_code

LANGUAGES = load_json_data(LANG_CODES)
SR_LANGUAGES = load_json_data(LANGUAGES_IN_SERBIAN)


class Controller:
    def __init__(self, recognizer, speaker, commandResolver, executor):
        self.recognizer = recognizer
        self.speaker = speaker
        self.command_resolver = commandResolver
        self.executor = executor
        self.language = "en"
        self.speaking_language = "en"

    def set_language(self, language_list):
        # assert (isinstance(language_list, str))
        try:
            lang_code = get_language_code(language_list)
            logger.debug("Operating language = {}.".format(lang_code))
            if lang_code is None:
                raise KeyError
            self.language = lang_code
            self.speaking_language = lang_code
            self.recognizer.set_language(lang_code)
            self.speaker.set_language(lang_code)
            self.executor.set_services_language(lang_code)
            self.command_resolver.set_language(lang_code)
            self.command_resolver.set_processor_language(lang_code)
        except KeyError:
            raise ValueError("Language is not supported. Use English or Serbian.")

    def set_translation_language(self, language):
        assert (isinstance(language, str))
        if self.language == "sr":
            language = SR_LANGUAGES.get(convert_latin_to_cyrillic(language), "english")
        language = LANGUAGES.get(language, "en")
        self.recognizer.set_language(language)
        self.executor.set_param_and_commit("translation", "translate_text", "src_language",
                                           language, input_type="str",
                                           need_input=False, input_processing_method=None,
                                           is_ready=False)

    def reset_recognizer_language(self):
        if self.recognizer.get_language() != self.language:
            self.recognizer.set_language(self.language)

    def set_speaking_language(self, language):
        if language not in (None, self.language):
            self.speaker.set_language(language)
        # self.speaker.set_language(language)

    def reset_speaking_language_(self):
        self.speaker.set_language(self.language)

    def initialize(self):
        message_prefix, command_output_message = self.execute(None)
        self.speaker.save_speech_and_play(message_prefix + command_output_message)

    def finalize(self):
        final_command = self.command_resolver.find_command_by_tag("final")
        command_output_message = final_command["messages"]["success"][self.language]
        self.speaker.save_speech_and_play(command_output_message)
        exit(1)

    def raise_invalid_command(self):
        # invalid_command = self.command_resolver.
        pass

    def listen(self, init=False):
        return self.recognizer.recognize_from_microphone()

    def get_output_speech(self, command_result, messages={}):

        output_message, status, message_prefix = "", SUCCESS, ""
        if command_result is not None:
            output_message = command_result.get_result()
            status = command_result.get_status()
        if messages != {}:
            message_prefix = messages["success"][self.language] if status == SUCCESS else \
                messages["fail"][self.language]
        # output_message, exception_message = self.get_command_output_text(command_result)
        # message_prefix = message if exception_message is None else exception_message
        return message_prefix, output_message

    def determine_next_command(self, command, command_result):
        next_command_id = None
        if command_result is not None:
            if command_result.get_status() == SUCCESS:
                next_command_id = command["next_command_id"]
                # self.command_resolver.set_next_command_id(command["next_command_id"])
            elif command_result.get_status() == FAIL:
                # pass
                # TODO:
                # repeat command or break
                next_command_id = command["command_id"]
            # elif command_result.get_status() == FATAL:
            # exit(1)
            else:
                raise ValueError("Status can only be SUCCESS or FAIL")
        else:
            # case when command is not ready (executable)
            next_command_id = command["next_command_id"]
        self.command_resolver.set_next_command_id(next_command_id)

    def execute_controller_method(self, service, method, command):
        executor = getattr(self, method)
        try:
            if command["has_args"]:
                command_result = eval('executor(' + command["arg_name"] + "=" + "'" + str(command["arg"]) + "')")
            else:
                command_result = executor()
        except Exception as e:
            language = self.language if self.language is not None else "en"
            message = ExceptionHandler.get_exception_message(e, language)
            command_result = ActionResult(message, FAIL, language)
        return command_result

    # this method should be called only once per voice control request
    def execute(self, text):
        command = self.command_resolver.get_command(text)
        speaking_language = None
        service = command["service"]
        method = command["method"]
        # service is none for setup commands
        if service is None:
            # NOTE:if method is None - initial speaking, else language setting
            service = self
            # TODO: map language name to language code - check
        if method is not None:
            if service is self:
                command_result = self.execute_controller_method(service, method, command)
            else:
                command_result = self.executor.set_param_and_commit(command["service"], method, command["arg_name"],
                                                                    command["arg"], input_type=command["arg_type"],
                                                                    need_input=command["need_input"],
                                                                    input_processing_method=command[
                                                                        "input_processing_method"],
                                                                    is_ready=command["is_ready"])
        else:
            command_result = None

        self.determine_next_command(command, command_result)
        messages = command["messages"]  # [self.language]

        if command_result is not None:
            speaking_language = command_result.get_language() if command_result.get_language() is not None \
                else self.language
        self.speaking_language = speaking_language

        return self.get_output_speech(command_result, messages)

    # TODO:check gTTS Google text-to-speech API limit
    def speak_out(self, message_prefix, output_message):
        self.speaker.save_speech_and_play(message_prefix)
        self.set_speaking_language(self.speaking_language)
        self.speaker.save_speech_and_play(output_message)
        self.reset_speaking_language_()

    def listen_and_execute(self):
        try:
            text_result = self.recognizer.recognize_from_microphone()
        except Exception as e:
            message = ExceptionHandler.get_exception_message(e, self.language)
            text_result = ActionResult(message, FAIL)
        self.reset_recognizer_language()
        # _tts exception

        if text_result is None or text_result.get_result() is None or text_result.get_status() == FAIL:
            output = self.get_output_speech(text_result)
            # speaking_language = self.language
        else:
            print(text_result.get_result())
            output = self.execute(text_result.get_result())
        self.speak_out(message_prefix=output[0], output_message=output[1])
