# module1, redefined using youtube video tips

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def getAllMainLinksFromURL(currentURL):
    # Attempt to retrieve and print links from the given URL
    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a'):
            path = link.get('href')

            if path and path.startswith('/'):
                yield currentURL
            else:
                domain = urlparse(f"{path}").netloc
                yield domain

    except:
        print("something bad happened for this url: " + currentURL)

def turnListIntoSetVersa(listOfSorts):
    setBetween = set(listOfSorts)
    listAgain = list(setBetween)

    return listAgain