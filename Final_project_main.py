import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import secret
import sqlite3
import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots
from plotly.offline import plot 
from flask import Flask, render_template, Markup
from flask import request

TMDB_API_KEY='b6b67d5a0231de406a62568976194959'
OMDB_API_KEY='a701bb8e'

app = Flask(__name__)

def read_json(filepath, encoding='utf-8'):
    """Reads a JSON file and convert it to a Python dictionary

    Parameters:
    -------------------
        filepathz: str 
                 a path to the JSON file
        encoding: str
                 name of encoding used to decode the file

    Returns:
    -------------------
        dict/list: dict or list representations of the decoded JSON document
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
    -------------------
        filepath: str
                 the path to the file
        data: (dict)/(list): 
                  the data to be encoded as JSON and written to
                  the file
        encoding: str
                  name of encoding used to encode the file
        indent: int
                  number of "pretty printed" indention spaces applied to
                  encoded JSON

    Returns:
    -------------------
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
    
class Movie:
    """
    A class representing a movie with various attributes like title, release date, director, genre, plot, rating,
    ID, runtime, and popularity.

    Attributes:
        title (str): The title of the movie.
        id (str): The ID of the movie.
        runtime (int): The runtime of the movie in minutes.
        release_date (str): The release date of the movie in YYYY-MM-DD format.
        director (str): The director of the movie.
        genre (str): The genre of the movie.
        plot (str): The plot summary of the movie.
        rating (float): The rating of the movie.
        popularity (float): The popularity of the movie.
        Dict (dict): A dictionary containing the attribute values to initialize the movie with.

    Methods:
        __init__(self, title="None", id='none', runtime=0, release_date="None", director="None", genre="None",
                 plot="None", rating=0, popularity=0, Dict=None): Initializes a new instance of the Movie class with
                 either specific attribute values or a dictionary containing these values.
    """
    def __init__(self, title="None", id='none', runtime=0,release_date="None", director="None", genre="None", plot="None", rating=0, popularity=0, Dict=None):
        if Dict==None:
            self.title = title
            self.release_date = release_date
            self.director = director
            self.genre = genre
            self.plot = plot
            self.rating = rating
            self.id = id
            self.popularity=popularity
        else:
            self.title = Dict['title']
            self.year = Dict['release_date']
            self.director = Dict['director']
            self.genre = Dict['genre']
            self.genreIDs = Dict['genre_ids']
            self.plot = Dict['overview']
            self.rating = Dict['vote_average']
            self.id = Dict['id']
            self.runtime = Dict['runtime']
            self.popularity = Dict['popularity']
            self.poster = Dict['poster']
            self.country = Dict['country']

# Book class to store book information
class Book:
    """
    A class representing a book with various attributes like title, author, publisher, publication date, and preview link.

    Attributes:
        title (str): The title of the book.
        author (str): The author(s) of the book.
        publisher (str): The publisher of the book.
        publication_date (str): The publication date of the book in YYYY-MM-DD format.
        preview (str): The preview link of the book.
        Dict (dict): A dictionary containing the attribute values to initialize the book with.

    Methods:
        __init__(self, title="None", author="None", publisher="None", publication_date="None", preview='None',
                 Dict=None): Initializes a new instance of the Book class with either specific attribute values or a
                 dictionary containing these values.
    """
    def __init__(self, title="None", author="None", publisher="None", publication_date="None",preview='None', Dict=None):
        if Dict==None:
            self.title = title
            self.author = author
            self.publisher = publisher
            self.publication_date = publication_date
            self.preview = preview
        else:
            self.title = Dict['title']
            self.author = Dict['authors']
            self.publisher = Dict['publisher']
            self.publishedDate = Dict['publishedDate']
            self.preview = Dict['previewLink']
            
class Song:
    '''a standard media subclass that contains many insitance attribute of songs
    such as title, author and release year and so on.

    Attributes:
        title (str): The title of the song.
        author (str): The author(s) of the song.
        release_date (str): The release date of the song in YYYY format.
        url (str): The URL of the song.
        album (str): The album that the song belongs to.
        genre (str): The genre of the song.
        track_length (int): The length of the song in milliseconds.
        Dict (dict): A dictionary containing the attribute values to initialize the song with.

    Methods:
        __init__(self, title="No Title", author="No Author", release_date="No Release date", url="No URL", album="No Album",
                 genre="No Genre", track_length=0, Dict=None): Initializes a new instance of the Song class with either specific
                 attribute values or a dictionary containing these values.
    '''
    def __init__(self, title="No Title", author="No Author", release_date="No Release date", url="No URL", album="No Album", genre="No Genre", track_length=0, Dict=None):

        if Dict is None:
            self.author = author
            self.title = title
            self.album = album
            self.genre = genre
            self.track_length = track_length
            self.release_date = release_date
            self.url = url
        else:
            if Dict.get("trackName") is not None:
                self.title = Dict['trackName']
            elif Dict.get("collectionName") is not None:
                self.title = Dict['collectionName']
            else:
                self.title = "No Title"
            
            if Dict.get("artistName") is not None:
                self.author = Dict['artistName']
            else:
                self.author = "No Author"
            
            if Dict.get("releaseDate") is not None:
               self.release_date = Dict['releaseDate'].split("-")[0]
            else:
                self.release_date = "No Release Date"

            if Dict.get("trackViewUrl") is not None:
                self.url = Dict['trackViewUrl']
            elif Dict.get("collectionViewUrl") is not None:
                 self.url = Dict['collectionViewUrl']
            else:
                self.url = "No Url"
                
            if Dict.get("collectionName") is not None:
               self.album = Dict['collectionName']
            else:
                self.album = "No Album"
                
            if Dict.get("primaryGenreName") is not None:
                self.genre = Dict['primaryGenreName']
            else:
                self.genre = "No Genre"
                
            if Dict.get("trackTimeMillis") is not None:
                   self.track_length = int(Dict['trackTimeMillis'])/1e3
            else:
                self.track_length = 0
                
def retrieve_song_info(search_term):
    '''This function is to generate media object lists given 
    combined search information

    Args
    -------------------
    search: string
        the string specifying the Itune API websites and search term
    Returns
    -------
    song_list: list 
        the list contain song objects
    movie_list: list 
        the list containing movie objects
    other_list: list 
        the list containing other media objects
    total_media_list: list 
        the list containing combined objects of song, movie and other media
    
    '''
    base_url = 'https://itunes.apple.com/search?term="'
    search = base_url + search_term
    song_list = []
    song_kind = ['album', 'song']

    initial_results = requests.get(search)
    json_output = initial_results.json()
    itunes_list = json_output['results']
    
    for item in itunes_list:
        if item.get("kind") is not None:
            kind = item['kind']
            if kind in song_kind:
                S = Song(Dict=item)
                song_list.append(S)

    return song_list

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
        time_length =time_length
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

# Function to calculate similarity score between two movies based on weights
def calculate_similarity(movie1, movie2, weights):
    '''
    Calculates the similarity score between two movie objects based on their attributes and weights assigned to each attribute.
    --------
    Args:
        movie1 (Movie): The first movie object to compare.
        movie2 (Movie): The second movie object to compare.
        weights (dict): A dictionary containing the weights assigned to each attribute.
    --------
    Returns:
        relevance_score (float): The relevance score between the two movies based on their attributes and weights assigned to each attribute.
    '''

    relevance_score = weights["Director"] * (movie1.director == movie2.director) + \
                      weights["Genre"] * bool(set(movie1.genreIDs).intersection(movie2.genreIDs)) + \
                      weights["Rating"] * (movie1.rating == movie2.rating) + \
                      weights["Popularity"] * (movie1.popularity == movie2.popularity) + \
                      weights["Country"] * bool(set(movie1.country).intersection(movie2.country))+ \
                      weights["Runtime"] * (float(movie1.runtime.split(' ')[0]) == float(movie2.runtime.split(' ')[0]))
    return relevance_score

# Film Recommendation System class
class FilmRecommendationSystem:
    """
    A class that recommends movies based on user input and calculates similarity score between movies.

    Parameters:
    ----------
    Director_weights : float, optional
        The weight assigned to the Director of the movie. Default is 0.3.
    Genre_weights : float, optional
        The weight assigned to the Genre of the movie. Default is 0.2.
    Ratings_weights : float, optional
        The weight assigned to the Ratings of the movie. Default is 0.25.
    Runtime_weights : float, optional
        The weight assigned to the Runtime of the movie. Default is 0.05.
    Country_weights : float, optional
        The weight assigned to the Country of the movie. Default is 0.05.
    popularity_weights : float, optional
        The weight assigned to the Popularity of the movie. Default is 0.15.

    Attributes:
    -----------
    movies_cache : dict
        A dictionary to store the movie data.
    weights : dict
        A dictionary of pre-defined weights for movie properties.

    Methods:
    --------
    recommend_movies(user_input_year, user_input_rating_threshold, user_input_time_threshold, user_input_search_term)
        Recommends movies based on user input.
    graph_processing(movieClassListForGraph)
        Calculates the similarity score between movies.

    """
    def __init__(self, Director_weights=0.3, Genre_weights=0.2, Ratings_weights=0.25, Runtime_weights=0.05, Country_weights=0.05, popularity_weights=0.15):
        """
        Initializes the FilmRecommendationSystem object with the given weights for movie properties.

        Parameters:
        ----------
        Director_weights : float, optional
            The weight assigned to the Director of the movie. Default is 0.3.
        Genre_weights : float, optional
            The weight assigned to the Genre of the movie. Default is 0.2.
        Ratings_weights : float, optional
            The weight assigned to the Ratings of the movie. Default is 0.25.
        Runtime_weights : float, optional
            The weight assigned to the Runtime of the movie. Default is 0.05.
        Country_weights : float, optional
            The weight assigned to the Country of the movie. Default is 0.05.
        popularity_weights : float, optional
            The weight assigned to the Popularity of the movie. Default is 0.15.

        Returns:
        --------
        None
        """
        self.movies_cache = {} # Cache to store movie data
        self.weights = { # Pre-defined weights for movie properties
            "Director": Director_weights,
            "Genre": Genre_weights,
            "Rating": Ratings_weights,
            "Runtime": Runtime_weights,
            "Country": Country_weights,
            "Popularity": popularity_weights
            # Add more properties and weights as needed
        }

    # Method to recommend movies based on user input
    def recommend_movies(self, user_input_year, user_input_rating_threshold,user_input_time_threshold, user_input_search_term):
        """
        Recommends movies based on user input.

        Parameters:
        ----------
        user_input_year : int
            The year in which the user wants to see the movies.
        user_input_rating_threshold : float
            The minimum rating of the movie that the user wants to see.
        user_input_time_threshold : float
            The maximum length of the movie in minutes that the user wants to see.
        user_input_search_term : str
            The search term entered by the user.

        Returns:
        --------
        movieClassListForGraph : list
            A list of Movie objects recommended based on user input.
        """
        movieListForGraph = movie_data_preprocessing(user_input_search_term, user_input_year, user_input_rating_threshold,user_input_time_threshold)
        # here we finally introduce movie class to keep the useful information

        movieListForGraph.sort(key=lambda x: x["vote_average"], reverse=True) # Sort movies by rating
        movieClassListForGraph=[]
        for movieItem in movieListForGraph:
            movieClassListForGraph.append(Movie(Dict=movieItem))

        return movieClassListForGraph
    
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

def run_main(year=2005,rate=7, rumtimelen=120):
    """
    Run the main function of the Film Recommendation System to generate a list of recommended movies.

    Parameters
    ----------
    year : int, optional
        The release year of the movies to consider. Default is 2005.
    rate : float, optional
        The minimum rating threshold of the movies to consider. Default is 7.
    rumtimelen : int, optional
        The average runtime length of the movies to consider. Default is 120.

    Returns
    -------
    list
        A sorted list of recommended movies based on the input parameters.

    """
    release_year = year
    rating_threshold = rate
    time_length =rumtimelen

    user_input_year=release_year
    user_input_rating_threshold=rating_threshold
    user_input_time_threshold=time_length
    user_input_search_term=None
    moviesorted=FilmRecommendationSystem().recommend_movies(user_input_year, user_input_rating_threshold, user_input_time_threshold, user_input_search_term)

    return moviesorted



def flask_plot(xvals, yvals, title, fig_type):
    ''' this function generetes either bar chart or pie chart 
        and return the plot which will be use for display in web

    Parammeters
    -----------
    xvals: list
        a list of x values
    yvals: list
        a list of y values that correspond to the x values
    title: string
        the title of the plot
    fig_type: string
        either "bar" or "pie" that defines the output plot type

    Returns
    --------
    fig_div: string
        the plot that is readable by html files
    '''
    fig = make_subplots(rows=1, cols=1, specs=[[{"type": fig_type}]], subplot_titles=(title))
    if fig_type == 'pie':
        fig.add_trace(go.Pie(labels=xvals, values=yvals), row=1, col=1)
        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    elif fig_type == 'bar':
        fig.add_trace(go.Bar(x=xvals, y=yvals), row=1, col=1)
    
    fig.update_layout(annotations=[dict(text=title, font_size=25, showarrow=False)])
    fig_div = plot(fig, output_type="div")
    return fig_div


def rating_trend(releaseYear=2005,ave_rating=7,running_time=120):
    """
    Generates a bar plot of movie ratings for movies released in a given year, with a minimum rating and runtime.

    Parameters:
    -----------
    releaseYear: int, optional (default=2005)
        The year of release for the movies to consider.

    ave_rating: float, optional (default=7)
        The minimum average rating for the movies to consider.

    running_time: int, optional (default=120)
        The average running time for the movies to consider.

    Returns:
    --------
    matplotlib figure object:
        A bar plot of the ratings for the movies that meet the given criteria.
    """
    movieList=run_main(releaseYear,ave_rating,running_time)

    xvals = []
    yvals = []

    for movie in movieList:
        xvals.append(movie.title)
        yvals.append(float(movie.rating))
    
    title = 'Movie Rating graph according to user selection'
    return flask_plot(xvals, yvals, title, 'bar')

def popularity_trend(releaseYear=2005,ave_rating=7,running_time=120):
    """
    Generates a bar plot of movie popularity for movies released in a given year, with a minimum rating and runtime.

    Parameters:
    -----------
    releaseYear: int, optional (default=2005)
        The year of release for the movies to consider.

    ave_rating: float, optional (default=7)
        The minimum average rating for the movies to consider.

    running_time: int, optional (default=120)
        The average running time for the movies to consider.

    Returns:
    --------
    matplotlib figure object:
        A bar plot of the popularity for the movies that meet the given criteria.
    """
    movieList=run_main(releaseYear,ave_rating,running_time)

    xvals = []
    yvals = []

    for movie in movieList:
        xvals.append(movie.title)
        yvals.append(float(movie.popularity))
    
    title = 'Movie popularity graph according to user selection'
    return flask_plot(xvals, yvals, title, 'bar')

def time_trend(releaseYear=2005,ave_rating=7,running_time=120):
    """
    Generates a bar plot of movie running times for movies released in a given year, with a minimum rating and runtime.

    Parameters:
    -----------
    releaseYear: int, optional (default=2005)
        The year of release for the movies to consider.

    ave_rating: float, optional (default=7)
        The minimum average rating for the movies to consider.

    running_time: int, optional (default=120)
        The average running time for the movies to consider.

    Returns:
    --------
    matplotlib figure object:
        A bar plot of the running times for the movies that meet the given criteria.
    """
    movieList=run_main(releaseYear,ave_rating,running_time)

    xvals = []
    yvals = []

    for movie in movieList:
        xvals.append(movie.title)
        yvals.append(int(movie.runtime.split(' ')[0]))
    
    title = 'Movie run time graph according to user selection'
    return flask_plot(xvals, yvals, title, 'bar')



#########################################
############# Flask Web App #############
#########################################

@app.route('/')
def home():
    """
    This function sorts and renders movie data on home page.

    Returns:
    -------
    str:
        Rendered HTML template for home page.
    """
    moviesorted = run_main()
    return render_template('home.html', movielist=moviesorted, param=[2005, 7, 120])

@app.route('/user_input')
def user_input():
    """
    This function renders the input page for users to input their preferences.

    Returns:
    -------
    str:
        Rendered HTML template for input page.
    """
    return render_template('input.html')

@app.route('/home/<releaseY>/<ave_rate>/<running_Time>')
def Rating(releaseY, ave_rate, running_Time):
    """
    This function generates a graph of movie ratings based on user selection.

    Parameters:
    ----------
    releaseY: int
        Year of release for movies to filter.
    ave_rate: float
        Average rating threshold for movies to filter.
    running_Time: int
        Running time threshold for movies to filter.

    Returns:
    -------
    str:
        Rendered HTML template for the graph of movie ratings.
    """
    figure = rating_trend(int(releaseY),float(ave_rate),int(running_Time))
    return render_template('plot.html', figure=Markup(figure))

@app.route('/home/<parameters>')
def Run_Time(parameters):
    """
    This function generates a graph of movie run time based on user selection.

    Parameters:
    ----------
    parameters: str
        User input parameters for movie filtering in the format "[release year, average rating, running time]".

    Returns:
    -------
    str:
        Rendered HTML template for the graph of movie run time.
    """
    x=parameters.split(',')
    param1 = int(x[0].split('[')[1])
    param2= float(x[1])
    param3=int(x[2].split(']')[0])
    figure = time_trend(param1,param2,param3)
    return render_template('plot.html', figure=Markup(figure))

@app.route('/home/<param1>/<param2>')
def Popularity(param1, param2):
    """
    This function generates a graph of movie popularity based on user selection.

    Parameters:
    ----------
    param1: int
        Year of release for movies to filter.
    param2: str
        User input parameters for movie filtering in the format "[average rating, running time]".

    Returns:
    -------
    str:
        Rendered HTML template for the graph of movie popularity.
    """
    x=param2.split(',')
    param2 = float(x[0].split('[')[1])
    param3=int(x[1].split(']')[0])
    figure = popularity_trend(int(param1), param2, param3)
    return render_template('plot.html', figure=Markup(figure))

@app.route('/input/', methods=['POST'])
def process_form():
    """
    This function processes user form input for movie filtering.

    Returns:
    -------
    str:
        Rendered HTML template for home page with filtered movie data.
    """
    release_year = int(request.form['fname'])
    rating_threshold = float(request.form['lname'])
    run_time_threshold = int(request.form['lname2'])
    moviesorted = run_main(release_year, rating_threshold, run_time_threshold)
    return render_template('home.html', movielist=moviesorted, param=[release_year, rating_threshold, run_time_threshold])


@app.route('/summary/<movie_plot>')
def choice_movie_plot(movie_plot):
    """
    Renders a summary page for a selected movie plot.
    
    Parameters
    ----------
    movie_plot : str
        The selected movie plot.
    
    Returns
    -------
    str
        The rendered HTML template for the summary page.
    """
    return render_template('summary.html', movie_plot=movie_plot)

@app.route('/multimedia/backhome')
def redirect():
    """
    Redirects to the home page of the application.

    Returns
    -------
    str
        The rendered HTML template for the home page.
    """
    return render_template('home.html', param=[])

@app.route('/multimedia/<user_selection>/<user_selection_year>/<user_selection_rating>/<user_selection_runtime>')
def multi_media_recommendation(user_selection,user_selection_year,user_selection_rating,user_selection_runtime):
    """
    Renders a multimedia recommendation page based on the user's movie selection, year, rating and runtime.

    Parameters
    ----------
    user_selection : str
        The user's movie selection.
    user_selection_year : str
        The user's selected movie release year.
    user_selection_rating : str
        The user's selected movie rating.
    user_selection_runtime : str
        The user's selected movie runtime.

    Returns
    -------
    str
        The rendered HTML template for the multimedia recommendation page.
    """
    selection_year = int(user_selection_year.split('-')[0])
    selection_rating = float(user_selection_rating)
    selection_runtime = float(user_selection_runtime.split(' ')[0])
    moviesorted = run_main(selection_year, selection_rating, selection_runtime)
    movie_graph = FilmRecommendationSystem().graph_processing(moviesorted)
    user_choose_film = user_selection
    edges = movie_graph.edges([user_choose_film], data=True)
    movieGraphSortedList=[]
    sorted_edges = sorted(edges, key=lambda x: x[2]['weight'], reverse=True)
    for e in sorted_edges:
        movie_graph.nodes[e[1]]['attributes'].similarity=e[2]
        movieGraphSortedList.append(movie_graph.nodes[e[1]]['attributes'])

    # Sort the edges by their weight
    sorted_edges = sorted(edges, key=lambda x: x[2]['weight'], reverse=True)

    # get movie related book info
    url = f"https://www.googleapis.com/books/v1/volumes?q="+user_choose_film
    response = requests.get(url)
    book_data = response.json()
    movie_related_books_info = []
    for i in range(0, len(book_data['items'])):
        try:
            movie_related_books_info.append(Book(Dict=book_data['items'][i]['volumeInfo']))
        except:
            print('There will be less than 10 books recommended')


    # get movie related song info
    movie_related_songs_info = retrieve_song_info(user_choose_film)
    return render_template('multimedia.html', recommended_movie=movieGraphSortedList, recommended_song=movie_related_songs_info, recommended_book=movie_related_books_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
