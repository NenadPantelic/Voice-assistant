from services.websearch.wikipedia_service import WikipediaService
from services.action_result import  ActionResult

from services.command_resolver import CommandResolver
from services.webapi.owm_service import WeatherForecastService
import datetime
wfs = WeatherForecastService()
ws_data = wfs.get_weather_at_location('London')
print(ws_data.get_temperature(unit = 'celsius'))
#w_data = wfs.get_forecast(ws_data, 'all', **{"unit":"celsius"})
#print(w_data)
#print(wfs.get_forecast_in_readable_form(w_data))
#print(
#ws_data_5 = wfs.get_forecast_for_next_x_days("Novi Sad", 5)
#print(dir(ws_data_5))
#get_forecat(), get_weather_at())
#w_data = ws_data_5.get_forecast().get_weathers()[0]
#print(dir(w_data))
#print((w_data.get_weathers()[0]))
#print(wfs.get_weather_param(w_data, 'temperature', **{"unit":"celsius"}))
#print(wfs.get_weather_param(ws_data_5, 'temperature', **{"unit":"celsius"}))

#print(wfs.get_forecast_at(datetime.datetime(2019, 9, 15, 8, 47, 0)))
