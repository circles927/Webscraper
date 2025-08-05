# module1, redefined using youtube video tips

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def getAllMainLinksFromURL(currentURL):
    # Attempt to retrieve and print links from the given URL
    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a'):
            # Searches the link
            path = link.get('href')

            if path and path.startswith('/'):
                # If the link doesn't have www, leave it out
                yield currentURL
            else:
                # Cut the link to the main domain name only
                domain = urlparse(f"{path}").netloc
                yield domain

    except:
        print("something bad happened for this url: " + currentURL)

def turnListIntoSetVersa(listOfSorts):
    # Turns a list into a set and back to a list to remove duplicates
    setBetween = set(listOfSorts)
    listAgain = list(setBetween)

    return listAgain