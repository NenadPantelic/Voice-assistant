#search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
'''

query : query string that we want to search for.
tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
lang : lang stands for language.
num : Number of results we want.
start : First result to retrieve.
stop : Last result to retrieve. Use None to keep searching forever.
pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
'''

#import googlesearch

'''
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = "Geeksforgeeks"

for j in search(query, tld="com", num=10, stop=1, pause=2):
    print(j)
'''
j = 'https://www.geeksforgeeks.org/'
import threading


#https://python-googlesearch.readthedocs.io/en/latest/

#https://docs.python.org/2/library/webbrowser.html

'''
webbrowser.open(url, new=1, autoraise=True)
Display url using the default browser. If new is 0, the url is opened in the same browser window if possible. If new is 1, a new browser window is opened if possible. If new is 2, a new browser page (“tab”) is opened if possible. If autoraise is True, the window is raised if possible (note that under many window managers this will occur regardless of the setting of this variable).

Note that on some platforms, trying to open a filename using this function, may work and start the operating system’s associated program. However, this is neither supported nor portable.

Changed in version 2.5: new can now be 2.

webbrowser.open_new(url)
Open url in a new window of the default browser, if possible, otherwise, open url in the only browser window.

webbrowser.open_new_tab(url)
Open url in a new page (“tab”) of the default browser, if possible, otherwise equivalent to open_new().

New in version 2.5.

'''

import webbrowser
import time

def open_url(url, new, autoraise=False):
    webbrowser.open(url, new=2, autoraise=False)
    time.sleep(5)
def open_window(url):
    webbrowser.open_new(url)

def open_tab(url):
    webbrowser.open_tab(url)

x = threading.Thread(target=open_url, args=(j,2))
x.start()

print("Ovde")

#https://realpython.com/intro-to-python-threading/

for i in range(10):
    print(i)