import telebot
import requests
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))

@bot.message_handler(commands=["start"]) 
def start(message):
    bot.send_message(message.chat.id, "Привет, введи свой город")


@bot.message_handler(content_types="text")
def handle_text(message):
    PARAMS = {
        "apikey": os.getenv("YANDEX_API"),
        "geocode": message.text,
        "format": "json"
        }
    response = requests.get("https://geocode-maps.yandex.ru/1.x/", params= PARAMS)
    if response.status_code != 200:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте позже.")
        return 
    data = response.json()
    coordinates = data["response"]["GeoObjectCollection"]["featureMember"]
    if not coordinates:
        bot.send_message(message.chat.id, "Город не найден")
        return 
    pos = coordinates[0]["GeoObject"]["Point"]["pos"]
    lng, lat = pos.split(" ")
    today = date.today()
    PARAMS_TIME_SUNRISE = {
        "lat": lat,
        "lng": lng,
        "date": today
    } 
    time_sunrise = requests.get("https://api.sunrise-sunset.org/v2", params=PARAMS_TIME_SUNRISE)
    if time_sunrise.status_code != 200:
        bot.send_message(message.chat.id, "Не удалось получить данные о времени восхода, попробуйте позже")
        return 
    date_time = time_sunrise.json()
    sunrise_time = date_time["sunrise"].split("T")[1].split("+")[0][:5]
    sunset_time = date_time["sunset"].split("T")[1].split("+")[0][:5]
    hours, minutes = date_time["day_length"] // 3600, (date_time["day_length"] % 3600) // 60

    PARAMS_WEATHER = {
        "latitude": lat,
        "longitude": lng,
        "current": "temperature_2m,weather_code,precipitation,relative_humidity_2m",
        "timezone": "auto"
    }
    response_weather = requests.get("https://api.open-meteo.com/v1/forecast", params=PARAMS_WEATHER)
    if response_weather.status_code != 200:
        print("Статус погоды:", response_weather.status_code)
        print(response_weather.text)
        bot.send_message(message.chat.id, "Не удалось получить данные о погоде, попробуйте позже.")
        return 
    
    date_weather = response_weather.json()
    temperature = date_weather["current"]["temperature_2m"]
    precipitation_date = date_weather["current"]["precipitation"]
    weather_code = date_weather["current"]["weather_code"]
    humidity_date = date_weather["current"]["relative_humidity_2m"]

    print(date_weather)
    WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Слабая морось",
    53: "Морось",
    55: "Сильная морось",
    61: "Слабый дождь",
    63: "Дождь",
    65: "Сильный дождь",
    71: "Слабый снег",
    73: "Снег",
    75: "Сильный снег",
    80: "Ливень",
    95: "Гроза",
    }
    weather_text = WEATHER_CODES.get(weather_code, "Неизвестно")

    text = (
        f"Погода: \n"
        f"🌡 Температура: {temperature} °C\n"
        f"☁️ Погода: {weather_text}\n"
        f"💧 Осадки: {precipitation_date} мм\n"
        f"💦 Влажность: {humidity_date} % \n"
        f"🌅 Рассвет: {sunrise_time}\n"
        f"🌇 Закат: {sunset_time} \n"
        f"☀️ Длина дня: {hours} ч. {minutes} м."
        
    )
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)