import json
import sys


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as open_file:
        return json.load(open_file)


def get_biggest_bar(data_for_restaurants):
    biggest_bar = max(
        data_for_restaurants,
        key=lambda seats_count:
        seats_count['properties']['Attributes']['SeatsCount'],
    )
    return biggest_bar


def get_smallest_bar(data_for_restaurants):
    smallest_bar = min(
        data_for_restaurants,
        key=lambda seats_count:
        seats_count['properties']['Attributes']['SeatsCount'],
    )
    return smallest_bar


def calc_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2) + ((y2 - y1) ** 2) ** 0.5
    return distance


def get_closest_bar(data_for_restaurants, longitude, latitude):
    nearest_bar = min(
        data_for_restaurants,
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
        if len(sys.argv) == 1:
            user_file_path = input('Укажите путь до файла: ')
        else:
            user_file_path = sys.argv[1]
        try:
            list_of_restaurants = load_data(user_file_path)['features']
        except json.decoder.JSONDecodeError as e:
            print('Некорректный JSON')
            raise SystemExit(1)
        print(
            'Самый большой бар',
            get_biggest_bar(list_of_restaurants)
            ['properties']['Attributes']['Name'],
        )
        print(
            'Самый маленький бар',
            get_smallest_bar(list_of_restaurants)
            ['properties']['Attributes']['Name'],
        )
        try:
            user_longitude, user_latitude = [float(point) for point in input(
                '\nВведите через пробел '
                'координаты текущего местоположения: \n'
            ).split(' ')]

        except (ValueError, TypeError) as e:
            print('\nНекорректный формат координат.'
                  '\nПример корректного ввода: '
                  '"37.635709999610896 55.805575000158512" ')
            raise SystemExit(1)
        print('Самый близкий бар:', str(get_closest_bar(
                                            list_of_restaurants,
                                            float(user_longitude),
                                            float(user_latitude),
                                        )['properties']['Attributes']['Name']))
    except FileNotFoundError as e:
        print('Файла не существует')
