import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from Souper import souper

def get_work_page(movie_query_name):
    encoded_query_name = urllib.parse.quote(movie_query_name)
    search_page = f"https://www.themoviedb.org/search?query={encoded_query_name}"
    search_soup = souper(search_page)
    title = search_soup.find("div", {'class' : 'title'} )
    if (title.h2.text.lower() == movie_query_name.lower()):
        link_href = title.a['href']
        the_page = f"https://www.themoviedb.org{link_href}"
        print(the_page)
    else :
        print("No Page Found")