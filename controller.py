from exceptions.exception_handler import ExceptionHandler
import services.websearch.wikipedia_service as ws
import services.webapi.owm_service as owm
from config.constants import LANG_CODES, LANGUAGES_IN_SERBIAN
from utils.utils import convert_or_return_text, load_json_data, convert_latinic_to_cyrilic

LANGUAGES = load_json_data(LANG_CODES)
SR_LANGUAGES = load_json_data(LANGUAGES_IN_SERBIAN)


# TODO: add json structure checking
# TODO:check if this can be refactored
def get_language_code(str_list):
    if "english" in str_list or "default" in str_list:
        lang_choice = "en"  # "en-US"
    elif "serbian" in str_list:
        lang_choice = "sr"
    else:
        lang_choice = None
    return lang_choice


class Controller:
    def __init__(self, recognizer, speaker, commandResolver, executor):
        self.recognizer = recognizer
        self.speaker = speaker
        self.command_resolver = commandResolver
        self.executor = executor
        self.language = "en"
        self.speaking_language = "en"

    def set_language(self, language_list):
        # assert isinstance(language_list, list)
        lang_code = get_language_code(language_list)
        self.language = lang_code
        self.speaking_language = lang_code
        self.recognizer.set_language(lang_code)
        self.speaker.set_language(lang_code)
        self.executor.set_services_language(lang_code)
        self.command_resolver.set_language(lang_code)
        self.command_resolver.set_processor_language(lang_code)

    def set_translation_language(self, language):
        assert (isinstance(language, str))
        if self.language == "sr":
            language = SR_LANGUAGES.get(convert_latinic_to_cyrilic(language), "english")
        language = LANGUAGES.get(language, "en")
        self.recognizer.set_language(language)
        self.executor.set_param_and_commit("translation", "translate_text", "src_language",
                                           language, input_type="str",
                                           need_input=False,
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

    def listen(self, init=False):
        return self.recognizer.recognize_from_microphone()

    def get_command_output_text(self, command_result):
        # TODO:add check if output_message and exception_message are nonempty
        exception_message = None
        output_message = ""
        if command_result is not None:
            output_message = "" if command_result.get_result() is None else command_result.get_result()
            exception_message = ExceptionHandler.check_exception_existence(command_result.get_status(), self.language)
        return output_message, exception_message

    def get_output_speech(self, command_result, message):
        output_message, exception_message = self.get_command_output_text(command_result)
        message_prefix = message if exception_message is None else exception_message
        # message_prefix = self.get_message_prefix(message, exception_message)
        return message_prefix, output_message

    def execute_appropriate_method(self, service, method, command):
        executor = getattr(service, method)
        if command["has_args"]:
            command_result = eval('executor(' + command["arg_name"] + "=" + "'" + str(command["arg"]) + "')")
        else:
            command_result = executor()
        return command_result

    # this method should be called only once per voice control request
    def execute(self, text):
        command = self.command_resolver.get_command(text)
        #command_result = None
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
                command_result = self.execute_appropriate_method(service, method, command)
            else:
                command_result = self.executor.set_param_and_commit(command["service"], method, command["arg_name"],
                                                                    command["arg"], input_type=command["arg_type"],
                                                                    need_input=command["need_input"],
                                                                    is_ready=command["is_ready"])
        else:
            command_result = None
        message = command["messages"][self.language]

        if command_result is not None:
            speaking_language = command_result.get_language() if command_result.get_language() is not None \
                else self.language
        self.speaking_language = speaking_language

        return self.get_output_speech(command_result, message)

    # TODO:check gTTS Google text-to-speech API limit
    def speak_out(self, message_prefix, output_message):
        print(message_prefix, output_message)
        self.speaker.save_speech_and_play(message_prefix)
        self.set_speaking_language(self.speaking_language)
        self.speaker.save_speech_and_play(output_message)
        self.reset_speaking_language_()

    def listen_and_execute(self):
        text_result = self.recognizer.recognize_from_microphone()
        self.reset_recognizer_language()
        # tts exception

        if text_result is None or text_result.get_result() is None:
            output = self.get_output_speech(text_result, '')
            # speaking_language = self.language
        else:
            print(text_result.get_result())
            output = self.execute(text_result.get_result())
        self.speak_out(message_prefix=output[0], output_message=output[1])
