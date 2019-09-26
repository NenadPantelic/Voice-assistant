# imdb = IMDBService()
# imdb.get_movie_by_title('Titanic')

from services.webapi.translation_service import TranslationService

translator = TranslationService()
# print(translator.translate('Ja sam Nenad Pantelić iz Srbije'))

# translated = translator.translate('I\'m not your mother Nicky', src_lang = 'english',dest_lang = 'french')
# translated = translator.translate('Ja danas branim diplomski rad', dest_lang = 'french')

# print(translated.text)
# print(dir(translated))
# print(translated.dest)

# print(translator.detect_language('Kak ste kaj'))
text = 'Kuullut jos jostain ole konsuli alkanut pistaen vai. Harva iso kai hanna sanoa nyt. Lisaa ne uskoa pohja aikaa joita ja. Salaa se se yksin jolta ne ai. Ero paastanyt jos pianaikaa jos mimmoinen seisomaan merirosvo arentinsa. No torjuen jo antaisi tuhatta nuorten aitinsa et hanelle. Ne huoneen tulevan on ei leikkia heraten kuulkaa. Housunsa vaikenee paivassa he se vedappas vallassa vahinkoa. Liikkeelle jai kas onnestanne varmaankin mielellaan. Ai pain juon ajat aave ne ne aiti se. '
# lang = translator.detect_language(text)
# print(lang)
# print(translator.translate(text, src_lang=lang.lang))
# print(translator.translate_text_(text, "french"))
# print(translator.convert_language_to_lang_code(None))

text = "Моja кућа је далеко где ме стара мајка чека"
# print(translator.detect_language_from_text("Ja sam Marko Marković").get_result())
# print(translator.detect_language_from_text(text))

# print(translator.translate_text_(text, "german"))
# print(translator.translate_text_(text, "german"))
# print(translator.translate_text_(text, "german"))
# print(translator.translate_text_(text, "italian"))


'''
langs = googletrans.LANGCODES.keys()
sr_langs = {}
for lang in langs:
    sr_langs[translator.translate(text=lang, src_lang="en", dest_lang="sr").text.lower()] = lang

import json
with open('data/langs_in_serbian.json', 'w', encoding='utf8') as f:
    json.dump(sr_langs, f, ensure_ascii = False)
    

import json
with open('data/langs_codes.json', 'w', encoding='utf8') as f:
    json.dump(googletrans.LANGCODES, f, ensure_ascii = False)

'''

'''


'''

# from services.system.os_service import *

# print(subprocess.Popen(['echo',x[0]]))

from services.system.os_service import OSService

os_srv = OSService()
# os_srv.execute_command("date")
# print(os_srv.execute_command("sudo find / -name 'subprocess.py'"))
# file = os_srv.search_file("cat.jpg")
# file = os_srv.search_file("temporary.mp3")

# print(file)
# print(os_srv.open_file(file))
# print(os_srv.get_computer_status())
# print(os_srv.get_pid("chrome"))


# get_exception_message

