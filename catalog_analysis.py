import math

movies = [
    {"title": "The Dune Chronicles", "year": 2021, "genres": {"sci-fi", "drama"},
     "rating": 8.6, "duration_min": 155, "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]}, # noqa: E501
    {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
     "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
    {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
     "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
    {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
     "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
    {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
     "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
    {"title": "midnight in oslo", "year": 2020, "genres": {"thriller", "mystery"},
     "rating": 8.9, "duration_min": 124, "actors": ["K. Lee", "R. Ferguson"]},
    {"title": "Garden of Static", "year": 2022, "genres": {"drama"},
     "rating": 4.8, "duration_min": 137, "actors": ["P. Diaz", "J. Bloom"]},
    {"title": "The Quiet Algorithm", "year": 2024, "genres": {"sci-fi", "drama"},
     "rating": 9.2, "duration_min": 118, "actors": ["M. Ferguson", "O. Isaac"]},
    {"title": "Two Left Shoes", "year": 2011, "genres": {"comedy"},
     "rating": 6.0, "duration_min": 95, "actors": ["A. Novak", "K. Lee"]},
    {"title": "Red Harbor", "year": 2018, "genres": {"action", "thriller"},
     "rating": 7.3, "duration_min": 129, "actors": ["P. Diaz", "T. Chalamet"]},
]


def average_rating(movies):
    total_rating = 0
    for movie in movies:
        total_rating += movie["rating"]
    return round(total_rating / len(movies), 1)


def catalog_age_stats(movies, current_year=2026):
    ages = [current_year - movie["year"] for movie in movies]
    oldest = max(ages)
    newest = min(ages)
    avg_age = math.ceil(sum(ages) / len(ages))
    return (oldest, newest, avg_age)


def duration_in_hours(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}ч {remaining_minutes}м"


def rating_tier(rating):
    if rating >= 9:
        return "шедевр"
    elif rating >= 7:
        return "хорошо"
    else:
        return "слабо" if rating < 5 else "средне"

def decade_label(year):
    match year:
        case _ if year > 2020:
            return "новые"
        case _ if 2015 <= year <= 2020:
            return "недавние"
        case _:
            return "старые"


def count_long_movies(movies, threshold=120):
    count = 0
    for movie in movies:
        if movie['duration_min'] > threshold:
            count += 1
    return count


def normalize_title(title):
    words = title.split()
    final = ''
    for word in words:
        final += word[0].upper() + word[1:] + ' '
    return final.rstrip()

def make_slug(title):
    return title.lower().replace(" ", "-")


def format_report_line(movie):
    title = normalize_title(movie["title"])
    year = movie["year"]
    rating = movie["rating"]
    duration = duration_in_hours(movie["duration_min"])
    genres = ", ".join(sorted(movie["genres"]))
    return f'"{title}" ({year}) — {rating}/10, {duration}, жанры: {genres}'


def titles_sorted_by_rating(movies):
    sorted_movies = sorted(
        movies,
        key=lambda movie: movie["rating"],
        reverse=True,
    )
    return [movie["title"] for movie in sorted_movies]


def top_n_by_rating(movies, n=3):
    sorted_movies = sorted(
        movies,
        key=lambda movie: movie["rating"],
        reverse=True,
    )
    return [(movie["title"], movie["rating"]) for movie in sorted_movies][:n]


def count_by_genre(movies):
    final_genres = {}
    for movie in movies:
        for genre in movie["genres"]:
            final_genres[genre] = final_genres.get(genre, 0) + 1
    return final_genres


def actor_filmography(movies):
    final_actors = {}
    for movie in movies:
        for actor in movie["actors"]:
            films = final_actors.get(actor, [])
            films.append(movie["title"])
            final_actors[actor] = films
    return final_actors


def all_genres(movies):
    genres = set()
    for movie in movies:
        genres |= movie["genres"]
    return genres


def common_actors(movie1, movie2):
    return set(movie1["actors"]) & set(movie2["actors"])


def genres_only_in_one(movies_a, movies_b):
    genres_a = set()
    for movie in movies_a:
        genres_a |= movie["genres"]
    genres_b = set()
    for movie in movies_b:
        genres_b |= movie["genres"]
    return genres_a - genres_b


def iter_high_rated(movies, min_rating=8.0):
    for movie in movies:
        if movie["rating"] >= min_rating:
            yield movie


def build_report(movies):
    avg_rating = average_rating(movies)
    _, _, avg_age = catalog_age_stats(movies)

    print("ОТЧЕТ ПО КАТАЛОГУ")
    print(f"Средний рейтинг: {avg_rating}")
    print(f"Средний возраст фильмов: {avg_age} лет")
    print()

    print("Топ-3 фильма:")
    movies_by_title = {movie["title"]: movie for movie in movies}
    for title, _rating in top_n_by_rating(movies, 3):
        print(f"  {format_report_line(movies_by_title[title])}")
    print()

    print("Фильмов по жанрам:")
    sorted_genres = sorted(
        count_by_genre(movies).items(),
        key=lambda item: item[1],
        reverse=True,
    )
    for genre, count in sorted_genres:
        print(f"  {genre} — {count}")
    print()

    print(f"Все жанры каталога: {', '.join(sorted(all_genres(movies)))}")


if __name__ == "__main__":
    for movie in movies:
        if "comedy" in movie["genres"]:
            continue
        print(movie["title"])

    i = 0
    while i < len(movies):
        if movies[i]["rating"] > 9.0:
            print(movies[i]["title"])
            break
        i += 1
    else:
        print("Шедевров не найдено")

    catalog_without_masterpieces = [m for m in movies if m["rating"] <= 9.0]
    i = 0
    while i < len(catalog_without_masterpieces):
        if catalog_without_masterpieces[i]["rating"] > 9.0:
            print(catalog_without_masterpieces[i]["title"])
            break
        i += 1
    else:
        print("Шедевров не найдено")

    avg_rating = average_rating(movies)
    title_rating = {
        movie["title"]: movie["rating"]
        for movie in movies
        if movie["rating"] > avg_rating
    }

    for movie in iter_high_rated(movies):
        print(format_report_line(movie))

    print(sum(m["duration_min"] for m in movies if m["rating"] > 7))

    build_report(movies)
