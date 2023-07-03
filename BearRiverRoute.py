import requests
import csv
import time
import textwrap
from fpdf import FPDF
from open_meteo_data import OpenMeteoData
from pprint import pprint
from datetime import datetime, timedelta


class RouteData:
    def __init__(self, route_n: int, route_db_n: int, river_name_p: str, area_p: str, start_point_p: str, end_point_p: str,
                 distance_km_p: str, year_journey_p: str, qty_days_p: str, distance_from_city_p: str, feature_p: str,
                 camping_places_p: str, coord_camping_places_p: str, picture_links_p: str,
                 coord_start_point_p: str, coord_end_point_p: str, name_p: str, temperature_p: float,
                 temperature_2m_max_p: list, temperature_2m_min_p: list, sunrise_p: str, sunset_p: str,
                 wind_p: float, wind_gust_p: float, clouds_p: float, description: list, description_p: list,
                 precipitation_sum_p: float, precipitation_sum_l: list):
        self.route_n = route_n  # ['Маршрут']
        self.route_db_n = route_db_n  # ['№']
        self.river_name_p = river_name_p  #['Река']
        self.area_p = area_p  #['Область']
        self.start_point_p = start_point_p  #['Место старта']
        self.end_point_p = end_point_p  #['Место финиша']
        self.distance_km_p = distance_km_p  #['Дистанция']
        self.year_journey_p = year_journey_p  #['Год']
        self.qty_days_p = qty_days_p  #['Кол-во дней']
        self.distance_from_city_p = distance_from_city_p  #['От Москвы, км']
        self.feature_p = feature_p  #['Особенность']
        self.camping_places_p = camping_places_p  #['Стоянки']
        self.coord_camping_places_p = coord_camping_places_p  #['Координаты стоянок']
        self.picture_links_p = picture_links_p  #['Фотоотчёт']
        self.coord_start_point_p = coord_start_point_p  #['Координаты старта']
        self.coord_end_point_p = coord_end_point_p  #['Координаты финиша']
        self.name_p = name_p  #['Ответ сервера по месту прогноза']
        self.temperature_p = temperature_p  #['Температура']
        self.temperature_2m_max_p = temperature_2m_max_p  #['Максимальная температура по дням']
        self.temperature_2m_min_p = temperature_2m_min_p  #['Минимальная температура по ночам']
        self.sunrise_p = sunrise_p  #['Рассвет']
        self.sunset_p = sunset_p  #['Закат']
        self.wind_p = wind_p  #['Ветер']
        self.wind_gust_p = wind_gust_p  #['Порыв ветра']
        self.clouds_p = clouds_p  #['Облачность']
        self.description = description  # ['Погода по дням']
        self.description_p = description_p  #['Погода']
        self.precipitation_sum_p = precipitation_sum_p  #['Осадки']
        self.precipitation_sum_l = precipitation_sum_l  #['Осадки по дням']

    def route_clear(self):
        self.route_n = 0  # ['Маршрут']
        self.route_db_n = 0  # ['№']
        self.river_name_p = ""  #['Река']
        self.area_p = ""  #['Область']
        self.start_point_p = ""  #['Место старта']
        self.end_point_p = ""  #['Место финиша']
        self.distance_km_p = ""  #['Дистанция']
        self.year_journey_p = ""  #['Год']
        self.qty_days_p = ""  #['Кол-во дней']
        self.distance_from_city_p = ""  #['От Москвы, км']
        self.feature_p = ""  #['Особенность']
        self.camping_places_p = ""  #['Стоянки']
        self.coord_camping_places_p = ""  #['Координаты стоянок']
        self.picture_links_p = ""  #['Фотоотчёт']
        self.coord_start_point_p = ""  #['Координаты старта']
        self.coord_end_point_p = ""  #['Координаты финиша']
        self.name_p = ""  #['Ответ сервера по месту прогноза']
        self.temperature_p = 0.0  #['Температура']
        self.temperature_2m_max_p = []  #['Максимальная температура по дням']
        self.temperature_2m_min_p = []  #['Минимальная температура по ночам']
        self.sunrise_p = ""  #['Рассвет']
        self.sunset_p = ""  #['Закат']
        self.wind_p = 0.0  #['Ветер']
        self.wind_gust_p = 0.0  #['Порыв ветра']
        self.clouds_p = 0.0  #['Облачность']
        self.description = []  # ['Погода по дням']
        self.description_p = []  #['Погода']
        self.precipitation_sum_p = 0.0  #['Осадки']
        self.precipitation_sum_l = []  #['Осадки по дням']

    def read_active_route(self, route_number, route_data):
        self.route_n = route_number
        self.route_db_n = route_data['№']
        self.river_name_p = route_data['Река']
        self.area_p = route_data['Область']
        self.start_point_p = route_data['Место старта']
        self.end_point_p = route_data['Место финиша']
        self.distance_km_p = route_data['Дистанция']
        self.year_journey_p = route_data['Год']
        self.qty_days_p = route_data['Кол-во дней']
        self.distance_from_city_p = route_data['От Москвы, км']
        self.feature_p = route_data['Особенность']
        self.camping_places_p = route_data['Стоянки']
        self.coord_camping_places_p = route_data['Координаты стоянок']
        self.picture_links_p = route_data['Фотоотчёт']
        self.coord_start_point_p = route_data['Координаты старта']
        self.coord_end_point_p = route_data['Координаты финиша']

    def write_route_forecast(self, route_data):
        route_data['Ответ сервера по месту прогноза'] = self.name_p
        route_data['Температура'] = self.temperature_p
        route_data['Максимальная температура по дням'] = self.temperature_2m_max_p
        route_data['Минимальная температура по ночам'] = self.temperature_2m_min_p
        route_data['Рассвет'] = self.sunrise_p
        route_data['Закат'] = self.sunset_p
        route_data['Ветер'] = self.wind_p
        route_data['Порыв ветра'] = self.wind_gust_p
        route_data['Облачность'] = self.clouds_p
        route_data['Погода по дням'] = self.description
        route_data['Погода'] = self.description_p
        route_data['Осадки'] = self.precipitation_sum_p
        route_data['Осадки по дням'] = self.precipitation_sum_l

    def route_pr(self):
        pprint(self.river_name_p)
        pprint(self.area_p)


