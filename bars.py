import json
import sys
from math import sqrt


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as open_file:
        return json.load(open_file)


def get_biggest_bar(bars):
    biggest_bar = max(
        bars,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount'],
    )
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(
        bars,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount'],
    )
    return smallest_bar


def calc_distance(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return distance


def get_closest_bar(bars, longitude, latitude):
    nearest_bar = min(
        bars,
        key=lambda restaurant:
        calc_distance(
            longitude,
            latitude,
            restaurant['geometry']['coordinates'][0],
            restaurant['geometry']['coordinates'][1],
        ),
    )
    return nearest_bar


if __name__ == '__main__':
    try:
        user_file_path = sys.argv[1]
        bars = load_data(user_file_path)['features']
        print(
            'Самый большой бар',
            get_biggest_bar(bars)['properties']['Attributes']['Name'],
        )
        print(
            'Самый маленький бар',
            get_smallest_bar(bars)['properties']['Attributes']['Name'],
        )
        custom_coordinates = [float(point) for point in input(
            '\nВведите через пробел '
            'координаты текущего местоположения: \n'
        ).split(' ')]
        user_longitude, user_latitude = custom_coordinates
    except (json.decoder.JSONDecodeError, FileNotFoundError, IndexError):
        exit('Некорректный JSON')
    except (ValueError, TypeError):
        exit('\nНекорректный формат координат.'
             '\nПример корректного ввода: '
             '"37.635709999610896 55.805575000158512" ')
    the_closest_bar = get_closest_bar(
        bars,
        user_longitude,
        user_latitude,
    )['properties']['Attributes']['Name']
    print('Самый близкий бар:', the_closest_bar)
