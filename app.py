from flask import Flask, render_template, request
import requests
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

# 'API_KEY'  TMDb API key
TMDB_API_KEY = '830c0f3285681fbcec21181de020b20c'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
app.config['SECRET_KEY'] = 'sHANMUKX'

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = SearchForm()
    movies = None
    if form.validate_on_submit():
        movies = search_tmdb(form.query.data)
    return render_template('query.html', form=form, movies=movies)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    if not query:
        return render_template('index.html', error='Please enter a search query.')

    search_url = f'{TMDB_BASE_URL}/search/movie'
    params = {'api_key': TMDB_API_KEY, 'query': query}
    
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        movies = data.get('results', [])
        return render_template('index.html', movies=movies)
    except Exception as e:
        return render_template('index.html', error=f'Error: {str(e)}')

def search_tmdb(query):
    api_key = '830c0f3285681fbcec21181de020b20c'
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': query}
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    movies = []
    for result in data.get('results', []):
        poster_path = result.get('poster_path')
        if poster_path:
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
        else:
            poster_url = 'https://via.placeholder.com/150'

        movie_info = {
            'title': result.get('title'),
            'release_date': result.get('release_date'),
            'overview': result.get('overview'),
            'poster_url': poster_url,
        }
        movies.append(movie_info)

    return movies

if __name__ == '__main__':
    app.run(debug=True)