def split_lat_lon(coord_str) -> dict:
    coords = coord_str.split(', ')
    coords_d = dict()
    coords_d.setdefault("lat", coords[0])
    coords_d.setdefault("lon", coords[1])
    return coords_d


def read_routes(file_csv) -> dict:
    """ чтение csv через rDictReader.
    # особенности: читаем только построчно, файл закрывать нельзя, можно читать сколь угодно большие файлы
    # не нужно считать номера колонок, т.к. у них теперь есть имена
    """
    with open(file_csv, "r", encoding="UTF-8") as f:
        routes_reader = csv.DictReader(f)
        count = 0
        data_routes = dict()
        for row in routes_reader:
            count += 1
            data_routes.setdefault(count, row)
            # for field in row:
                # print(field)
                # print(row[field])
    # print(data_routes)
    print(f"В этом файле указано количество маршрутов: {count}")
    return data_routes


def route_info_print2(best_offer_r, route_r, i_r):
    wmo_dict = {"0": "Чистое небо",
                "1": "В основном ясно",
                "2": "Переменная облачность",
                "3": "Пасмурная погода",
                "45": "Туман",
                "48": "Туман осаждающийся в иней",
                "51": "Моросящий дождь: легкий",
                "53": "Моросящий дождь: умеренный",
                "55": "Моросящий дождь: густой и интенсивный",
                "56": "Моросящий дождь: лёгкой интенсивности",
                "57": "Моросящий дождь: высокой интенсивности",
                "61": "Дождь: небольшой",
                "63": "Дождь: умеренный",
                "65": "Дождь: сильной интенсивности",
                "66": "Ледяной дождь: лёгкой интенсивности",
                "67": "Ледяной дождь: высокой интенсивности",
                "71": "Выпадение снега: незначительное",
                "73": "Выпадение снега: умеренное",
                "75": "Снегопад: большая интенсивность",
                "77": "Ледяной снег",
                "80": "Ливневые дожди: незначительные",
                "81": "Ливневые дожди: умеренные",
                "82": "Ливневые дожди: сильные",
                "85": "Небольшой снегопад",
                "86": "Сильный снегопад",
                "95": "Гроза: слабая или умеренная",
                "96": "Гроза с небольшим градом",
                "99": "Гроза с сильным градом",
                }
    river_name_p = best_offer_r[route_r]['Река']
    area_p = best_offer_r[route_r]['Область']
    start_point_p = best_offer_r[route_r]['Место старта']
    end_point_p = best_offer_r[route_r]['Место финиша']
    distance_km_p = best_offer_r[route_r]['Дистанция']
    year_journey_p = best_offer_r[route_r]['Год']
    qty_days_p = best_offer_r[route_r]['Кол-во дней']
    distance_from_city_p = best_offer_r[route_r]['От Москвы, км']
    feature_p = best_offer_r[route_r]['Особенность']
    camping_places_p = best_offer_r[route_r]['Стоянки']
    coord_camping_places_p = best_offer_r[route_r]['Координаты стоянок']
    picture_links_p = best_offer_r[route_r]['Фотоотчёт']
    coord_start_point_p = best_offer_r[route_r]['Координаты старта']
    coord_end_point_p = best_offer_r[route_r]['Координаты финиша']
    name_p = best_offer_r[route_r]['Ответ сервера по месту прогноза']
    temperature_p = best_offer_r[route_r]['Температура']
    temperature_2m_max_p = data_routes[route_r]['Максимальная температура по дням']
    temperature_2m_min_p = data_routes[route_r]['Минимальная температура по ночам']
    sunrise_p = best_offer_r[route_r]['Рассвет']
    sunset_p = best_offer_r[route_r]['Закат']
    wind_p = best_offer_r[route_r]['Ветер']
    wind_gust_p = best_offer_r[route_r]['Порыв ветра']
    clouds_p = best_offer_r[route_r]['Облачность']
    description_p = best_offer_r[route_r]['Погода']
    # print(description_p)
    try:
        description = [wmo_dict[str(x)] for x in description_p]
    except KeyError:
        description = "Что-то неизвестное по коду погоды"
    precipitation_sum_p = data_routes[route_r]['Осадки']
    precipitation_sum_l = data_routes[route_r]['Осадки по дням']

    str_forecast = "\n\nМаршрут № " + str(i_r)

    # print(precipitation_sum_p)
    if precipitation_sum_p > 0.2 or max(precipitation_sum_l) > 0.2:
        str_forecast += "\nДОЖДЬ!"
    else:
        str_forecast += "\nНет дождя."

    str_forecast += "\nМаршрут по реке " + river_name_p + ": " + start_point_p + " - " + end_point_p + \
                    " на " + str(qty_days_p) + " дня(ей) ≈ " + str(distance_km_p) + " км." \
                    "\nВажные комментарии: " + feature_p + "." \
                    "\nОбласть: " + area_p + "." \
                    "\nКоординаты старта: " + coord_start_point_p + ", финиша: " + coord_end_point_p + \
                    "\nРасположен примерно в " + str(distance_from_city_p) + " км от Москвы." \
                    "\nКоординаты стоянки: " + coord_camping_places_p + \
                    "\nСтоянок: " + camping_places_p + \
                    "\nПогода: " + str(description) + \
                    "\nОсадки: " + str(precipitation_sum_l) + \
                    "\nТемпература в пункте " + name_p + " составляет \nднём до: " + str(temperature_2m_max_p) + " гр," \
                    "\nночью до: " + str(temperature_2m_min_p) + " гр," \
                    "\nоблачность " + str(clouds_p)[0:5] + "," \
                    "\nскорость ветра " + str(wind_p)[0:5] + " м/с, с порывами до " + str(wind_gust_p)[0:5] + " м/с," \
                    "\nв часовом поясе МСК время восхода " + str(sunrise_p) + ", заката " + str(sunset_p) + "." \
                    "\nФотоотчёт: " + picture_links_p + ", пройден в " + str(year_journey_p) + " г."

    str_forecast += make_helpful_link(coord_start_point_p, coord_end_point_p)
    print(str_forecast)
    with open("прогноз.txt", "a", encoding='UTF-8') as file1:
        file1.write(str_forecast)

    route_item_p = [river_name_p, start_point_p, end_point_p]
    return route_item_p


