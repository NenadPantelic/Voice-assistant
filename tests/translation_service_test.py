import sys

sys.path.append("..")
from services.webapi.translation_service import TranslationService

translator = TranslationService()
# private method access violation
print(translator.detect_language_from_text('Ja sam Nenad Pantelić iz Srbije'))

translated = translator.translate_text('I\'m not your mother Nicky', src_language='english', dest_language='french')
print(translated.get_result())
translated = translator.translate_text('Ja danas branim diplomski rad', src_language="sr", dest_language='french')
print(translated.get_result())


print(translator._detect_language('Kak ste kaj'))
text = 'Kuullut jos jostain ole konsuli alkanut pistaen vai. Harva iso kai hanna sanoa nyt. Lisaa ne uskoa pohja aikaa joita ja. Salaa se se yksin jolta ne ai. Ero paastanyt jos pianaikaa jos mimmoinen seisomaan merirosvo arentinsa. No torjuen jo antaisi tuhatta nuorten aitinsa et hanelle. Ne huoneen tulevan on ei leikkia heraten kuulkaa. Housunsa vaikenee paivassa he se vedappas vallassa vahinkoa. Liikkeelle jai kas onnestanne varmaankin mielellaan. Ai pain juon ajat aave ne ne aiti se. '
lang = translator._detect_language(text)
print(lang)
print(translator.translate_text(text, src_language=lang.lang))
print(translator.translate_text(text, src_language=lang.lang, dest_language="french"))
print(translator._convert_language_to_lang_code(None))

text = "Moре Марко не ори друмове."
lang = translator.detect_language_from_text(text).get_result()
print(translator.translate_text(text, lang, "german"))
print(translator.translate_text(text, lang, "italian"))

#https://py-googletrans.readthedocs.io/en/latest/

