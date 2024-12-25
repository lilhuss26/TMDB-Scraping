import requests
from bs4 import BeautifulSoup
def souper (one_link):
    page = requests.get(one_link)
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    return soup