def make_helpful_link(coord_start_p, coord_end_p):
    p1 = split_lat_lon(coord_start_p)
    p2 = split_lat_lon(coord_end_p)
    #https://brouter.de/brouter-web/#map=5/57.140/41.950/standard&lonlats=33.713608,58.107636;33.802872,58.137824&profile=river
    str_out = "\n\nBrouter:\n"
    str_out += "https://brouter.de/brouter-web/#map=5/57.140/41.950/standard&lonlats=" + p1["lon"] + "," + p1["lat"] + \
        ";" + p2["lon"] + "," + p2["lat"] + "&profile=river"
    # https://yandex.ru/pogoda/details/10-day-weather?lat=57.6638&lon=34.7665&via=ms#8
    str_out += "\nПрогноз от Яндекс.Погоды на ближайшие 10 дней:\n"
    str_out += "https://yandex.ru/pogoda/details/10-day-weather?lat=" + p1["lat"] + "&lon=" + p1["lon"] + "&via=ms#8"

    return str_out


def make_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 12
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', fontsize_pt)

    with open(text, "r", encoding='UTF-8') as f:
        for x in f:
            pdf.cell(50, 5, txt=x, ln=1, align='L')
    pdf.output(filename)


def manual_input(test_value):
    data_request = dict()
    if test_value == 0:
        weekend = input("\nТребуется прогноз на ближайшие субботу и воскресенье на 2 дня до 401 км от Москвы? ")
        weekend = weekend.lower()
        if weekend == "да" or weekend == "1":
            test_value = 1
        else:
            test_value = 0
    if test_value == 0:
        target_days = input("\nУкажите количество дней:")
        try:
            target_days = int(target_days)
            data_request.setdefault("target_days", target_days)
        except ValueError:
            print("Некорректный ввод")
            exit(101)
        if int(target_days) > 14:
            target_days = "14"
        start_day = input("\nУкажите дату начала маршрута(ГГГГ-ММ-ДД):")
        try:
            start_day = str(start_day)
            data_request.setdefault("start_day", start_day)
        except ValueError:
            print("Некорректный ввод")
            exit(1001)
        start_day_d = datetime.strptime(start_day, "%Y-%m-%d").date()
        finish_day = start_day_d + timedelta(int(target_days)-1)
        data_request.setdefault("finish_day", finish_day)
        today_now = datetime.now().date()
        finish_max_day = today_now + timedelta(14)
        if today_now > start_day_d or start_day_d > finish_max_day or today_now > finish_day or finish_day > finish_max_day:
            print(f"\nДата начала и завершения маршрута должны быть в интервале: {today_now} - {finish_max_day}")
            exit(1002)
        target_distancemin_km = input("\nУкажите минимальную удалённость от Москвы в км:")
        try:
            target_distancemin_km = int(target_distancemin_km)
            data_request.setdefault("target_distancemin_km", target_distancemin_km)
        except ValueError:
            print("Некорректный ввод")
            exit(102)
        target_distancemax_km = input("\nУкажите максимальную удалённость от Москвы в км:")
        try:
            target_distancemax_km = int(target_distancemax_km)
            data_request.setdefault("target_distancemax_km", target_distancemax_km)
        except ValueError:
            print("Некорректный ввод")
            exit(103)
        print("\n")
    elif test_value == 1:
        # Ближайшая суббота
        d_start = datetime.today().strftime('%Y-%m-%d')
        d = datetime.strptime(d_start, '%Y-%m-%d')
        t = timedelta((7 + 5 - d.weekday()) % 7)

        target_days = "2"
        start_day = (d + t).strftime('%Y-%m-%d')
        start_day_d = datetime.strptime(start_day, "%Y-%m-%d").date()
        finish_day = start_day_d + timedelta(int(target_days)-1)
        target_distancemin_km = "1"
        target_distancemax_km = "401"

        data_request.setdefault("target_days", target_days)
        data_request.setdefault("start_day", start_day)
        data_request.setdefault("finish_day", finish_day)
        data_request.setdefault("target_distancemin_km", target_distancemin_km)
        data_request.setdefault("target_distancemax_km", target_distancemax_km)

    # pprint(data_request)
    return data_request


