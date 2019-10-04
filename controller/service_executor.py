from config.config import COMMANDS, logger, FAIL, FATAL
from exceptions.exception_handler import ExceptionHandler
from exceptions.exceptions import VoiceAssistantException
from services.common.action_result import ActionResult
from utils.utils import load_json_data
from utils import data_extraction

commands = load_json_data(COMMANDS)


class ServiceExecutor:
    def __init__(self, service_pool={}):
        """
        service_command_methods - dictionary that contains all exec methods for service - key:service_alias,
        value:dictionary with the following structure - key: service method, value:dictionary of service method
        arguments e.g.mailing:{send_email:{recipient : None, subject :None, content:None}}
        :param service_pool: cache of services objects
        """

        self._service_command_methods = {}
        self._populate_service_command_methods()
        self._service_pool = service_pool
        self._language = None
        print(self._service_command_methods)

    def set_services_language(self, language):
        """
        Sets the _language to all services.
        :param (str or None) language: _language code
        :rtype: None
        :return: void method
        """
        assert (language is None or isinstance(language, str))
        self._language = language
        for service in self._service_pool.values():
            if hasattr(service, "set_language"):
                service.set_language(language)

    def set_param_and_commit(self, service, method_name, arg_name, arg_value, need_input=False, input_type="str",
                             input_processing_method=None,
                             is_ready=False):
        """
        Sets parameter value in service_methods_commands and commit if method is executable.
        :param str service: alias name of the service
        :param str method_name: name of the target method
        :param str arg_name: argument name
        :param str arg_value: argument value
        :param bool need_input: needs input from keyboard or not
        :param str input_type: str value of any type_ (`float`, `str`, `int`, `bool` ...)
        :param str input_processing_method: name of the function that should preprocess [arg_value]
        :param bool is_ready: only ready methods are committed
        :rtype: output type_ of [_commit] method or None
        :return:
        """
        self._set_param(service, method_name, arg_name, arg_value, input_type, input_processing_method, need_input)
        if is_ready:
            return self._commit(service, method_name)

    # private methods
    # TODO: optimize arg list with kwargs or locals() (NOTE: this way is cleaner)
    def _set_param(self, service, method_name, arg_name, arg_value, input_type, input_processing_method,
                   need_input=False):
        """
        Sets parameter value in service_methods_commands
        :param str service: alias name of the service
        :param str method_name: name of the target method
        :param str arg_name: argument name
        :param str arg_value: argument value
        :param bool need_input: needs input from keyboard or not
        :param str input_type: str value of any type_ (`float`, `str`, `int`, `bool` ...)
        :param str input_processing_method: name of the function that should preprocess [arg_value]
        :return:
        """
        if need_input:
            logger.debug("Expecting input...")
            print("Enter your input:")
            arg_value = input()
        logger.debug("Argument before processing: [type_ = {}, value = {}]".format(type(arg_value), arg_value))
        if input_type is not None:
            arg_value = eval(input_type + "('" + arg_value + "')")
        if input_processing_method is not None:
            arg_value = eval("data_extraction." + input_processing_method + "('" + arg_value + "')")
        logger.debug("Argument after processing: [type_ = {}, value = {}]".format(type(arg_value), arg_value))
        self._service_command_methods[service][method_name][arg_name] = arg_value

    def _commit(self, service, method):
        """
        Executes service method with arguments from [service_command_methods] dict. If some error occurs, calls exception
        handler. If service is None, returns ActionResult with fatal status.
        :param str service: service name
        :param str method: method name
        :rtype: ActionResult
        :return: ActionResult with SUCCESS - result of execution as payload, FAIL - customized exception message as
        payload or FATAL - blank message result.
        """
        logger.info("-------- begin commit --------")
        service_inst = self._service_pool.get(service, None)
        command_result = None
        if service_inst is not None:
            if hasattr(service_inst, method):
                executor = getattr(service_inst, method)
                try:
                    result = executor(**self._service_command_methods[service][method])
                    logger.debug("Output = {}".format(result))
                    command_result = result

                    # TODO:handle fatal exception
                except Exception as e:
                    message = ExceptionHandler.get_exception_message(e, self._language)
                    command_result = ActionResult(message, FAIL, self._language)
                finally:
                    logger.info("-------- end commit --------")
                    #self._clear_all_params(service, method)
                    return command_result
        else:
            logger.error("Fatal, service cannot be found.")
            message = ExceptionHandler.get_exception_message(VoiceAssistantException, self._language)
            #self._clear_all_params(service, method)
            return ActionResult(message, FATAL)

    def _populate_service_command_methods(self):
        """
        Populating service commands methods dictionary.
        :rtype: None
        :return: void method
        """
        logger.debug("Populating service command methods....")
        if self._service_command_methods != {}:
            return
        for command in commands:
            service = command["service"]
            method = command["method"]
            arg_name = command["arg_name"]
            if service is not None:
                if service not in self._service_command_methods:
                    method_dict = {method: {} if arg_name is None else {arg_name: None}}
                    self._service_command_methods[service] = method_dict
                else:
                    if arg_name is not None:
                        if method in self._service_command_methods[service]:
                            self._service_command_methods[service][method][arg_name] = None
                        else:
                            self._service_command_methods[service][method] = {arg_name: None}

    def _clear_all_params(self, service, method):
        """
        Clears all the data for service-method.
        :param str service: service name
        :param str method: method name
        :rtype: None
        :return: void method
        """
        for arg_name in self._service_command_methods[service][method]:
            self._service_command_methods[service][method][arg_name] = None
