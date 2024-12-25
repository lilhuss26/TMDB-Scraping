import pandas as pd
import urllib.parse
from Souper import souper

def get_person_page(person_query_name):
    encoded_person_name = urllib.parse.quote(person_query_name)
    search_page = f"https://www.themoviedb.org/search?query={encoded_person_name}"
    search_soup = souper(search_page)
    name = search_soup.find('p', {'class' : 'name'} )
    if (name.a.text.lower()  == person_query_name.lower()):
        link_href = name.a['href']
        person_name_page = f"https://www.themoviedb.org{link_href}"
        return person_name_page
    else :
        print("No Page Found")

def find_works (person_page):
    per_soup = souper(person_page)
    credits_list = per_soup.find("div",{'class':'credits_list'})
    parts = credits_list.find_all("table",{'class':'card credits'})
    roles = []
    for i in credits_list.find_all('h3'):
        roles.append(i.text)
    works = []
    for group in parts:
        maps = group.find_all('a',{'class': 'tooltip'})
        works.append(maps)
    works_links = []
    unique_works_links = set()
    for group in works:
        group_links = []
        for work in group:
            work_href = work['href']
            if not work_href.startswith('/tv'):
                url = f"https://www.themoviedb.org{work_href}"
            if url not in unique_works_links:
                unique_works_links.add(url)
                group_links.append(url)
        works_links.append(group_links)
    roles_links = {}
    for role, links in zip(roles, works_links):
        roles_links[role] = [link for link in links]
    return roles_links

def movie_datar(movie_page):
    movie_src = souper(movie_page)
    movie_header = movie_src.find("section", {'class': 'header'})

    # Handle potential exceptions and assign default values
    movie_name = ''
    release_year = '-'
    movie_runtime = '-'
    movie_age = '-'
    director = '-'
    movie_score = '-'
    movie_genres = '-'
    status = ''
    language = ''
    Budget = ''
    revenue = ''

    try:
        movie_name = movie_header.a.text
    except AttributeError:
        pass
    try:
        release_year = movie_header.find("span", {'class': 'release_date'}).text.strip('()')
    except AttributeError:
        pass
    try:
        movie_runtime = movie_header.find("span", {'class': 'runtime'}).text.strip()
    except AttributeError:
        pass
    try:
        movie_age = movie_header.find("span", {'class': 'certification'}).text.strip()
    except AttributeError:
        pass
    try:
        director = movie_header.find('p', {'class': 'character'}).parent.p.a.text
    except AttributeError:
        pass
    try:
        movie_score = movie_header.find("div", {'class': 'user_score_chart'}).get('data-percent')
    except AttributeError:
        pass
    try:
        genres = movie_header.find("span", {'class': 'genres'}).find_all('a')
        all_genres = [genre.text for genre in genres]
        movie_genres = ', '.join(all_genres)
    except AttributeError:
        pass
    try:
        facts_columns = movie_src.find("section", {'class': 'facts left_column'})
        facts_raw = facts_columns.find_all('p')
        facts_all = [fact.bdi.decompose() for fact in facts_raw]
        status = facts_raw[0].text.strip()
        language = facts_raw[1].text.strip()
        Budget = facts_raw[2].text.strip()
        revenue = facts_raw[3].text.strip()
    except AttributeError:
        pass

    data_temp = {
        'Name': movie_name,
        'Release Year': release_year,
        'Runtime': movie_runtime,
        'Age Rating': movie_age,
        'Director': director,
        'Score': movie_score,
        'Genres': movie_genres,
        'Status': status,
        'Language': language,
        'Budget': Budget,
        'Revenue': revenue
    }
    movie_data = pd.DataFrame(data_temp, index=[0])
    return movie_data

def main (person_name):
    person_page = get_person_page(person_name)
    movies = find_works(person_page)
    all_movie_data = []
    for role,links in movies.items():
        for link in links:
            movie_data = movie_datar(link)
            movie_data['Role'] = role
            all_movie_data.append(movie_data)
    if all_movie_data:
        combined_data = pd.concat(all_movie_data, ignore_index=True)  # Combine all movie data
        return combined_data
    else:
        return None
    #return all_movie_data