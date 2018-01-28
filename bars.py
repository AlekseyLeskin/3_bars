import json
import sys


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as open_file:
        return json.load(open_file)


def get_biggest_bar(data):
    biggest_bar = max(data['features'], key=lambda seats_count: seats_count['properties']['Attributes']['SeatsCount'])
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(data):
    smallest_bar = min(data['features'], key=lambda seats_count: seats_count['properties']['Attributes']['SeatsCount'])
    return smallest_bar['properties']['Attributes']['Name']


def calc_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2) + ((y2 - y1) ** 2) ** 0.5


def get_closest_bar(data, longitude, latitude):
    nearest_bar = min(data['features'], key=lambda restaurant: calc_distance(longitude,
                                                                             latitude,
                                                                             restaurant['geometry']['coordinates'][0],
                                                                             restaurant['geometry']['coordinates'][1]))
    return nearest_bar['properties']['Attributes']['Name']


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            user_file_path = input('Укажите путь до файла: ')
        else:
            user_file_path = sys.argv[1]
        file_data = load_data(user_file_path)
        print('Самый большой бар', get_biggest_bar(file_data))
        print('Самый маленький бар', get_smallest_bar(file_data))
        user_longitude, user_latitude = input('\nВведите через пробел координаты текущего местоположения: \n').split(" ")
        print('Самый близкий бар:', str(get_closest_bar(file_data, float(user_longitude), float(user_latitude))))
    except FileNotFoundError as e:
        print("Файла не существует")
