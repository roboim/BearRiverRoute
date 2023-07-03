from pprint import pprint
import requests
import time


class OpenMeteoData:

    def get_open_meteo_data(self, lat_m, lon_m, start_m, end_m):
        time.sleep(0.51)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": lat_m, "longitude": lon_m,
                  "hourly": "temperature_2m,cloudcover,windspeed_10m,windgusts_10m",
                  "daily": "sunrise,sunset,weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum",
                  "start_date": start_m, "end_date": end_m,
                  "timezone": "Europe/Moscow"}
        while True:
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                if response.status_code == 200:
                    print("Получено")
                    # pprint(response.json())
                    break
            except requests.ConnectionError as e:
                print("Повторное соединение")
                print(str(e))
                time.sleep(0.51)
                continue
            except requests.Timeout as e:
                print("Превышен период ожидания. Повторное соединение.")
                print(str(e))
                time.sleep(0.51)
                continue
            except requests.RequestException as e:
                print("Общая ошибка. Повторное соединение.")
                print(str(e))
                time.sleep(0.51)
                continue
        return response.json()

    def add_route_forecast(self, result, active_route):
        name = str(result['latitude'])
        name += ", " + str(result['longitude'])
        temperature_l = result['hourly']['temperature_2m']
        temperature = sum(temperature_l) / len(temperature_l)
        temperature_2m_max = result['daily']['temperature_2m_max']
        temperature_2m_min = result['daily']['temperature_2m_min']
        precipitation_sum_l = result['daily']['precipitation_sum']
        precipitation_sum = sum(precipitation_sum_l) / len(precipitation_sum_l)
        sunrise = result['daily']['sunrise'][0][11:]
        sunset = result['daily']['sunset'][0][11:]
        wind_l = result['hourly']['windspeed_10m']
        wind = sum(wind_l) / len(wind_l)
        wind_gust_l = result['hourly']['windgusts_10m']
        wind_gust = sum(wind_gust_l) / len(wind_gust_l)
        clouds_l = result['hourly']['cloudcover']
        clouds = sum(clouds_l) / len(clouds_l)
        description = result['daily']['weathercode']

        active_route.name_p = name
        active_route.temperature_p = temperature
        active_route.temperature_2m_max_p = temperature_2m_max
        active_route.temperature_2m_min_p = temperature_2m_min
        active_route.sunrise_p = sunrise
        active_route.sunset_p = sunset
        active_route.wind_p = wind
        active_route.wind_gust_p = wind_gust
        active_route.clouds_p = clouds
        active_route.description_p = description
        active_route.precipitation_sum_p = precipitation_sum
        active_route.precipitation_sum_l = precipitation_sum_l
