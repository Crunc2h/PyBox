import requests
import datetime as dt
import smtplib
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
API_ENDPOINT_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
API_ENDPOINT_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
DATA_FORMAT = "metric"

SMTP_ADDR = "smtp.gmail.com"
ACCESS_PW = os.environ.get("SMTP_LOGIN")
SENDER_MAIL = os.environ.get("SMTP_SENDER")
RECEIVER_MAIL = os.environ.get("SMTP_RECEIVERS")
LAT_LON_DATA = os.environ.get("LOC_COORDINATES")

def weather_api_request(lat, lon, format, api_key, url):
    params = {"lat": lat,
              "lon": lon,
              "units": format,
              "appid": api_key}

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def strip_hour_data(dt_text):
    return dt_text.split(' ')[1].split(':')[0] if dt_text.split(' ')[1].split(':')[0][0] != '0' else dt_text.split(' ')[1].split(':')[0][1]


def filter_forecast_data(forecast_data):
    today_forecast = []
    for i in range(8):
        today_forecast.append(forecast_data["list"][i])
    today_forecast = [hourly_forecast for hourly_forecast in today_forecast if int(strip_hour_data(hourly_forecast["dt_txt"])) > dt.datetime.now().hour]
    return today_forecast


def create_current_weather_report(weather_data):
    return f"Current temp is {weather_data['main']['temp']} celsius and felt temp is {weather_data['main']['feels_like']} celsius and weather is {weather_data['weather'][0]['description']}.\n"


def create_forecast_report(current_temp, forecast_data):
    precipitation_predictions = []
    sum_temp = current_temp

    for hourly_forecast in forecast_data:
        temp = hourly_forecast["main"]["temp"]
        if hourly_forecast["weather"][0]["id"] / 100 < 7:
            precipitation_predictions.append(hourly_forecast)
        sum_temp += temp

    avg_temp = round(sum_temp / len(forecast_data) + 1, 2)
    report = f"Average expected temp is {avg_temp} celsius."

    for prediction in precipitation_predictions:
        report += f"\nPrecipitation of type {prediction['weather'][0]['description']} at hour {strip_hour_data(prediction['dt_txt'])} is expected."

    return report


def prepare_final_weather_report(location_data):
    final_string = ""
    for location in location_data:
        location_current_weather_data = weather_api_request(lat=location["lat"],
                                                            lon=location["lon"],
                                                            format=DATA_FORMAT,
                                                            api_key=API_KEY,
                                                            url=API_ENDPOINT_WEATHER)
        location_current_forecast_data = weather_api_request(lat=location["lat"],
                                                             lon=location["lon"],
                                                             format=DATA_FORMAT,
                                                             api_key=API_KEY,
                                                             url=API_ENDPOINT_FORECAST)
        report_string = f"----{location['name']}----\n"
        report_string += create_current_weather_report(location_current_weather_data)
        report_string += create_forecast_report(location_current_weather_data["main"]["temp"], location_current_forecast_data["list"])
        report_string += "\n------------\n"
        final_string += report_string

    return final_string

weather_report = prepare_final_weather_report(LAT_LON_DATA)

with smtplib.SMTP(SMTP_ADDR) as connection:
    connection.starttls()
    connection.login(user=SENDER_MAIL, password=ACCESS_PW)
    connection.sendmail(from_addr=SENDER_MAIL, to_addrs=RECEIVER_MAIL, msg=f"Subject:Weather Report\n\n{weather_report}")