def check_and_sort_routes(input_data, data_routes_r):
    list_offer = dict()
    major_points = list()
    for route_number_r, route_data_r in data_routes_r.items():
        active_route.route_clear()
        active_route.read_active_route(route_number_r, route_data_r)

        if int(input_data['target_days']) >= int(active_route.qty_days_p) and \
                int(input_data['target_distancemax_km']) >= int(active_route.distance_from_city_p) and \
                int(input_data['target_distancemin_km']) <= int(active_route.distance_from_city_p):
            try:
                coord_data = split_lat_lon(active_route.coord_start_point_p)
                check_flag = active_route.coord_start_point_p + active_route.coord_end_point_p
                if check_flag not in major_points:
                    major_points.append(check_flag)
                    print(f'\nЗагружается маршрут: {active_route.route_db_n}')
                    if meteo_API == 2:
                        result_get = route_forecast.get_open_meteo_data(coord_data['lat'], coord_data['lon'],
                                                                        input_data['start_day'],
                                                                        input_data['finish_day'])
                        route_forecast.add_route_forecast(result_get, active_route)
                        active_route.write_route_forecast(route_data_r)
                        list_offer.setdefault(route_number_r, route_data_r)

            except IndexError:
                print(f"Не введены координаты старта для маршрута {active_route.river_name_p}: "
                      f"{active_route.start_point_p} - {active_route.end_point_p}.")

    best_offer = dict(sorted(list_offer.items(), key=lambda item: item[1]['Температура'], reverse=True))

    return best_offer


