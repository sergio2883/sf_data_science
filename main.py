import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN
from extensions import APIException, CurrencyConverter

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)

currencies = {
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB"
}

def send_message(user_id, text):
    vk.method("messages.send", {
        "user_id": user_id,
        "message": text,
        "random_id": 0
    })

print("Бот работает...")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id


        if text in ["/start", "/help"]:
            send_message(user_id, 
                "Чтобы начать работу введите:\n"
                "<имя валюты> <в какую валюту перевести> <количество>\n"
                "Пример:\n"
                "евро доллар 100"
            )


        elif text == "/values":
            values_text = "Доступные валюты:\n"
            for key in currencies.keys():
                values_text += f"{key}\n"
            send_message(user_id, values_text)


        else:
            try:
                values = text.split(" ")
                if len(values) != 3:
                    raise APIException("мало аргументов")
                    #raise APIException("Введите 3 параметра.")


                base, quote, amount = values
                total = CurrencyConverter.get_price(base, quote, amount)
                send_message(user_id, f"{amount} {base} = {total} {quote}")


            except APIException as e:
                send_message(user_id, f"Ошибка пользователя:\n{e}")


            except Exception as e:
                send_message(user_id, f"Не удалось обработать команду:\n{e}")