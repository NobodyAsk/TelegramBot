import telebot
import random
import apiBot
import data_bot

# Delete token and ID later!!!1
# Api token for bot from telegram
TOKEN = "<Insert your token here>"
# ID of the main user
MY_ID = "Insert your ID here"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Make start configuration for a new user"""
    id = message.chat.id
    text = data_bot.new_user(id)
    bot.send_message(id, text=text, parse_mode="html")

@bot.message_handler(commands = ["clear database"])
def clear(message):
    """ Clear all configurations and data for individual chat """
    if message.chat.type == "private":
        data_bot.new_user(message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Я сбросил ваши настройки. Давайте начнем заново.", parse_mode="html")
    else:
        administrators = bot.get_chat_administrators(message.chat.id)
        for ad in administrators:
            if message.from_user.id == ad.user.id:
                data_bot.new_user(message.chat.id)
                bot.send_message(chat_id=message.chat.id, text="Я сбросил ваши настройки. Давайте начнем заново.", parse_mode="html")

@bot.message_handler(regexp=("(?:запомни |Запомни )"))
def memory(message):
    """ Add phrase in to the database for this chat."""
    data_bot.add_phrase(message.chat.id, message.text, message.chat.type)
    bot.send_message(chat_id=message.chat.id, text="я запомнил.", parse_mode="html")

@bot.message_handler(regexp=("(?:Погода в|погода в)"))
def weather(message):
    """ Check weather for a city in city list (see 'get_city_list()'). """
    text = apiBot.weather_check(message)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("список город|Список город"))
def get_city_list(message):
    """ Show the list of available cities. To add new city in the list use function 'add_new_city()'."""
    text=data_bot.get_city_list()
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")  

@bot.message_handler(regexp=("бот добавить город"))
def add_new_city(message):
    """ Add new city in the list. """
    text=data_bot.add_city(message)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("бот покажи|Бот покажи"))
def show_img(message):
    """ Send a random image in current chat.
    Image gets from Yandex searching. """
    text=apiBot.request_photo(message)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("плохое слово|Плохое слово"))
def add_black_word(message):
    """ Add black word in a black list for image searching (see function 'show_img()'.) """
    text=data_bot.add_black_word(message)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")
    
@bot.message_handler(regexp=("(?:кэни|west|kanye|Kanye|Кэни|West|Кени|кени)"))
def kanye(message):
    """ Send random Kanye quote from twitter in chat. """
    text = apiBot.kanye_quote()
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("(?:факт дня|про кошк|про кот|то интер|скажи факт|Факт дня|акт про кош)"))
def cat_fact(message):
    """ Send random cat fact in chat. """
    text = apiBot.cat_send()
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("(?:ответ на картинке)"))
def img_citate(message):
    """ Send bot's answer on a custom image. """
    img = apiBot.make_img_citate(message)
    img = open(img, "rb")
    bot.send_photo(message.chat.id, photo = img)

@bot.message_handler(regexp=("(?:ень недели|егодня день)"))
def curr_weekday(message):
    """ Send current week day on a custom image. """
    img = apiBot.get_week_day()
    img = open(img, "rb")
    bot.send_photo(message.chat.id, photo = img)

@bot.message_handler(regexp=("(?:Бот скажи|бот скажи)"))
def triger(message):
    """ Trigger bot answer. """
    text=data_bot.make_reply(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")

@bot.message_handler(regexp=("бот уровень "))
def set_chat_level(message):
    """ Set a level of the bot's activity (from 0 to 100). """
    chat_level = message.text.split("вень ")[1]
    text=data_bot.set_chat_level(message.chat.id, chat_level)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="html")
 
@bot.message_handler(regexp=("format"))
def update_main_bank(message):
    """ Command for upadating common database (in progress). """
    if message.from_user.id == MY_ID:
        data_bot.update_main_bank()
        bot.send_message(chat_id=message.chat.id, text="Банк обновлен", parse_mode="html")

@bot.message_handler(regexp=("morning"))
def auto_send(message):
    """ Mailing to all register users current day image (see 'curr_weekday()') """
    if message.from_user.id == 372025616:
        users = data_bot.get_user_list()
        for i in users:
            img = apiBot.get_week_day()
            img = open(img, "rb")
            bot.send_photo(i, photo = img)
            print("send "+i)

@bot.message_handler(content_types="text")
def reply_to(message):
    """ Make answer from a bot. """
    try:
        if message.reply_to_message.from_user.username == "mechaTrab69bot":
            text=data_bot.make_reply(message.chat.id)
            bot.send_message(chat_id=message.chat.id, text=text)
    except:
        num = data_bot.get_chat_level(message.chat.id)
        if message.chat.type == "private":
            try:
                text=data_bot.make_reply(message.chat.id)
                bot.send_message(chat_id=message.chat.id, text=text)
                if random.randint(0,10)>3:
                    data_bot.add_phrase(message.chat.id, message.text, message.chat.type)
            except:
                return bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так")
        else:
            if random.randint(0,100) < num:
                text=data_bot.make_reply(message.chat.id)
                bot.send_message(chat_id=message.chat.id, text=text)

# Command to bot to listening for a users inputs
bot.polling(non_stop=True, timeout=180)
