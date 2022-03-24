import telebot
from config import values, TOKEN
from extensions import APIException, get_price

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <Валюта> \
<Валюта для перевода> <Количество> \n \
Валюты нужно указывать с большой буквы! \n \
Доступные валюты: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def currency_ (message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in values.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types  = ['text'])
def convert (message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    

bot.polling()