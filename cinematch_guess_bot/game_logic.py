import json
import random

import requests


def generate_random_dates():
    start_release_year = 2000
    end_release_year = 2020

    start_date = random.randint(start_release_year, end_release_year)
    end_date = random.randint(start_date, end_release_year)

    return start_date, end_date


def generate_random_genre():
    genres = ["драма", "боевик", "ужасы", "триллер", "детектив", "криминал", "семейный"]

    genre = random.choice(genres)

    return genre


def api_request():
    url = "https://localhost:7036/api/Movie/getMovies"

    start_release_year, end_release_year = generate_random_dates()
    genre = generate_random_genre(

    )

    params = {
        "startReleaseYear": start_release_year,
        "endReleaseYear": end_release_year,
        "genres": genre,
    }

    try:
        response = requests.get(url, params=params, verify=False)

        if response.status_code == 200:
            movie_data = json.loads(response.text)

            random_movie = random.choice(movie_data)

            print(f"Рандомный фильм: {random_movie}")
            return random_movie
        else:
            print(f"Ошибка при запросе. Статус код: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


api_request()
