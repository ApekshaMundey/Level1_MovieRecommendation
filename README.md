# 🎬 Movie Recommendation System

A content-based movie recommendation system built using **Streamlit** and **TMDB API**.  
It recommends movies similar to a selected title and displays detailed information such as overview, cast, trailer, and similar movies.

---

## 🚀 Features

- 🔍 Search movies with autocomplete
- 🎯 Content-based recommendations
- 🔥 Trending movies (TMDB)
- 🎬 Detailed movie view
  - Poster
  - Overview
  - Cast
  - Rating, runtime, release date
  - YouTube trailer
- ❤️ Watchlist using session state
- ⚡ Optimized API calls with caching
- ☁️ Deployed on Streamlit Cloud

---

## 🧠 Methodology

1. Movie metadata is preprocessed and stored in a structured dataset (movies.pkl) for efficient access.
2. Text-based features are vectorized and cosine similarity is computed between movies.
3. A similarity matrix (similarity.pkl) is generated and stored to avoid runtime computation.
4. A content-based filtering approach is used to recommend movies similar to the selected one.
5. TMDB APIs are integrated to fetch real-time movie details such as posters, cast, and trailers.
6. Streamlit is used to build the interactive user interface and handle user interactions.
7. Session state and caching are applied to optimize performance and manage application state.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **ML:** Cosine similarity
- **API:** TMDB (The Movie Database)
- **Deployment:** Streamlit Cloud

---

## 📂 Project Structure
```
LEVEL1_MovieRecommendation/
│
├── app.py  #Streamlit UI for recommending movies
│
├── movies.pkl #Contains metadata about the movies
|
├── similarity.pkl #Pre-computed similarity matrix which represents cosine similarity between two movies
│
├── requirements.txt
├── README.md
```

---

## 🔑 TMDB API Key Setup

1. Create an account on https://www.themoviedb.org/
2. Generate an API key
3. In Streamlit Cloud:
   - Go to **App → Settings → Secrets**
   - Add:

  ```toml
  TMDB_API_KEY = "your_api_key_here"
4. In app.py, access it using:
  TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

---  

## Application Workflow

1. The Streamlit app initializes, loads configuration, cached datasets (movies.pkl, similarity.pkl), and session state variables.
2. The user selects a movie via search or trending movies, and the selected movie ID is stored in session state.
3. The recommendation engine retrieves cosine similarity scores and identifies the top 5 similar movies.
4. Movie details, cast, trailer, and similar movies are fetched from the TMDB API with a loading spinner.
5. The application displays the movie poster, overview, ratings, cast, trailer link, and recommendations.
6. Users can add or remove movies from the watchlist, which is managed using session state.

---

### ▶️ Run Locally
pip install -r requirements.txt
streamlit run app.py

### 🌐 Live Demo
🔗 App URL: https://level1movierecommendation-3q6xdanjzt2ektcrf9vbak.streamlit.app/

---

## 📌 Future Improvements

- User authentication
- Collaborative filtering
- Genre-based recommendations
- Database-backed watchlist  
---

## 👩‍💻 Author

**Apeksha**
Machine Learning and Python enthusiast

---

## 📜 License

This project is intended for **educational and academic purposes**.



