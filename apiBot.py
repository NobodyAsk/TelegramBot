import requests
import json
import re
from PIL import Image, ImageFont, ImageDraw
import datetime
import data_bot
import random

# API ID from https://api.openweathermap.org
WEATHER_ID="<Insert your API_ID here>"
# path for image
img = "img/citate_template.jpg"

def get_week_day():
    """ Make image with a caption of the current weekday. """
    usual_img = "img/weekday.jpg"
    wednesday_img = "img/wednesday.jpg"
    day = datetime.datetime.today().strftime('%A')
    #   Особая картинка для среды
    if day == "Wednesday":
        img = Image.open(wednesday_img).save("img/weekday_temp.jpg")
        img = Image.open("img/weekday_temp.jpg")
        #   Настраиваем шрифт и положение надписи
        font = ImageFont.truetype("img/ariblk.ttf", size = 120)
        draw_text = ImageDraw.Draw(img)
        draw_text.text(
        (300, 1100),
        day,
        #   Добавляем шрифт к изображению
        font=font,
        fill='#ffffff',# Цвет
        )
    else:
        img = Image.open(usual_img).save("img/weekday_temp.jpg")
        img = Image.open("img/weekday_temp.jpg")
        #   Настраиваем шрифт и положение надписи
        font = ImageFont.truetype("img/ariblk.ttf", size = 76)
        draw_text = ImageDraw.Draw(img)
        draw_text.text(
        (280, 600),
        day,
        #   Добавляем шрифт к изображению
        font=font,
        fill='#ffffff',# Цвет
        )
    img.save("img/weekday_temp.jpg")  
    return "img/weekday_temp.jpg"

def kanye_quote():
    """ Get the kanye quote from his twitter. """
    try:
        response = requests.get("https://api.kanye.rest")
        response.raise_for_status()
        quote = response.json()
        return quote["quote"]
    except:
        return "Revolution."

def cat_send():
    """ Get the Cat Fact. """
    try:
        response = requests.get("https://meowfacts.herokuapp.com/")
        response.raise_for_status()
        cat = response.json()
        return(cat["data"][0])
    except:
        return "Багирка топчик"

def make_img_citate(message):
    """ Make image with a caption of the bot's answer. 
    Needing to create folder called 'img'"""
    id = message.chat.id
    text = data_bot.make_reply(id)
    text = text.split(" ")
    redacted_text = []
    num = 0
    for i in text:
        num+= len(i)
        if num > 20:
            num = 0
            redacted_text.append("\n")
        redacted_text.append(i)
    text=" ".join(redacted_text)
    img = Image.open(img).save("img/citate_temp.jpg")
    img = Image.open("img/citate_temp.jpg")
    # Create object with font (Need to provide custom font)
    font = ImageFont.truetype("img/comic.ttf", size = 48)
    draw_text = ImageDraw.Draw(img)
    draw_text.text(
        (50, 100),
        text,
        #   Добавляем шрифт к изображению
        font=font,
        fill='#ffffff',# Цвет
        )
    img.save("img/citate_temp.jpg")
    return "img/citate_temp.jpg"

def weather_check(message):   
    """ Return the weather in city from city_list.
    See also functions 'add_city()', 'get_city_list()' in 'data_bot.py' and
    'weather()', 'get_city_list()', 'add_new_city()' in 'main.py'. """   

    user_city = message.text.split("огода в ")[1].lower()
    with open ("cities.json", "r", encoding="utf-8") as data_file:
        cities = json.load(data_file)
    for city in cities:
        if city == user_city:
            lat = cities[city]["lat"]
            lon = cities[city]["lon"]
            city = city.capitalize()
            break
    try:
        param = {
        "lat":lat,
        "lon":lon,
        "appid": WEATHER_ID,
        "lang":"ru"
        }
    except:
        return "Такого города нет в моем списке."
    try:
        response = requests.get(url = "https://api.openweathermap.org/data/2.5/weather", params=param)
        response.raise_for_status()
        weather = response.json()
        sky = weather["weather"][0]["description"]
        wind_velocity = weather["wind"]["speed"]
        wind_direction = weather["wind"]["deg"]
        temperature = round(weather["main"]["temp"]-273, 0)
        temp=int((wind_direction/22.5)+.5)
        arr=["северный","северо-северозападный","северозападный","запад-северозападный","западный","запад-югозападный", "юго-западный", "юго-югозападный","южный","юго-юговосточный","юговосточный","восток-юговосточный","восточный","восточный-северовосточный","северовосточный","север-северовосточный"]
        wind_direction = arr[(temp % 16)]
        place = weather["name"]
        return f"Небо в городе {city} {sky}. Температура воздуха {temperature} град. Ветер {wind_direction}, {wind_velocity} м/сек. [{place}]"
    except:
        return "Ошибка. Попробуйте позже."

def request_photo(message):
    """ Find image in yandex searching. """
    random.Random()
    try:
        text=message.text.split("ажи ")[1]
    except:
       return "Нечего показывать"
    with open("black_list.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
        for i in data["words"]:
            if i.lower() in text.lower():
                return "Это плохой запрос"
    req = requests.get("https://yandex.ru/images/search?text="+text)

    ph_links = list(filter(lambda x: '.jpg' in x, re.findall('''(?<=["'])[^"']+''', req.text)))
    ph_list = []
    for i in range(len(ph_links)):
        if (ph_links[i][0] == "h"):
            ph_list.append(ph_links[i])
    del ph_links
    if len(ph_list)==0:
        return "ничего не найдено"
    return ph_list[random.randint(0, len(ph_list))]

def add_black_words(message):
    """ Adding words in black list for searching. """
    word = message.text.split("лово ")[1]
    with open ("black_list.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    new_data = data["words"]
    print(new_data)
    new_data.append(word)
    new_data = {"words":new_data}
    data.update(new_data)
    with open("black_list.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)
    return "Плохое слово добавлено"