from pyowm import OWM
from pyowm.caches.lrucache import LRUCache

from config.constants import OWM_API_KEY, WEATHER_PARAMS, WEATHER_PARAMETERS, OK
from ..action_result import ActionResult


class WeatherForecastService:

    def __init__(self, language="en"):
        self.__api = OWM(OWM_API_KEY, language=language)
        self.__cache = LRUCache()

    @property
    def api(self):
        return self.__api

    def set_language(self, language):
        language = 'hr' if language == 'sr' else language
        self.api.set_language(language)

    def get_weather_at_location(self, location, out_format="json"):
        # if(out_format not in ("json", "xml")):
        #    raise ValueError("Only json and xml output formats are supporrted!")
        cache_value = self.__cache.get(location)
        if cache_value is not None:
            return cache_value
        if type(location) == str:
            target_function = self.api.weather_at_place
        elif (type(location) == int):
            target_function = self.api.weather_at_id
        elif (type(location) == tuple):
            target_function = self.api.weather_at_coords
        else:
            raise TypeError("Location type is not allowed")
        weather_data = target_function(location)
        self.__cache.set(location, weather_data)
        return weather_data.get_weather()

    def get_forecast(self, weather_data, param, **kwargs):
        if param == "all":
            weather_param = self.get_all_weather_params(weather_data, **kwargs)
        else:
            weather_param = self.get_weather_param(weather_data, param, **kwargs)
        return weather_param

    def get_weather_param(self, weather_data, param, **kwargs):
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

        return weather_param

    def get_all_weather_params(self, weather_data, **kwargs):
        weather = {}
        for param in WEATHER_PARAMS:
            weather[param] = self.get_weather_param(weather_data, param, **kwargs)
        return weather

    # def get_forecast_in_readable_form(self, forecast):
    def get_forecast_in_readable_form(self, weather_data, param, **kwargs):
        forecast = self.get_forecast(weather_data, param, **kwargs)
        display_str = ''
        for param, struct in WEATHER_PARAMETERS.items():
            if param in ("temperature_min", "temperature_max"): param = "temperature"
            # NOTE:pressure value is measured in hPa, which is equal to mbar
            weather_param_value = forecast[param]
            child_alias_status = struct[1]
            child_alias_value = struct[0]
            display_name = struct[2][self.api.get_language()]
            value = weather_param_value[child_alias_value] if child_alias_status == "child" else weather_param_value
            display_str += display_name + ": " + str(value) + "\n"
        return display_str

    def get_forecast_result(self, location, param="all", unit="celsius"):
        weather_data = self.get_weather_at_location(location)
        forecast_output = self.get_forecast_in_readable_form(weather_data, param, **{"unit": unit})
        return ActionResult(forecast_output, OK)

    def get_forecast_at(self, time):
        try:
            return (dir(self.__api.get_weather_at(time)))
        except Exception as e:
            print(e)
            return None

    def get_forecast_for_next_x_days(self, location, days_limit):
        forecast = self.__api.daily_forecast(location, limit=days_limit)
        return forecast  # get_forecast and get_weather_at

# ws = WeatherForecastService(lang='hr')
# ws_data = ws.get_weather_at_location('Kragujevac')
# print(ws.get_weather_param(ws_data, 'temperature', **{"unit":"celsius"}))
# print(ws.get_weather_param(ws_data, 'status'))
# print(ws.get_forecast_for_next_x_days("Novi Sad", 5))
# temp, temp_min, temp_max, pressure, humidity, cloud, wind
# only can say if it will be foggy, rainy etc
# import datetime

# fc = ws.get_forecast_for_next_x_days("Novi Sad", 5)
# print(fc.get_weather_at(datetime.datetime(2019, 8, 22, 8, 47, 0)))
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html
