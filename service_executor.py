from config.constants import ENGLISH_COMMANDS, SUCCESS, logger, FAIL
from exceptions.exception_handler import ExceptionHandler
from services.action_result import ActionResult
from utils.utils import load_json_data
from utils import data_conversion
commands = load_json_data(ENGLISH_COMMANDS)


class ServiceExecutor:
    def __init__(self, service_pool={}):
        # dictionary that contains all exec methods for service - key:service_alias, value:dictionary with the following
        # structure - key: service method, value:dictionary of service method arguments e.g.
        # mailing:{send_email:{recipient : None, subject :None, content:None}}
        self.__service_command_methods = {}
        self.__populate_service_command_methods()
        self.service_pool = service_pool
        #TODO;check if this should be set in constructor
        self.__language = None

    def set_services_language(self, language):
        self.__language = language
        for service in self.service_pool.values():
            if hasattr(service, "set_language"):
                service.set_language(language)

    def set_translator_src_language(self, language):
        if "translation" in self.service_pool:
            self.service_pool['translation'].set_src_language(language)

    def set_param_and_commit(self, service, method_name, arg_name, arg_value, need_input=False, input_type="str",
                             input_processing_method = None,
                             is_ready=False):
        self.__set_param(service, method_name, arg_name, arg_value, input_type, input_processing_method,need_input)
        if is_ready:
            return self.__commit(service, method_name)

    # super private methods
    def __set_param(self, service, method_name, arg_name, arg_value, input_type, input_processing_method, need_input=False):
        if need_input:
            print("Enter your input:")
            arg_value = input()
        if input_type is not None:
            arg_value = eval(input_type + "('" + arg_value + "')")
        print(arg_value)
        if input_processing_method is not None:
            arg_value = eval("data_conversion." + input_processing_method + "('" + arg_value +"')")
        print(arg_value, type(arg_value))
        self.__service_command_methods[service][method_name][arg_name] = arg_value

    def __commit(self, service, method):
        logger.info("-------- begin commit --------")
        service_inst = self.service_pool.get(service, None)
        command_result = None
        if service_inst is not None:
            if hasattr(service_inst, method):
                executor = getattr(service_inst, method)
                try:
                    result = executor(**self.__service_command_methods[service][method])
                    print(result.get_result())
                    command_result = result
                except Exception as e:
                    message = ExceptionHandler.get_exception_message(e, self.__language)
                    command_result = ActionResult(message, FAIL, self.__language)
                finally:
                    logger.info("-------- end commit --------")
                    return command_result
        else:
            pass
        #logger.info("-------- end commit --------")

        # TODO:exception handling

    def __populate_service_command_methods(self):
        if self.__service_command_methods != {}:
            return
        for command in commands:
            service = command["service"]
            method = command["method"]
            arg_name = command["arg_name"]
            if service is not None:
                if service not in self.__service_command_methods:
                    method_dict = {method: {} if arg_name is None else {arg_name: None}}
                    self.__service_command_methods[service] = method_dict
                else:
                    if arg_name is not None:
                        if method in self.__service_command_methods[service]:
                            self.__service_command_methods[service][method][arg_name] = None
                        else:
                            self.__service_command_methods[service][method] = {arg_name: None}
