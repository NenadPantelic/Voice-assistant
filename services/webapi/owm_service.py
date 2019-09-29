from datetime import datetime

from pyowm import OWM
from functools import lru_cache
from config.constants import OWM_API_KEY, WEATHER_PARAMS, WEATHER_PARAMETERS, SUCCESS, logger
from services.common.action_result import ActionResult


class WeatherForecastService:

    def __init__(self, language="en"):
        self._api = OWM(OWM_API_KEY, language=language)

    def set_language(self, language):
        """
        Sets _language for OWM API.
        :param language : _language code (str) e.g. en, fr, sr...
        :return:
        """
        logger.debug("Setting owm _language: {}".format(language))
        language = 'hr' if language == 'sr' else language
        self._api.set_language(language)

    # region public methods
    def get_forecast_result(self, location, param="all", unit="celsius"):
        """
        Returns weather forecast for location.
        :param location: location (str) - location which forecast we seek
        :param param: param (str); default = all - which weather parameter we want
        :param unit: unit(str); default = celsius - unit for temperature measurement, expected values are celsius,
        fahrenheit and kelvin
        :return: weather forecast in string format weather_param:value
        covered params:clouds, pressure, wind speed (mph), humidity, minimum temperature, maximum temperature,temperature
        detailed status
        """
        logger.debug(
            "Calling get_forecast_result with params: [location = {}, param = {}, unit = {}]".format(str(location), \
                                                                                                     str(param),
                                                                                                     str(unit)))
        weather_data = self._get_weather_at_location(location)
        logger.debug("Weather data results were fetched....")
        logger.debug("Raw forecast results = {}".format(str(weather_data)))
        forecast_output = self._get_forecast_in_readable_form(weather_data, param, **{"unit": unit})
        logger.debug("Forecast in readable form:\n{}".format(forecast_output))
        return ActionResult(forecast_output, SUCCESS)

    # region private methods
    @lru_cache(maxsize=8)
    def _get_weather_at_location(self, location, out_format="json"):
        """
        Get raw weather data.
        :param location: location (str) - location which forecast we seek
        :param out_format: output format (str) - (json, xml)
        :return: returns observation object (pyowm.weatherapi25.observation.Observation)
        """
        assert (out_format in ("json", "xml")), "Only json and xml output formats are supported!"
        if type(location) == str:
            target_function = self._api.weather_at_place
        elif type(location) == int:
            target_function = self._api.weather_at_id
        elif type(location) == tuple:
            # NOTE:do not use tuple, currently it is not handled  when lat,long tuple arg is used
            target_function = self._api.weather_at_coords
        else:
            raise TypeError("Location type_ is not valid.")
        weather_data = target_function(location)
        return weather_data.get_weather()

    def _get_forecast_in_readable_form(self, weather_data, param_name, **kwargs):
        """
        Returns weather forecast in for-read user-friendly form.
        :param weather_data (pyowm.weatherapi25.weather.Weather): Weather object
        :param param_name (str): parameter we want e.g. temperature, humidity,....
        metric units: wind (m/s), temperature (celsius), cloudines(%), pressure(mbar), humidity...
        :param kwargs:
        :return: weather data in string format weather_param:value
        """
        forecast = self._get_forecast(weather_data, param_name, **kwargs)
        logger.debug("Complete forecast info: {}".format(forecast))
        display_str = ''
        for param, struct in WEATHER_PARAMETERS.items():
            if param in ("temperature_min", "temperature_max"): param = "temperature"

            if param not in forecast:
                continue
            # NOTE:pressure value is measured in hPa, which is equal to mbar
            weather_param_value = forecast[param]
            if param == "reference_time":
                weather_param_value = datetime.utcfromtimestamp(int(weather_param_value)).strftime('%d-%m-%Y %H:%M:%S')
            child_alias_status = struct[1]
            child_alias_value = struct[0]
            display_name = struct[2][self._api.get_language()]
            value = weather_param_value[child_alias_value] if child_alias_status == "child" else weather_param_value
            display_str += display_name + ": " + str(value) + ",\n"
        return display_str

    def _get_forecast(self, weather_data, param, **kwargs):
        """
        Get  weather parameter dictionary from weather object. If param is `all`, then returns complete weather status,
        with all parameters defined in config file
        :param weather_data (pyowm.weatherapi25.weather.Weather): Weather object
        :param param_name (str): parameter we want e.g. temperature, humidity,....
        :param kwargs:
        :return: dictionary with weather_param:value pairs
        """
        if param == "all":
            weather_param = self._get_all_weather_params(weather_data, **kwargs)
        else:
            weather_param = self._get_weather_param(weather_data, param, **kwargs)
        return weather_param

    def _get_all_weather_params(self, weather_data, **kwargs):
        """
          Returns complete weather status, with all parameters defined in config file.
          :param weather_data (pyowm.weatherapi25.weather.Weather): Weather object
          :return: dictionary with weather_param:value pairs
        """
        weather = {}
        for param in WEATHER_PARAMS:
            weather.update(self._get_weather_param(weather_data, param, **kwargs))
        return weather

    def _get_weather_param(self, weather_data, param, **kwargs):
        """
         Get  weather parameter dictionary from weather object for particular weather param.
         :param weather_data (pyowm.weatherapi25.weather.Weather): Weather object
         :param param_name (str): parameter we want e.g. temperature, humidity,....
         :param kwargs:
         :return: dictionary with weather_param:value pair to follow usage interface in higher level methods
         """
        func_ptr = weather_param = None
        if hasattr(weather_data, 'get_' + param):
            func_ptr = getattr(weather_data, 'get_' + param)
        if func_ptr is not None:
            if param == 'temperature' and kwargs.get('unit', None) is not None:
                unit = kwargs.get('unit', None)
                if unit not in (
                        "celsius", "fahrenheit"):  # imperial = fahrenheit, metric = celsius, kelvin is by default
                    raise ValueError("Only celsius, kelvin and fahrenheit scales are supported")
                weather_param = func_ptr(unit=unit)
            else:
                weather_param = func_ptr()
        return {param: weather_param}

    # for weather prediction - not used at this moment
    def _get_forecast_for_next_x_days(self, location, days_limit):
        forecast = self._api.daily_forecast(location, limit=days_limit)
        return forecast  # _get_forecast and get_weather_at
