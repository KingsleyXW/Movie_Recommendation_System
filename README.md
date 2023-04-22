# WN2023 A Movie-Based Multimedia Recommendation System

## Introduction
The project is to build a Movie-Based multimedia recommendation system to recommend films and related media such as songs and books given user input parameters. First, the user inputs some parameters specifying the basic information about the film such as time length, rating threshold, year period, and so on. Once input relevant parameters, the system starts some preliminary processing to generate a number of films and their detailed information such as posters, type, plot, and other backgrounds. The user can review and choose the film he may like or ask the system to update another series of films that satisfy his input request. Once the user selects the film, the system can also recommend the relevant songs and books, or other relevant media about the film. The user can open the website to review further information. Finally, after the above functionality, the user can choose to recommend films based on his next selection or go back home page and start a new set of input requested searching. Several basic programming techniques are adopted in the project, which includes accessing data efficiently with caching via scraping and web API, and using Plotly and Flask for data visualization, etc.

## Data Sources
There 4 major data sources are used for the project, including 2 major source APIs which require API_KEY, and 2 minor sources which donn't need API_KEY

(1) The Movie Database API:
(https://developers.themoviedb.org/3/movies/get-movie-details). 

(2) Open Movie Database API:
(https://www.omdbapi.com/)

(3) Google Books API:
(https://developers.google.com/books/docs/v1/using). 

(4) iTunes API:
(https://performance-partners.apple.com/search-api)


## Data Structure
The following code indicates how I retrieve data, preprocess data and storage. Note, during the course of interactive selection. The user better select year within the recommendation range which is 2000~2020 to access the existed cache data, Or he might wait over 20 min till the preprcessing finished due to huge amount of data

```  
def movie_data_preprocessing(search_term, release_year, rating_threshold, time_length):
    """
    Preprocesses movie data by retrieving information from The Movie Database API and Open Movie Database API.
    ------------
    Args:
    search_term (str or None): The movie title to search for in the Open Movie Database API. If None, a list of movies
    will be retrieved from The Movie Database API based on the release year.
    release_year (int): The year in which the movie was released.
    rating_threshold (float): The minimum rating threshold for including a movie in the output list.
    time_length (int): The desired length of the movie in minutes.
    ------------
    Returns:
    MovieList_for_graph_processing (list): A list of movie dictionaries containing information such as title, director, runtime, country, genre, poster,
    and vote_average. Only movies that meet the rating threshold and time length requirements are included.
    """
    API_KEY=TMDB_API_KEY
    try:
        MovieList = read_json('./json_cache_'+str(release_year)+'.json')
    except:
        MovieList = []
        for half_year in range(1,3):
            for page in range(1,501):
                if half_year==1:
                    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&primary_release_date.gte={release_year}-01-01&primary_release_date.lte={release_year}-06-30&page={page}"
                elif half_year==2:
                    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&primary_release_date.gte={release_year}-07-01&primary_release_date.lte={release_year}-12-31&page={page}"
                response = requests.get(url)
                data = response.json()
                if len(data['results'])!=0:
                    MovieList.extend(data['results'])
        for movie in MovieList:
            movie_title = movie['title']
            if 'director' in list(movie.keys()) and 'runtime' in list(movie.keys()) and \
            'runtime' in list(movie.keys()) and 'genre' in list(movie.keys()) and \
            'poster' in list(movie.keys()):
                continue
            else:
                url = f"http://www.omdbapi.com/?t={movie_title}&apikey=" + OMDB_API_KEY
                response = requests.get(url)
                try:
                    detailed_data = response.json()
            
                    print(detailed_data,movie_title)
                    if list(detailed_data.keys())[1]!='Error':
                        movie['director'] = detailed_data['Director']
                        movie['runtime'] = detailed_data['Runtime']
                        movie['country'] = detailed_data['Country'].split(',')
                        movie['genre'] = detailed_data['Genre'].split(',')
                        movie['poster'] = detailed_data['Poster']
                        # print(movie['poster'])
                    else:
                        movie['director'] = 'Unknown'
                        movie['runtime'] = 'Unknown'
                        movie['country'] = 'Unknown'
                        movie['genre'] = 'Unknown'
                        movie['poster'] = 'Unknown'
                except:
                        movie['director'] = 'Unknown'
                        movie['runtime'] = 'Unknown'
                        movie['country'] = 'Unknown'
                        movie['genre'] = 'Unknown'
                        movie['poster'] = 'Unknown'
        write_json('./json_cache_'+str(release_year)+'.json', MovieList)

    if search_term is None:
        ratingThre = rating_threshold
        time_length =120
        timeMinThre = int(time_length) - 10
        timeMaxThre = int(time_length) + 10

    else:
        user_picked_movie_response = requests.get(search_term)
        user_picked_movie_item = user_picked_movie_response.json()
        if list(user_picked_movie_item.keys())[1]!='Error':
           print("There is no such movie or there is no detailed information regarding this movie\n, please inout another movie title")
           return False
        else:
            Title = user_picked_movie_item['Title']
            ratingThre = float(user_picked_movie_item['imdbRating'])
            time_length =user_picked_movie_item['Runtime'].split(' ')[0]
            timeMinThre = int(time_length) - 10
            timeMaxThre = int(time_length) + 10
    
    MovieList_for_graph_processing=[]
    for movie in MovieList:
        try:
            runTime = float(movie['runtime'].split(' ')[0])
        except:
            runTime = 0
        ratingAverage = float(movie['vote_average'])
        if runTime<=timeMaxThre and runTime>=timeMinThre and ratingAverage>=ratingThre:
            MovieList_for_graph_processing.append(movie)
    
    
    return MovieList_for_graph_processing

```  
The following code is how I do the graph processing:

```  
def graph_processing(self, movieClassListForGraph):
        '''
        Graph the movies based on their similarity scores and return the graph.

        Parameters
        ----------
        movieClassListForGraph : list of Movie objects
            The list of movies to be used in the graph.

        Returns
        -------
        G : Graph object
            The resulting graph of movies, where nodes represent movies and edges represent 
            their similarity scores.

        '''
        G = nx.Graph()
        for movie1 in movieClassListForGraph:
            G.add_node(movie1.title, attributes=movie1)
            for movie2 in movieClassListForGraph:
                G.add_node(movie2.title, attributes=movie2)
                if movie1 != movie2:
                   similarity_score =  calculate_similarity(movie1, movie2, self.weights)
                   if similarity_score>=0.05:
                      G.add_edge(movie1.title, movie2.title, weight=similarity_score)

        return G
```  

## Run the Program
### Step 1: Apply an API Key for OMDB and TMDB
(1) Go to The Movie Database API website (https://developers.themoviedb.org/3/movies/get-movie-details) and Open Movie Database API website (https://www.omdbapi.com/) to acquire your own unique API KEY

(2) Replace the TMDB_API_KEY and OMDB_API_KEY in the Final_project_main.py
```  
TMDB_API_KEY = '<your TMDB key>'
OMDB_API_KEY = '<your OMDB key>'
```  
### Step 2: Install packages
```
$ pip install -r requirements.txt --user
```  

### Step 3: Run Final_project_main.py  
```  
$ python Final_project_main.py
```  
### Step 4: Open "http://127.0.0.1:5000/ " in a browser
