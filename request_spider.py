import requests
from bs4 import BeautifulSoup
from estela_requests_wrapper.requests_wrapper import RequestsWrapperSession
from urllib.parse import urljoin

url = "https://stackoverflow.com/questions/tagged/web-scraping"
session = RequestsWrapperSession()
counter = 10
def get_pages(act_url, i):
    response = session.get(act_url)
    soup = BeautifulSoup(response.content, "html.parser")
    next_link = soup.find('a', {'rel': 'next'})
    next_page = urljoin(act_url, next_link["href"])
    print(next_page)
    i += 1
    if counter < i:
        return
    get_pages(next_page, i)

get_pages(url, 0)
