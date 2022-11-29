import telebot
from telebot import types
from config import keys, TOKEN
from extensions import APIException, MoneyConverter

def create_markup(quote = None):
    conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != quote:
            buttons.append(types.KeyboardButton(val.capitalize()))

    conv_markup.add(*buttons)
    return conv_markup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте! Я конвертер валют. Чтобы начать выберите:\n<имя валюты> \
<в какую валюту перевести> \
<введите количество переводимой валюты>\nЧтобы начать, нажмите /conver'
    bot.reply_to(message, text)

@bot.message_handler(commands=['conver'])
def values(message: telebot.types.Message):
    text = 'Выберете валюту, какую хотите конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup= create_markup())
    bot.register_next_step_handler(message, quote_handler)

def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().lower()
    text = 'Выберете валюту, в которую хотите конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup= create_markup(quote))
    bot.register_next_step_handler(message, base_handler, quote)

def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip().lower()
    text = 'Введите колличество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = MoneyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)