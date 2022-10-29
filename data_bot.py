import random
import json

def new_user(id):
    """ Adding a new user in the database. """
    with open ("data.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    try:
        new_data = data[f"{id}"]
    except:
        new_data = {f"{id}":{
            "data":["Привет.", "Я настоящий мальчик.", "У меня нет рта, но я хочу кричать."],
            "main_bank": False,
            "chat_level":40
        }
        }
    data.update(new_data)
    with open ("data.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)
    return "Привет. Давай поговорим."

def make_reply(id):
    """ Return reply from the bot. """
    try:
        with open("data.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
        if len(data[f"{id}"]["data"]) < 5:
            return "Мало слов. Используйте команду \"запомнить\""
    except (KeyError):
        new_user(id)
        with open("data.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
    except:
        return print("There are error in Make_reply function")
    try:
        if data[f"{id}"]["main_bank"] == True:
            id = 0
    except:
        pass
    text = []
    text_list=[]
    num = random.randint(0,10)
    for i in range(0,4):
        text_list.append(data[f"{id}"]["data"][random.randint(0,len(data[f"{id}"]["data"])-1)].split(" "))
    for i in range(1, random.randint(1, len(text_list[0]))):
        text.append(text_list[0][i])
    if num>5 and len(text_list[1]) > 2:
        for i in range(1, random.randint(0, len(text_list[1])-1)):
            text.append(text_list[1][i])
    if num>8 and len(text_list[2]) > 2:
        for i in range(1, random.randint(0, len(text_list[2])-1)):
            text.append(text_list[2][i])
    num = random.randint(1, len(text_list[3]))
    for i in range(num, len(text_list[3])):
        text.append(text_list[3][i])
    sentence = " ".join(text)
    return sentence

def get_user_list():
    """ Return a list of all users in the database. """
    with open("data.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    users = []
    for i in data:
        if i == "0":
            continue
        else:
            users.append(i)
    return users

def add_phrase(id, user_text, chat_type):
    """ Add phrase from user in the database. """
    try:
        text = user_text.split("мни ")[1]
    except:
        if chat_type == "private":
            text = user_text
        else:
            return "я не запомнил"
    try:
        with open("data.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
        try:
            new_data = data[f"{id}"]
            new_data["data"].append(text)
            new_data={f"{id}":new_data}
        except (KeyError or IndexError):
            print("error: проблема в функции add_phrase")
            new_data=new_user(id)
        data.update(new_data)
        with open("data.json", "w", encoding="utf-8") as data_file: 
            json.dump(data, data_file, indent=4)
    except:
        return "я не запомнил"

def update_users():
    """ Function for updating user's configuration in the database. """
    with open("data.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
        dump_data = {}
        for i in data:
            new_data = data[i]
            new_data["main_bank"] = False
            new_data["chat_level"] = 5
            dump_data[i] = new_data
    with open("data.json", "w", encoding="utf-8") as data_file:
        json.dump(dump_data, data_file, indent=4)
    
def clean_data(id):
    """ Clean user's data in the database (in progress). """
    pass

def update_main_bank():
    """ Update common database (in progress). """  
    pass

def set_chat_level(id, chat_level):
    """ Set bot's activity level. """
    try:
        chat_level = int(chat_level)
        if chat_level < 0:
            chat_level = 0
        elif chat_level > 100:
            chat_level = 100
    except:
        return "ошибка в иземенении уровня активности"
    with open ("data.json","r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    new_data = data[f"{id}"]
    new_data["chat_level"] = chat_level
    new_data = {f"{id}":new_data}
    data.update(new_data)
    with open("data.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)
    return f"Уровень активности бота: {chat_level}"

def get_chat_level(id):
    """ Show bot's activity level. """
    try:
        with open("data.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
        chat_level = data[f"{id}"]["chat_level"]
    except:
        print ("Error: Нет записи про уровень активности бота в функции get_chat_level")
        chat_level = 10
    return chat_level

def add_black_word(message):
    """ Add black words in black_list. """
    word = message.text.split("лово ")[1]
    with open ("black_list.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    new_data = data["words"]
    new_data.append(word)
    new_data = {"words":new_data}
    data.update(new_data)
    with open("black_list.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)
    return "Плохое слово добавлено"

def add_city(message):
    """ Add new city in city_list.
    Format: Город (<City_Name>) долгота <City longitude> широта <City latitude> """
    text = message.text
    try:
        city = text.split("ород (")[1].split(")")[0].lower()
        lon = float(text.split("долгота ")[1].split(" ")[0])
        lat = float(text.split("широта ")[1].split(" ")[0])
        with open ("cities.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
        new_data ={city:{"lon":lon, "lat":lat}}
        data.update(new_data)
        with open("cities.json", "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=4)
        return ("Добавил город под названием " + city.capitalize())
    except:
         return "Возникла ошибка"

def get_city_list():
    """ Return a list of available cities. """
    with open("cities.json","r") as data_file:
        data=json.load(data_file)
    city_list=list(data.keys())
    text="/n".join(city_list)
    return text