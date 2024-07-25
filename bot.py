import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды: /show_city [город][цвет], /remember_city [город], /show_my_cities[цвет]")

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-2]
    color = message.text.split()[-1]

    user_id = message.chat.id
    manager.create_grapf(f'{user_id}.png',[city_name],color)
    with open(f'{user_id}.png','rb') as map:
        bot.send_photo(user_id, map)

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    color = message.text.split()[-1]
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    if cities:
        manager.create_grapf(f'{message.chat.id}_cities.png',cities,color)
        with open(f'{message.chat.id}_cities.png','rb') as map:
            bot.send_photo(message.chat.id, map)
    else:
        bot.send_message(message.chat.id,'У вас пока нет сохранённых городов')

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
