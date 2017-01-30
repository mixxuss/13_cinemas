import requests
from bs4 import BeautifulSoup
import time

def fetch_afisha_page():
    html = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    html_page = html.text
    return html_page


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    page_elements = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    list_movies_and_places_amount = []
    for element in page_elements:
        tuple_movie_places = (element.find('div', {'class': 'm-disp-table'}).find('a').text,
                              len(element.find_all('tr')))
        list_movies_and_places_amount.append(tuple_movie_places)
    return list_movies_and_places_amount


def get_only_popular_movie_titles(list_movies):
    only_popular_names_list = [movie[0] for movie in list_movies if int(movie[1]) > 10]
    return only_popular_names_list


def make_dict_name_rating(movie_names_list, timeout=6):
    names_rating_votes_dict = {}
    for movie_name in movie_names_list:
        names_rating_votes_dict[movie_name] = fetch_movie_info(movie_name)
        time.sleep(timeout)
    return names_rating_votes_dict


def fetch_movie_info(movie_name):
    url = 'https://www.kinopoisk.ru/index.php'
    headers = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    params = {
        'first': 'no',
        'what': '',
        'kp_query': movie_name
    }
    cookies = {'user_country': 'ru',
               'yandex_gid': '10758',
               'mobile': 'no',
               'PHPSESSID': '7b74661247009b38f33dee4bfad99827',
               'last_visit': '2017-01-29+19%3A47%3A43'}
    try:
        session = requests.Session()
        response = session.get(url, params=params, headers=headers, cookies=cookies)
        search_movie_html = response.text
        soup = BeautifulSoup(search_movie_html, 'html.parser')
        element_most_wanted = soup.find_all('div', 'element most_wanted')[0]
        rating_and_votes_amount_list = element_most_wanted.find_all('div',
                                                                    'rating ratingGreenBG')[0].attrs['title'].split(' ')
        tuple_rating_and_votes_amount = list_strings_to_tuple(rating_and_votes_amount_list)
        return tuple_rating_and_votes_amount
    except:
        return (0, 0)


def list_strings_to_tuple(list_rating):
    tuple_rating = (float(list_rating[0]), int(list_rating[1].replace('(', '').replace(')', '')))
    return tuple_rating


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
    raw_afisha_html = fetch_afisha_page()
    list_movie_and_places_amount = (parse_afisha_list(raw_afisha_html))
    only_popular_titles_list = get_only_popular_movie_titles(list_movie_and_places_amount)
    print(only_popular_titles_list)
    #dict_name_rating = make_dict_name_rating(only_popular_titles_list)
    #top10_list = make_top_list(dict_name_rating, top_list_amount)
    #output_to_console(top10_list)
