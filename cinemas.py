import requests
from bs4 import BeautifulSoup
import collections


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    page_elements = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    dict_movies_and_places_amount = {element.find('div', {'class': 'm-disp-table'}).find('a').text:
                                     len(element.find_all('tr'))
                                     for element in page_elements}
    return dict_movies_and_places_amount


def get_only_popular_movie_titles(dict_movies_places, min_places_amount=30):
    only_popular_names_list = [movie for movie, places in dict_movies_places.items() if int(places) > min_places_amount]
    return only_popular_names_list


def make_dict_name_rating(movies_names_list):
    names_rating_votes_dict = {movie_name:parse_movie_info(get_page_html(fetch_kinopoisk_movie_url(movie_name)))
                               for movie_name in movies_names_list}
    return names_rating_votes_dict


def fetch_kinopoisk_movie_url(movie_name):
    url = 'https://plus.kinopoisk.ru/search/'
    params = {
        'text': movie_name
    }
    search_page_html = get_page_html(url, params)
    soup = BeautifulSoup(search_page_html, 'html.parser')
    movie_url = soup.find('a', 'link  film-snippet__media-content').attrs['href']
    return movie_url


def get_page_html(url, params=None):
    return requests.get(url, params).text


def parse_movie_info(search_movie_html):
    try:
        soup = BeautifulSoup(search_movie_html, 'html.parser')
        rating = soup.find('div', 'rating-button__rating').text
        votes = soup.find('div', 'film-header__rating-comment').text
        movie_info_template = collections.namedtuple('Movies', ['Rating', 'Votes'])
        movie_info = [float(rating), votes]
        dict_movie_info = dict(movie_info_template._make(movie_info)._asdict())
        return dict_movie_info
    except:
        return {'Rating': 0,
                'Votes': 0}


def make_top_list(name_rating_dict, results_amount):
    name_rating_list = list(name_rating_dict.items())
    rating = [(movie[0], movie[1]['Rating'], movie[1]['Votes']) for movie in name_rating_list]
    return sorted(rating, key=lambda movie: movie[1], reverse=True)[0: results_amount]


def output_to_console(sorted_movie_list):
    for movie in sorted_movie_list:
        print('У фильма %s рейтинг %s (%s)' % (movie[0], movie[1], movie[2]))


if __name__ == '__main__':
    afisha_url = 'http://www.afisha.ru/msk/schedule_cinema/'
    top_list_amount = 10
    raw_afisha_html = get_page_html(afisha_url)
    list_movie_and_places_amount = (parse_afisha_list(raw_afisha_html))
    only_popular_titles_list = get_only_popular_movie_titles(list_movie_and_places_amount)
    dict_name_rating = make_dict_name_rating(only_popular_titles_list)
    top10_list = make_top_list(dict_name_rating, top_list_amount)
    output_to_console(top10_list)
