from flask import Flask, render_template, request, jsonify
import requests
import os
app = Flask(__name__)
api_key = os.getenv('api_key')
def get_actor_id(actor_name, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/search/person",
                            params={"api_key": api_key, "query": actor_name})
    data = response.json()
    return data['results'][0]['id'] if data['results'] else None

def get_actor_movie_credits(actor_id, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits",
                            params={"api_key": api_key})
    movies = response.json()['cast']
    for movie in movies:
        movie['rating'] = get_movie_rating(movie['id'], api_key)
    return movies

def get_actor_tv_credits(actor_id, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/person/{actor_id}/tv_credits",
                            params={"api_key": api_key})
    tv_shows = response.json()['cast']
    for show in tv_shows:
        show['rating'] = get_tv_show_rating(show['id'], api_key)
    return tv_shows

def get_movie_rating(movie_id, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}",
                            params={"api_key": api_key})
    data = response.json()
    return data.get('vote_average', 'N/A')

def get_tv_show_rating(tv_show_id, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/tv/{tv_show_id}",
                            params={"api_key": api_key})
    data = response.json()
    return data.get('vote_average', 'N/A')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        actor_name = request.form.get('actor_name')
        actor_id = get_actor_id(actor_name, api_key)

        if actor_id:
            movies = get_actor_movie_credits(actor_id, api_key)
            tv_shows = get_actor_tv_credits(actor_id, api_key)
            return render_template('results.html', actor_name=actor_name, movies=movies, tv_shows=tv_shows)
        else:
            return jsonify({"error": "Actor not found"})

    return render_template('index.html')

if __name__ == '__main__':
    
    app.run(debug=True)
