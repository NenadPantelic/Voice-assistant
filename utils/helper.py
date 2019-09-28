import googletrans
from services.webapi.translation_service import  TranslationService

# NOTE: this was used in other file, so it is not tested here (possible problems with imports)
translator = TranslationService()

langs = googletrans.LANGCODES.keys()
sr_langs = {}
for lang in langs:
    sr_langs[translator.translate(text=lang, src_lang="en", dest_lang="sr").text.lower()] = lang

import json

with open('data/langs_in_serbian.json', 'w', encoding='utf8') as f:
    json.dump(sr_langs, f, ensure_ascii=False)

with open('data/langs_codes.json', 'w', encoding='utf8') as f:
    json.dump(googletrans.LANGCODES, f, ensure_ascii=False)