def print_sorted_routes(input_data, best_offer_p, print_pdf_p):
    list_best_offer = list(best_offer_p)

    str_file = "Сортировка выполнена по температуре, указано наличие или отсутствие дождя." \
                "\nРЕКОМЕНДАЦИИ ПО МАРШРУТАМ" \
                "\nДата начала:" + str(input_data['start_day']) + \
                "\nМаксимальная длительность: " + str(input_data['target_days']) + \
                "\nМинимальная удалённость от Москвы: " + str(input_data['target_distancemin_km']) + " км." \
                "\nМаксимальная удалённость от Москвы: " + str(input_data['target_distancemax_km']) + " км."
    with open("прогноз.txt", "w", encoding='UTF-8') as file1:
        file1.write(str_file)
    i = 1
    route_item = ['', '', '']
    for route in list_best_offer:
        if (route_item[0] == best_offer_p[route]['Река'] and
                route_item[1] == best_offer_p[route]['Место старта'] and route_item[2] == best_offer_p[route][
                    'Место финиша']):
            pass
        else:
            if meteo_API == 2:
                route_item = route_info_print2(best_offer_r, route, i)
            i += 1

    if print_pdf_p is True:
        input_filename = 'прогноз.txt'
        output_filename = 'прогноз.pdf'
        make_pdf(input_filename, output_filename)


# Moscow lat="55.6595",lon="37.7937"
# unixtime += 10800 # Время МСК
test_seting = 0
# 2 - get_open_meteo_data
meteo_API = 2
print_pdf = False
data_file_csv = "data.csv"
route_forecast = OpenMeteoData()
active_route = RouteData(0, 0, "", "", "", "",
                 "", "", "", "", "",
                 "", "", "",
                 "", "", "", 0.0,
                 [], [], "", "",
                 0.0, 0.0, 0.0, [], [],
                 0.0, [])

data_routes = read_routes(data_file_csv)
input_data_w = manual_input(test_seting)
best_offer_r = check_and_sort_routes(input_data_w, data_routes)
print_sorted_routes(input_data_w, best_offer_r, print_pdf)

exit_line = input("\nНажмите ввод для выхода: ")
