# TMDB-Scraping
This code takes a director or actor's name and scrap data of every project he worked on from [TMDB](https://www.themoviedb.org)
## Functions
### Souper 
This function returns the soup (HTML code) for any link, using "lxml" parser
### get_person_page
Since we can't move directly to an actor link page with his name,
because the link contains a unique code like this "https://www.themoviedb.org/person/138-quentin-tarantino",
we create a bot to simulate the search process.
We extract the herf EX:(/person/138-quentin-tarantino) of the actor from the result box we scraped from the query page.
### find_works
This function takes the link got extracted from the `get_person_page`, to get a list of the link of every work the actor envolved in, grouped by his role.
+ `credits_list` scraps the credits list div that have all the card credits of every role.
+ `parts` divide the credit cards in the 'credit list'
+ `roles` list have the roles from the credit cards
+ Now we loop over every credit card get the herf of the movies only, add the base url to it, and add it to `works_links`, then create the `roles_links` to group the links by the actor role.
### movie_datar
This function takes one movie page link, and scrap it.
We scrap the movie_name, release_year, movie_runtime, movie_age, director, movie_score,movie_genres from the movie page head, the rest of the data from the facts left column.
## main
We call `get_person_page` & `find_works`.Then iterate over each group of movie links under a role to scrap it using `movie datar`.
Then make it a pandas data frame.
### cast_datar
Also, we have a function to scrape a movie cast and the characters they played, and sort it in a pandas data frame.
