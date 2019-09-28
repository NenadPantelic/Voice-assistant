# imdb = IMDBService()
# imdb.get_movie_by_title('Titanic')

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

