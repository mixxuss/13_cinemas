import requests
from bs4 import BeautifulSoup

def fetch_afisha_page():
    html = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    html_page = html.text
    return html_page


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    page_elements = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    list_movies = []
    for element in page_elements:
        tuple_movie_places = (element.find('div', {'class': 'm-disp-table'}).find('a').text,
                              len(element.find_all('tr')))
        list_movies.append(tuple_movie_places)
    return list_movies


def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    # raw_html = fetch_afisha_page()
    # list_movie_places = (parse_afisha_list(raw_html))
    kinopoisk_page = requests.get('https://www.kinopoisk.ru/s/type/all/find/Балерина')#, 'Балерина')
    html = kinopoisk_page.text
    #ele = html.find('div', {'class': 'rating'})
    print(html)#.find('div', {'class': 'element most_wanted'}))







    # movie_list = Movie.objects.search('Балерина')
    # print(movie_list[0].title)
    # print(movie_list[0].id)
    # movie = Movie(movie_list[0].id)
    # movie.get_content('main_page')
    # print(movie)







    # soup = BeautifulSoup(html_page, 'html.parser')
    # elements = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    # print(elements)
    # for element in elements:
    #    print(element.find('div', {'class': 'm-disp-table'}).find('a').text)
    #    print(len(element.find_all('tr')))
