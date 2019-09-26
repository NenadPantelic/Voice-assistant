from config.constants import FACEBOOK_BASE_URL, TWITTER_BASE_URL, INSTAGRAM_BASE_URL, LINKEDIN_BASE_URL, logger

social_networks_url_map = {"facebook": FACEBOOK_BASE_URL, "twitter": TWITTER_BASE_URL, \
                           "instagram": INSTAGRAM_BASE_URL, "linkedin": LINKEDIN_BASE_URL}

tpe_map = {"videos": "vid", "images": "isch", "news": "nws", "shopping": "shop", "books": "bks", "applications": "app"}


def get_social_network_base_url(social_network_str):
    for social_network, url in social_networks_url_map.items():
        if social_network in social_network_str:
            return url

    return None


# TODO:adapt to serbian phrases (for both methods)
def get_search_type(type_str):
    for type, type_code in tpe_map.items():
        if type in type_str:
            return type_code

    return ''


def get_relay_state(arduino_control_str):
    keywords = {"switch": ("switch", "promeni", "stanje"), "power on": ("power on", "turn on", "switch on",
                                                                        "uključi", "upali", "aktiviraj"),
                "power off": ("power off", "turn off", "switch off", "isključi", "ugasi",
                              "deaktiviraj")}
    logger.debug("Converting input command to control demand....")
    for target_word, assoc_words in keywords.items():
        if any(word in assoc_words for word in arduino_control_str):
            return target_word
    #NOTE:default case is switch (scenarios when speech is not recognized correctly)
    return "switch"
