from exceptions.exception_handler import ExceptionHandler
from config.constants import LANG_CODES, LANGUAGES_IN_SERBIAN, SUCCESS, FAIL, logger, FATAL, PATH_TO_AUDIO_DIR
from services.common.action_result import ActionResult
from utils.utils import load_json_data, convert_latin_to_cyrillic, get_language_code, delete_all_mp3_files

LANGUAGES = load_json_data(LANG_CODES)
SR_LANGUAGES = load_json_data(LANGUAGES_IN_SERBIAN)


class Controller:
    def __init__(self, recognizer, speaker, command_resolver, executor):
        self._recognizer = recognizer
        self._speaker = speaker
        self._command_resolver = command_resolver
        self._executor = executor
        self._language = "en"
        self._speaking_language = "en"

    # public methods
    def set_language(self, language_str):
        """
        Sets the operating language of the voice assistant (recognizer, speaker, executor, command resolver and services
        ). Raises KeyError/ValueError if invalid language is set.
        :param str language_str: string that contains language name
        :rtype: None
        :return: void method
        """
        assert (isinstance(language_str, str))
        try:
            lang_code = get_language_code(language_str)
            logger.debug("Operating _language = {}.".format(lang_code))
            if lang_code is None:
                raise KeyError
            self._language = lang_code
            self._speaking_language = lang_code
            self._recognizer.set_language(lang_code)
            self._speaker.set_language(lang_code)
            self._executor.set_services_language(lang_code)
            self._command_resolver.set_language(lang_code)
            self._command_resolver.set_processor_language(lang_code)
        except KeyError:
            raise ValueError("Language is not supported. Use English or Serbian.")

    def set_translation_language(self, language):
        """
        Sets the translation language (for recognizer and translation service)
        :param str language: language to be set
        :rtype: None
        :return: void method
        """
        assert (isinstance(language, str))
        if self._language == "sr":
            language = SR_LANGUAGES.get(convert_latin_to_cyrillic(language), "english")
        language = LANGUAGES.get(language, "en")
        self._recognizer.set_language(language)
        self._executor.set_param_and_commit("translation", "translate_text", "src_language",
                                            language, input_type="str",
                                            need_input=False, input_processing_method=None,
                                            is_ready=False)

    def initialize(self):
        message_prefix, command_output_message = self._execute(None)
        self._speaker.save_speech_and_play(message_prefix + command_output_message)

    def finalize(self):
        final_command = self._command_resolver.find_command_by_tag("final")
        command_output_message = final_command["messages"]["success"][self._language]
        self._speaker.save_speech_and_play(command_output_message)
        delete_all_mp3_files(PATH_TO_AUDIO_DIR)
        exit(1)

    def listen_and_execute(self):
        try:
            text_result = self._recognizer.recognize_from_microphone()
        except Exception as e:
            message = ExceptionHandler.get_exception_message(e, self._language)
            text_result = ActionResult(message, FAIL)
        self._reset_recognizer_language()

        if text_result is None or text_result.get_result() is None or text_result.get_status() == FAIL:
            output = self._get_output_speech(text_result)
        else:
            logger.debug("Speech recognition result = {}".format(text_result))
            try:
                output = self._execute(text_result.get_result())
            except Exception as e:
                output = (ExceptionHandler.get_exception_message(e, self._language), '')
        self._speak_out(message_prefix=output[0], output_message=output[1])

    # private methods
    def _reset_recognizer_language(self):
        if self._recognizer.get_language() != self._language:
            self._recognizer.set_language(self._language)

    def _set_speaking_language(self, language):
        if language not in (None, self._language):
            self._speaker.set_language(language)

    def _reset_speaking_language_(self):
        self._speaker.set_language(self._language)

    def _raise_fatal_command(self, command_result):
        output = self._get_output_speech(command_result)
        self._speak_out(message_prefix=output[0], output_message=output[1])
        exit(1)

    def _get_output_speech(self, command_result, messages={}):

        output_message, status, message_prefix = "", SUCCESS, ""
        if command_result is not None:
            output_message = command_result.get_result()
            status = command_result.get_status()
        if messages != {}:
            message_prefix = messages["success"][self._language] if status == SUCCESS else \
                messages["fail"][self._language]
        return message_prefix, output_message

    def _determine_next_command(self, command, command_result):
        next_command_id = None
        if command_result is not None:
            if command_result.get_status() == SUCCESS:
                next_command_id = command["next_command_id"]
            elif command_result.get_status() in (FAIL, FATAL):
                next_command_id = command["command_id"]
            else:
                raise ValueError("Status can only be SUCCESS or FAIL")
        else:
            # case when command is not ready (executable)
            next_command_id = command["next_command_id"]
        self._command_resolver.set_next_command_id(next_command_id)

    def _execute_controller_method(self, service, method, command):
        executor = getattr(self, method)
        try:
            if command["has_args"]:
                command_result = eval('executor(' + command["arg_name"] + "=" + "'" + str(command["arg"]) + "')")
            else:
                command_result = executor()
        except Exception as e:
            language = self._language if self._language is not None else "en"
            message = ExceptionHandler.get_exception_message(e, language)
            command_result = ActionResult(message, FAIL, language)
        return command_result

    # this method should be called only once per voice control request
    def _execute(self, text):
        command = self._command_resolver.get_command(text)
        speaking_language = None
        service = command["service"]
        method = command["method"]
        # service is none for setup commands
        if service is None:
            service = self
        if method is not None:
            if service is self:
                command_result = self._execute_controller_method(service, method, command)
            else:
                command_result = self._executor.set_param_and_commit(command["service"], method, command["arg_name"],
                                                                     command["arg"], input_type=command["arg_type"],
                                                                     need_input=command["need_input"],
                                                                     input_processing_method=command[
                                                                         "input_processing_method"],
                                                                     is_ready=command["is_ready"])
        else:
            command_result = None

        # TODO: this may be refactored to use SESE principle
        if command_result is not None:
            speaking_language = command_result.get_language() if command_result.get_language() is not None \
                else self._language
            if command_result.get_status() == FATAL:
                return self._raise_fatal_command(command_result)

        self._determine_next_command(command, command_result)
        messages = command["messages"]
        self._speaking_language = speaking_language
        return self._get_output_speech(command_result, messages)

    def _speak_out(self, message_prefix, output_message):
        logger.debug("Message prefix = {}".format(message_prefix))
        self._speaker.save_speech_and_play(message_prefix)
        self._set_speaking_language(self._speaking_language)
        logger.debug("Output message = {}".format(output_message))
        self._speaker.save_speech_and_play(output_message)
        self._reset_speaking_language_()
