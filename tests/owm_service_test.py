import sys
sys.path.append("..")

#from owm_service import WeatherForecastService
from services.webapi.owm_service import WeatherForecastService

wfs = WeatherForecastService()
# assertion check
# print(ws._get_weather_at_location("London", out_format="pdf"))
london_weather = wfs.get_forecast_result("London")
print(london_weather.get_result())
ws_data = wfs._get_weather_at_location('London')
print(ws_data.get_temperature(unit='celsius'))
w_data = wfs._get_forecast(ws_data, 'all', **{"unit": "celsius"})
print(w_data)
print(wfs._get_forecast_in_readable_form(ws_data, param_name="humidity"))
ws_data_5 = wfs._get_forecast_for_next_x_days("Novi Sad", 5)
w_data = ws_data_5.get_forecast().get_weathers()[0]
print(w_data)
print(wfs._get_weather_param(w_data, 'temperature', **{"unit": "celsius"}))
print(wfs._get_weather_param(ws_data_5, 'temperature', **{"unit": "celsius"}))
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html
