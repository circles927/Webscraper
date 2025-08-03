# module1, redefined using youtube video tips

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def getAllMainLinksFromURL(currentURL):
    retrievedURLs = []

    # Attempt to retrieve and print links from the given URL
    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a'):
            path = link.get('href')

            if path and path.startswith('/'):
                retrievedURLs.append(currentURL)
                print(f"Found link: {currentURL}")
            else:
                domain = urlparse(f"{path}").netloc
                retrievedURLs.append(domain)
                print(f"Found link: {domain}")

    except:
        print("something bad happened for this url: " + currentURL)

    # Attempt to remove duplicates from the list of URLs
    try:
        uniqueURLs = turnListIntoSetVersa(retrievedURLs)
    except:
        uniqueURLs = retrievedURLs

    return uniqueURLs

def turnListIntoSetVersa(listOfSorts):
    setBetween = set(listOfSorts)
    listAgain = list(setBetween)

    return listAgain