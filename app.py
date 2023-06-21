import telebot
from config import dict, Token
from extensions import CryptoConverter, ConvertionException
bot = telebot.TeleBot(Token)





@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'In order to use the bot follow the instructions:\n (name of currency)\n' \
           ' (desirable currency)\n' \
           ' (the amount)\n to see the list of all currencies: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'accessible currencies: '
    for d in dict.keys():
        text = '\n'.join((text, d))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('too many parameters')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'user"s error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'cannot handle the request\n{e}')
    else:
        text = f'price {amount} {quote} in {base} - {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()
