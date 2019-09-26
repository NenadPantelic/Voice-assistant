import sys
sys.path.append("..")

from services.webapi.wikipedia_service import WikipediaService

ws = WikipediaService()
#exception case
#print(ws.brief_search("fsfsfsfs").get_result())
print(ws.brief_search("Mihajlo Pupin").get_result())

ws.set_language("sr")
print(ws.brief_search("Новак Ђоковић").get_result())
#assertion error
print(ws.brief_search("Новак Ђоковић", sentences=11).get_result())

