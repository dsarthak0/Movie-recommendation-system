import streamlit as st
import pickle
import pandas as pd
import os

# Load environment variables from the .env file
# (Make sure the dotenv and API key part is correct for your use case, but it's not used in this version)
# load_dotenv()  # Load environment variables
# api_key = os.getenv("TMDB_API_KEY")  # Fetch the API key from .env

# Set the TMDb API endpoint
TMDB_HOST = "themoviedb.p.rapidapi.com"


@st.cache_data
def load_data():
    """Load movie data and similarity matrix from pickle files."""
    try:
        movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError as e:
        st.error("Required data files are missing. Please ensure `movie_dict.pkl` and `similarity.pkl` are available.")
        st.stop()


def recommend(movie):
    """Recommend movies based on similarity matrix."""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)

        return recommended_movies
    except IndexError:
        st.error(f"Could not find recommendations for the movie: {movie}")
        return []


# Load movie data and similarity matrix
movies, similarity = load_data()

# Streamlit App
st.title('Movie Recommendation System')

# Select a movie from the list
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# When the "Recommend" button is pressed
if st.button('Recommend'):
    names = recommend(selected_movie_name)

    if names:
        # Display recommended movies
        st.write("Recommended Movies:")
        for name in names:
            st.text(name)
    else:
        st.error("No recommendations available.")






