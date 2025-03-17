from ActorScrap import main
from CastScrap import cast_datar
# Get an actor filmography details
person_name = "Leonardo DiCaprio"
leo_filmography = main(person_name)
print(leo_filmography)
#///////////////////////////////////////
#Get a movie cast details
movie_page = 'https://www.themoviedb.org/movie/634649-spider-man-no-way-home/cast'
NWH_cast = cast_datar(movie_page,"Spider-Man: No Way Home")
print(NWH_cast)