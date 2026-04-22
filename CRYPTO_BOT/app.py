import telebot


TOKEN = '8640643460:AAHwV7lOxzBn3B6Y07hC1Royi4Mh3khiZhY'


bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',   
}


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
    
    
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'hello')
    
    
bot.polling()