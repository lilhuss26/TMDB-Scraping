from Souper import souper
import pandas as pd

def cast_datar (cast_link,movie_name):
    cast_src = souper(cast_link)
    cast_raw = cast_src.find("ol",{'class':'people'})
    cast_names_soup = cast_raw.find_all("li")
    cast_data_temp = []
    for inf in cast_names_soup:
        actor =  inf.find("div",{'class':'info'}).p.a.text
        character = inf.find("p",{'class':'character'}).text.strip()
        cast_data_temp.append({'actor': actor, 'character': character})
    for cast_member in cast_data_temp:
        cast_member['movie'] = movie_name
    cast_data = pd.DataFrame(cast_data_temp)
    return cast_data