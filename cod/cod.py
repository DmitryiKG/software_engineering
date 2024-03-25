import telebot
from telebot import types
from currency_converter import CurrencyConverter

corrency = CurrencyConverter()
amount = 0
bot = telebot.TeleBot('7038675379:AAEr0PwZxp7vu0_Cca3ktFr1BCXPcH9dnNY')


@bot.message_handler(commands=['start']) # Код для команды /start
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Я помогу вам перевести валюту. Введите вашу сумму.')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip()) # Получаем число от пользователя
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат.')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        m = types.InlineKeyboardMarkup(row_width=1)  # Создаём онлайн-кнопки, row_width - сколько кнопок у нас в строке
        button1 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD') # USD - Доллар США
        button2 = types.InlineKeyboardButton('CNY/JPY', callback_data='CNY/JPY') # JPY - Японская Иена
        button3 = types.InlineKeyboardButton('RUB/CNY', callback_data='RUB/CNY') # CNY - Китайский Юань
        button4 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR') # EUR - Евро
        button5 = types.InlineKeyboardButton('GBP/USD', callback_data='GBP/USD') # GBP - вьетнамский доллар
        button6 = types.InlineKeyboardButton('Пользовательские значения', callback_data='else')
        m   .add(button1, button2, button3, button4, button5, button6) # Добавляем в markup наши кнопки
        bot.send_message(message.chat.id, 'Выберите пару валют (пример валют:EUR – евро, JPY – японская иена, '
                                          'GBP – фунт стерлингов, AUD – австралийский доллар, CNY – китайская юань)',
                         reply_markup=m)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше 0.')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.split('/')
        res = corrency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите валюты через "/"')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = corrency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так.')
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)
