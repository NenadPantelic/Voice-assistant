from services.websearch.wikipedia_search import WikipediaService
from services.action_result import  ActionResult

from services.command_resolver import CommandResolver


ws = WikipediaService('en')
#print(ws.briefSearch('Nikola Jokić').getResult())
#print(ws.briefSearch.__wrapped__)

sr = CommandResolver("en")
sr.calculateServiceScores()
