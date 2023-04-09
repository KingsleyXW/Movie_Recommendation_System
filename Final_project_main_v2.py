import requests
import json

# Movie class to store movie information
class Movie:
    def __init__(self, title="None", id='none', runtime='none',release_date="None", director="None", genre="None", plot="None", rating="None",Dict=None):
        if Dict==None:
            self.title = title
            self.release_date = release_date
            self.director = director
            self.genre = genre
            self.plot = plot
            self.rating = rating
            self.id = id
        else:
            self.title = Dict['title']
            self.year = Dict['release_date']
            self.director = Dict['director']
            self.genre = Dict['genre']
            self.plot = Dict['overview']
            self.rating = Dict['vote_average']
            self.id = Dict['id']
            self.id = Dict['runtime']

# Song class to store song information
class Song:
    '''a standard media subclass that contains many insitance attribute of songs
    such as title, author and release year and so on.

    Instance Attributes
    -------------------
    title: string
        the song title
    author: string
        the author of the song
    release_year: string
        the release year of the song
    url: string
        the url of the song
    album: string
        the album of the song's belonging
    genre: string
        the genre of the song
    track_length: float
        the length of the song
    json: dict
        a dictionary containing all the possible information regarding to the song
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
            if self.json.get("trackName") is not None:
                self.title = self.json['trackName']
            elif self.json.get("collectionName") is not None:
                self.title = self.json['collectionName']
            else:
                self.title = "No Title"
            
            if self.json.get("artistName") is not None:
                self.author = self.json['artistName']
            else:
                self.author = "No Author"
            
            if self.json.get("releaseDate") is not None:
               self.release_date = self.json['releaseDate'].split("-")[0]
            else:
                self.release_date = "No Release Date"

            if self.json.get("trackViewUrl") is not None:
                self.url = self.json['trackViewUrl']
            elif self.json.get("collectionViewUrl") is not None:
                 self.url = self.json['collectionViewUrl']
            else:
                self.url = "No Url"
                
            if self.json.get("collectionName") is not None:
               self.album = self.json['collectionName']
            else:
                self.album = "No Album"
                
            if self.json.get("primaryGenreName") is not None:
                self.genre = self.json['primaryGenreName']
            else:
                self.genre = "No Genre"
                
            if self.json.get("trackTimeMillis") is not None:
                   self.track_length = int(self.json['trackTimeMillis'])
            else:
                self.track_length = 0

# Book class to store book information
class Book:
    def __init__(self, title="None", author="None", genre="None", publication_date="None", plot="None",Dict=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date
        self.plot = plot


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,edgeWeight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], edgeWeight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
    
class Vertex:
      def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        def addNeighbor(self, nbr, edgeWeight=0):
            self.connectedTo[nbr] = edgeWeight
        def getId(self):
            return self.id
        def getWeight(self, nbr):
            return self.connectedTo[nbr]
        def getConnections(self):
            return self.connectedTo.keys()
        def __str__(self):
            #return str(self.id) + 'is connected to ' + str((x.id, x.weight) for x in self.connectedTo)
            return str(self.id) + ' is connected to ' + str([(x, self.connectedTo[x]) for x in self.connectedTo])

def get_Song_list(search):
    '''This function is to generate media object lists given 
    combined search information
    -------------------
    search: string
        the string specifying the Itune API websites and search term
    Returns
    -------
    song_list: list 
        the list contain song objects
    
    '''
    song_list = []
    song_kind = ['album', 'song']

    initial_results = requests.get(search)
    json_output = initial_results.json()
    itunes_list = json_output['results']

    for item in itunes_list:
        if item.get("kind") is not None:
            kind = item['kind']
            if kind in song_kind:
                S = Song(json=item)
                song_list.append(S)

    total_song_list = song_list 
    return total_song_list

def calculate_similarity(movie1, movie2, weights):
    similarity = 0
    for prop in weights:
        if prop in movie1 and prop in movie2:
            similarity += movie1[prop] * movie2[prop] * weights[prop]
    return similarity

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



# Film Recommendation System class
class FilmRecommendationSystem:
    def __init__(self, Director_weights=0.3, Genre_weights=0.2, Ratings_weights=0.35, Runtime_weights=0.05, Country_weights=0.1):
        self.movies_cache = {} # Cache to store movie data
        self.weights = { # Pre-defined weights for movie properties
            "Director": Director_weights,
            "Genre": Genre_weights,
            "Type": Ratings_weights,
            "runtime": Runtime_weights,
            "country": Country_weights
            # Add more properties and weights as needed
        }

    # Method to retrieve movie details from Open Movie Database API
    def get_movie_details(self, movie_title):
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=4a0cb4ab"
        response = requests.get(url)
        movie_data = response.json()
        return movie_data

    # Method to recommend movies based on user input
    def recommend_movies(self, user_input):
        movies = []
        if user_input["year_period"] in self.movies_cache:
            movies = self.movies_cache[user_input["year_period"]]
        else:
            url = f"http://www.omdbapi.com/?s=&apikey=4a0cb4ab"
            response = requests.get(url)
            movies_data = response.json()
            if "Search" in movies_data:
                movies = movies_data["Search"]
                for movie in movies:
                    movie_data = self.get_movie_details(movie["Title"])
                    movie.update(movie_data)
                self.movies_cache[user_input["year_period"]] = movies

        # Recommend movies based on user input and weights
        recommended_movies = []
        for movie in movies:
            relevance_score = (
                self.weights["Director"] * (movie["Director"] == user_input["director"]) +
                self.weights["Genre"] * (movie["Genre"] == user_input["genre"]) +
                self.weights["Type"] * (movie["Type"] == user_input["type"]) +
                self.weights["Plot"] * (movie["Plot"] == user_input["plot"])
                # Add more relevance scores based on other movie properties as needed
            )
            if relevance_score > 0:
                recommended_movies.append(movie)
        recommended_movies.sort(key=lambda x: x["imdbRating"], reverse=True) # Sort movies by rating
        return recommended_movies

    # Method to recommend songs based on movie information
    def recommend_songs(self, movie):
        # Retrieve songs based on movie title using iTunes API
        url = f"https://itunes.apple.com/search?term={movie}&media=music"
        response = requests.get(url)
        songs_data = response.json()

        songs = []
        if "results" in songs_data:
            songs = songs_data["results"]

        # Create Song objects for each retrieved song
        recommended_songs = []
        for song_data in songs:
            song = Song(
                title=song_data["trackName"],
                artist=song_data["artistName"],
                genre=song_data["primaryGenreName"],
                album=song_data["collectionName"],
                release_date=song_data["releaseDate"]
            )
            recommended_songs.append(song)

        return recommended_songs

    # Method to recommend books based on movie information
    def recommend_books(self, movie):
        # Check if book information is already cached
        if movie.title in self.books_cache:
            print("Fetching book information from cache...")
            return self.books_cache[movie.title]
        else:
            # Retrieve relevant information from Google Books API based on movie information
            query = f"{movie.title} {movie.director} {movie.year} book"
            books = self.google_books_api.search_books(query)

            # Placeholder for recommended books
            recommended_books = []

            # Extract relevant information from books data and create Book objects
            for book_data in books:
                title = book_data.get('title', '')
                author = book_data.get('author', '')
                genre = book_data.get('genre', '')
                plot = book_data.get('plot', '')

                book = Book(title, author, genre, plot)
                recommended_books.append(book)

            # Cache the recommended books
            self.books_cache[movie.title] = recommended_books

            return recommended_books
    
        # Main function to interact with the Film Recommendation System
    def main(self):
    # Construct the API request URL
        release_year = 2006
        rating_threshold = 7
        time_length =120
        time_min = int(time_length) - 5
        time_max = int(time_length) + 5
        API_KEY="b6b67d5a0231de406a62568976194959"
        MovieList = []
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
                        print(data['results'])

        print(MovieList)
        print(len(MovieList))
        
        for movie in MovieList:
            movie_title = movie['title']
            if 'director' in list(movie.keys()) and 'runtime' in list(movie.keys()) and \
            'runtime' in list(movie.keys()) and 'genre' in list(movie.keys()):
                continue
            else:
                url = f"http://www.omdbapi.com/?t={movie_title}&apikey=4a0cb4ab" 
                response = requests.get(url)
                detailed_data = response.json()
                print(detailed_data,movie_title)
                if list(detailed_data.keys())[1]!='Error':
                    movie['director'] = detailed_data['Director']
                    movie['runtime'] = detailed_data['Runtime']
                    movie['country'] = detailed_data['Country'].split(',')
                    movie['genre'] = detailed_data['Genre'].split(',')
                else:
                    movie['director'] = 'Unknown'
                    movie['runtime'] = 'Unknown'
                    movie['country'] = 'Unknown'
                    movie['genre'] = 'Unknown'
                    
        write_json('./json_cache_'+str(release_year)+'.json', MovieList)
    '''
            while True:
                
                print("Welcome to Film Recommendation System!")

                choice = input("Enter your choice: ")

        
                # Implement logic to input user parameters for movie recommendation
                # ...
                parameters = {}  # Placeholder for user input parameters
                recommended_movies = self.recommend_movies(parameters)
                # Display recommended movies to the user
                print("Recommended Movies:")
                for movie in recommended_movies:
                    print(movie.title)

                    base_url = 'https://itunes.apple.com/search?term=search_term'
                    total_media_list = []
                    url = f"https://www.googleapis.com/books/v1/volumes?q=search_term"
                    response = requests.get(url)
                    book_data = response.json()
                    print(len(book_data['items']))
                    print(book_data)
                    
                    while True:
                        if len(total_media_list) == 0:
                            search = input("Enter a search term, or 'exit' to quit:")
                            if search == "exit":
                                print("Bye!")
                                break
                            song_list = get_result_list(base_url+search)
                            output_format(song_list)
                        

if __name__ == "__main__":
    # Initialize Film Recommendation System with iTunes API key
    film_recommendation_system = FilmRecommendationSystem(Director_weights=0.2, Genre_weights=0.1, Type_weights=0.15, Plot_weights=0.3)

    # Call the main function to start interacting with the system
    film_recommendation_system.main()
        
    '''