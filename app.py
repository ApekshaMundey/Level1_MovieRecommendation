import streamlit as st
import pickle
import requests
import time

# ---------------- CONFIG ----------------
TMDB_API_KEY = "8fd21cc1330345d94b2a3c31c45898ff"

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()
movie_list = sorted(movies['title'].values)

# ---------------- SESSION STATE ----------------
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

if "favorites" not in st.session_state:
    st.session_state.favorites = {}  # {movie_id: title}

if "movie_cache" not in st.session_state:
    st.session_state.movie_cache = {}  # {movie_id: {details, cast, trailer, similar}}

# ---------------- SAFE REQUEST ----------------
def safe_get(url, params=None, retries=3):
    for _ in range(retries):
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException:
            time.sleep(1)
    return {}

# ---------------- TMDB FUNCTIONS ----------------
def fetch_movie_bundle(movie_id):
    return {
        "details": safe_get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            {"api_key": TMDB_API_KEY, "language": "en-US"}
        ),
        "cast": [
            c["name"]
            for c in safe_get(
                f"https://api.themoviedb.org/3/movie/{movie_id}/credits",
                {"api_key": TMDB_API_KEY}
            ).get("cast", [])[:5]
        ],
        "trailer": next(
            (
                f"https://youtube.com/watch?v={v['key']}"
                for v in safe_get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}/videos",
                    {"api_key": TMDB_API_KEY}
                ).get("results", [])
                if v.get("type") == "Trailer" and v.get("site") == "YouTube"
            ),
            None
        ),
        "similar": safe_get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/similar",
            {"api_key": TMDB_API_KEY}
        ).get("results", [])[:6]
    }

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_trending():
    return safe_get(
        "https://api.themoviedb.org/3/trending/movie/week",
        {"api_key": TMDB_API_KEY}
    ).get("results", [])

# ---------------- HELPERS ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return (
        [movies.iloc[i[0]].title for i in movie_indices],
        [movies.iloc[i[0]].movie_id for i in movie_indices]
    )

def format_runtime(minutes):
    if not minutes:
        return "N/A"
    return f"{minutes//60}h {minutes%60}m"

def genre_chips(genres):
    st.markdown(
        "".join(
            f"""
            <span style="
                background:#262730;
                padding:6px 12px;
                border-radius:20px;
                margin-right:8px;
                font-size:13px;
                color:#e5e7eb;
                display:inline-block;
            ">
            {g['name']}
            </span>
            """ for g in genres
        ),
        unsafe_allow_html=True
    )

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8;'>Start typing a movie name</p>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 3, 1])
with mid:
    selected_movie = st.selectbox("Search movie", movie_list, index=None)

# ---------------- SIDEBAR ----------------
st.sidebar.subheader("❤️ Watchlist")
if st.session_state.favorites:
    for title in st.session_state.favorites.values():
        st.sidebar.write("🎬", title)
else:
    st.sidebar.caption("No movies added yet")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2, 4])

# ---------- LEFT ----------
with left:
    if selected_movie:
        st.subheader("🎯 Recommended Movies")
        names, ids = recommend(selected_movie)
        for n, i in zip(names, ids):
            if st.button(n, key=f"rec_{i}", use_container_width=True):
                st.session_state.selected_movie_id = i
    else:
        st.subheader("🔥 Trending Movies")
        with st.spinner("🔥 Loading trending movies..."):
            trending = fetch_trending()
        for m in trending[:8]:
            if st.button(m["title"], key=f"trend_{m['id']}", use_container_width=True):
                st.session_state.selected_movie_id = m["id"]

# ---------- RIGHT ----------
with right:
    movie_id = st.session_state.selected_movie_id
    if movie_id:

        if movie_id not in st.session_state.movie_cache:
            with st.spinner("🎬 Fetching movie details..."):
                st.session_state.movie_cache[movie_id] = fetch_movie_bundle(movie_id)

        data = st.session_state.movie_cache[movie_id]
        details = data["details"]

        title = details.get("title", "Unknown Movie")
        st.subheader(f"🎬 {title}")

        col1, col2 = st.columns([1, 2])

        with col1:
            if details.get("poster_path"):
                st.image("https://image.tmdb.org/t/p/w500" + details["poster_path"], width=260)

            if data["trailer"]:
                st.link_button("▶ Watch Trailer", data["trailer"])

            if movie_id in st.session_state.favorites:
                if st.button("💔 Remove from Watchlist"):
                    del st.session_state.favorites[movie_id]
            else:
                if st.button("❤️ Add to Watchlist"):
                    st.session_state.favorites[movie_id] = title

        with col2:
            genre_chips(details.get("genres", []))
            st.markdown("### 📖 Overview")
            st.write(details.get("overview", "No overview available."))
            st.markdown("### 🎭 Cast")
            st.write(", ".join(data["cast"]) or "Cast unavailable")
            st.markdown("### ℹ️ Details")
            st.write(f"⭐ Rating: {details.get('vote_average','N/A')}")
            st.write(f"📅 Release: {details.get('release_date','N/A')}")
            st.write(f"⏱ Runtime: {format_runtime(details.get('runtime'))}")

        if data["similar"]:
            st.markdown("### 🎥 Similar Movies")
            cols = st.columns(len(data["similar"]))
            for i, m in enumerate(data["similar"]):
                with cols[i]:
                    if st.button(m["title"], key=f"sim_{m['id']}"):
                        st.session_state.selected_movie_id = m["id"]
