import sys
sys.path.append("..")
from services.websearch.browser_search_service import BrowserService
from config.constants import FACEBOOK_BASE_URL, TWITTER_BASE_URL, INSTAGRAM_BASE_URL, LINKEDIN_BASE_URL
bs = BrowserService()
#exception case
#print(bs._get_first_search_result(query="lionfsdfdjnefedmfurniojgigf").get_result())
print(bs._get_first_search_result(query="lion").get_result())
print(bs._get_first_search_result(query="Новак Ђоковић").get_result())
bs.open_found_url_in_browser("lion")
bs.open_found_url_in_browser("Новак Ђоковић")
bs.open_found_url_in_browser("lion", tpe="isch")


print(bs._get_first_search_result(query="lion", tpe="isch").get_result())
print(bs.open_social_network_page("nenad-pantelić", LINKEDIN_BASE_URL))