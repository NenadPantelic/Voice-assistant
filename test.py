from services.websearch.wikipedia_service import WikipediaService
from services.action_result import  ActionResult
from services.webapi.imdb_service import IMDBService
from services.command_resolver import CommandResolver
from services.webapi.owm_service import WeatherForecastService
import datetime
#wfs = WeatherForecastService()
#ws_data = wfs.get_weather_at_location('London')
#print(ws_data.get_temperature(unit = 'celsius'))
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

#imdb = IMDBService()
#imdb.get_movie_by_title('Titanic')

from services.webapi.translation_service import TranslationService


translator = TranslationService()
#print(translator.translate('Ja sam Nenad Pantelić iz Srbije'))

#translated = translator.translate('I\'m not your mother Nicky', src_lang = 'english',dest_lang = 'french')
#translated = translator.translate('Ja danas branim diplomski rad', dest_lang = 'french')

#print(translated.text)
#print(dir(translated))
#print(translated.dest)

#print(translator.detect_language('Kak ste kaj'))
text = 'Kuullut jos jostain ole konsuli alkanut pistaen vai. Harva iso kai hanna sanoa nyt. Lisaa ne uskoa pohja aikaa joita ja. Salaa se se yksin jolta ne ai. Ero paastanyt jos pianaikaa jos mimmoinen seisomaan merirosvo arentinsa. No torjuen jo antaisi tuhatta nuorten aitinsa et hanelle. Ne huoneen tulevan on ei leikkia heraten kuulkaa. Housunsa vaikenee paivassa he se vedappas vallassa vahinkoa. Liikkeelle jai kas onnestanne varmaankin mielellaan. Ai pain juon ajat aave ne ne aiti se. '
#lang = translator.detect_language(text)
#print(lang)
#print(translator.translate(text, src_lang=lang.lang))
#print(translator.translate_text_with_auto_detection(text, "french"))
#print(translator.convert_language_to_lang_code(None))

text = "Моja кућа је далеко где ме стара мајка чека"
print(translator.detect_language_from_text("Ja sam Marko Marković").get_result())
#print(translator.detect_language_from_text(text))

#print(translator.translate_text_with_auto_detection(text, "german"))
#print(translator.translate_text_with_auto_detection(text, "german"))
#print(translator.translate_text_with_auto_detection(text, "german"))
#print(translator.translate_text_with_auto_detection(text, "italian"))