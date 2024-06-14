from telebot import TeleBot
from app.settings import BOT_TOKEN
from app.db import *


bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    content = message.text.split()
    if len(content) == 1:
        bot.send_message(message.chat.id, "Пожалуйста, перейдите по ссылке из вашего личного кабинета для регистрации")
        return
    r.set(content[1], message.chat.id)
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")


if __name__ == "__main__":
    bot.polling()