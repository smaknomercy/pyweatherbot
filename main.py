import telebot
import config
from pyowm import OWM
from telebot import types
city = "Lviv"
standart_city = "Lviv"
owm = OWM(config.TOKEN_OWM)
mgr = owm.weather_manager()
spost = mgr.weather_at_place(city)
w = spost.weather
bot = telebot.TeleBot(config.TOKEN_BOT)
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода')
    btn2 = types.KeyboardButton('Температура')
    btn3 = types.KeyboardButton('Вологість')
    btn4 = types.KeyboardButton('Атмосферний тиск')
    markup.add(btn2, btn3, btn4, btn1)
    bot.send_message(message.chat.id, 'Привіт {0.first_name}! Я погодний бот.\nЩоб дізнатись або змінити обране місто, натисніть /settings'.format(message.from_user), reply_markup=markup)
@bot.message_handler(commands=["settings"])
def sett(message):
    markup1 = types.InlineKeyboardMarkup(row_width=3)
    inbtn1 = types.InlineKeyboardButton('Дізнатись обране місто', callback_data='dizm')
    inbtn2 = types.InlineKeyboardButton('Змінити обране місто', callback_data='zminm')
    markup1.add(inbtn1, inbtn2)
    bot.send_message(message.chat.id, 'Оберіть, що вам потрібно', reply_markup=markup1)
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data=='dizm':
                bot.send_message(call.message.chat.id, f"Ваше місто: {city}")
            elif call.data=='zminm':
                msg = bot.send_message(call.message.chat.id, """\
Введіть назву міста
""")
                bot.register_next_step_handler(msg, change_city_variable)
    except Exception as e:
        print(repr(e)) 
def change_city_variable(message):
    global city, spost, w
    try:
        city = message.text
        spost = mgr.weather_at_place(city)
        w = spost.weather
        bot.send_message(message.chat.id, "Змінено успішно!\nЩоб змінити назад, натисніть /settings")
    except:
        bot.send_message(message.chat.id, "Помилка! Місто вказано невірно")
        city = standart_city
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == 'Погода':
        bot.send_message(message.chat.id,
        f"""Smak Weather Bot
Відомості про погоду:
Місто: {city} 
Температура: {w.temperature('celsius').get("temp")}°C
Мін. температура: {w.temperature('celsius').get("temp_min")}°C
Макс. температура: {w.temperature('celsius').get("temp_max")}°C
Атм. тиск: {int(w.pressure.get("press") / 1.333)} мм рт. ст.
Вологість: {w.humidity}%
Хмарність: {w.clouds}%
Опади: {w.rain}
Швидкість вітру: {w.wind().get("speed")}
Тепловий індекс: {w.heat_index}
Додатково: {w.detailed_status}
"""
    )
    elif message.text=='Температура':
        bot.send_message(message.chat.id, 
            f"""Температура: {w.temperature('celsius').get('temp')}°C
Відчувається як: {w.temperature('celsius').get('feels_like')}°C"""
    )
    elif message.text=='Вологість':
        bot.send_message(message.chat.id, f"Атмосферна вологість: {w.humidity}%")       
    elif message.text=='Атмосферний тиск':
        bot.send_message(message.chat.id, "Атмосферний тиск: {} мм рт. ст.".format(int(w.pressure.get("press") / 1.333))
    )
if __name__ == "__main__":
    bot.polling(none_stop=True)
