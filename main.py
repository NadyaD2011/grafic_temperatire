import pandas as pd
import requests 
from matplotlib import pyplot as plt


def get_city_coord(city_name):
    params_coord = {'where': f'place_name="{city_name}" and country_code: "ES"'}

    url_coord = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records'
    response = requests.get(url_coord, params=params_coord)
    response.raise_for_status()
    if response.json()['total_count'] != 0:
        coord = response.json()['results'][0]['coordinates']
        return coord
    else:
        print('Произошла ошибка или такого города нет')


def get_meteo_date(coord, start_date, end_date):
    url_meteo = 'https://archive-api.open-meteo.com/v1/era5'
    params_meteo = {
        'latitude': coord['lat'],
        'longitude': coord['lon'],
        'start_date': start_date,
        'end_date': end_date,
        "hourly": "temperature_2m"
    }

    response = requests.get(url_meteo, params=params_meteo)
    response.raise_for_status()
    results = response.json()['hourly']

    return results


def make_the_diog(meteo_date, city_name):
    df = pd.DataFrame(list(zip(meteo_date['time'], meteo_date['temperature_2m'])), columns=['date', 'temp'])
    plt.plot(df['date'], df['temp'])
    plt.xlabel('Даты')
    plt.ylabel('Температуры (°C)')
    plt.title(f'График температуры в {city_name}')
    plt.show()


def main():
    city_name = input('Введите название города показатели погоды, которого вы хотите увидеть (на английском):') #"Los Angeles"
    start_date = input("Введите начальную дату прогноза(YYYY-MM-DD):") #"2020-06-01"
    end_date = input("Введите конечную дату прогноза(YYYY-MM-DD):") #"2025-06-05"
    coord = get_city_coord(city_name)
    meteo_date = get_meteo_date(coord, start_date, end_date)
    make_the_diog(meteo_date, city_name)


if __name__ == "__main__":
    main()