import requests
from bs4 import BeautifulSoup
import time
import collections


def fetch_afisha_page():
    html = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    html_page = html.text
    return html_page


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
    names_rating_votes_dict = {}
    for movie_name in movies_names_list:
        names_rating_votes_dict[movie_name] = fetch_movie_info(fetch_new_kinopoisk_page(fetch_kinopoisk_movie_url(movie_name)))
    return names_rating_votes_dict


def fetch_kinopoisk_movie_url(movie_name):
    url = 'https://plus.kinopoisk.ru/search/'
    params = {
        'text': movie_name
    }
    response = requests.get(url, params)
    search_page_html = response.text
    soup = BeautifulSoup(search_page_html, 'html.parser')
    movie_url = soup.find('a', 'link  film-snippet__media-content').attrs['href']
    return movie_url


def fetch_new_kinopoisk_page(url):
    movie_page_html = requests.get(url).text
    return movie_page_html


def fetch_movie_info(search_movie_html):
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
    sorted_list = [(movie, name_rating_dict[movie]) for movie in sorted(name_rating_dict,
                                                                        key=name_rating_dict.get, reverse=True)]
    if results_amount > len(sorted_list):
        return sorted_list[0:len(sorted_list)]
    return sorted_list[0:int(results_amount)-1]


def output_to_console(sorted_movie_list):
    for movie in sorted_movie_list:
        print('Movie %s had %s average rating (%s votes)' % (movie[0], movie[1][0], movie[1][1]))


if __name__ == '__main__':
    top_list_amount = 10
    # print(fetch_kinopoisk_movie_url('Балерина'))
    # print(fetch_movie_info(fetch_new_kinopoisk_page(fetch_kinopoisk_movie_url('Балерина'))))
    raw_afisha_html = fetch_afisha_page()
    list_movie_and_places_amount = (parse_afisha_list(raw_afisha_html))
    only_popular_titles_list = get_only_popular_movie_titles(list_movie_and_places_amount)
    dict_name_rating = make_dict_name_rating(only_popular_titles_list)
    print(dict_name_rating)
    #top10_list = make_top_list(dict_name_rating, top_list_amount)
    #output_to_console(top10_list)
