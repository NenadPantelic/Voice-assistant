from services.websearch.wikipedia_service import WikipediaService
from services.action_result import  ActionResult

from services.command_resolver import CommandResolver


ws = WikipediaService('en')
#print(ws.brief_search('Nikola Jokić').get_result())
#print(ws.brief_search.__wrapped__)

sr = CommandResolver("en")
sr.calculateServiceScores()
