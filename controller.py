from exceptions.exception_handler import ExceptionHandler
import services.websearch.wikipedia_service as ws
import services.webapi.owm_service as owm


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
    def __init__(self, recognizer, speaker, commandResolver, service_pool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.command_resolver = commandResolver
        self.service_pool = service_pool
        self.language = "en"

    def set_language(self, language_list):
        assert isinstance(language_list, list)
        lang_code = get_language_code(language_list)
        self.language = lang_code
        self.recognizer.set_language(lang_code)
        self.speaker.set_language(lang_code)
        for service in self.service_pool.values():
            service.set_language(lang_code)
        self.command_resolver.set_language(lang_code)
        self.command_resolver.set_processor_language(lang_code)

    def initialize(self):
        self.speaker.save_speech_and_play(self.execute(None))

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
        return message_prefix + output_message

    # this method should be called only once per voice control request
    def execute(self, text):
        command = self.command_resolver.get_command(text)
        command_result = None
        service = self.service_pool.get(command["service"], None)
        method = command["method"]
        # service is none for setup commands
        if service is None:
            # NOTE:if method is None - initial speaking, else language setting
            service = self
            # TODO: map language name to language code - check
        if method is not None:
            executor = getattr(service, method)
            if command["has_args"]:
                command_result = executor(command["arg"])
            else:
                command_result = executor()
        else:
            command_result = None
        message = command["messages"][self.language]
        return self.get_output_speech(command_result, message)

    def listen_and_execute(self, init=False):
        text_result = self.recognizer.recognize_from_microphone()
        # tts exception
        if text_result is None or text_result.get_result() is None:
            output = self.get_output_speech(text_result, '')
        else:
            output = self.execute(text_result.get_result())
        #TODO:check gTTS Google text-to-speech API limit
        self.speaker.save_speech_and_play(output)
