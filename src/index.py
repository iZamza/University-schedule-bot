import telepot
import time
from telepot.loop import MessageLoop

bot = telepot.Bot('1397222187:AAFoDRbVrr8TdeeuR_UnFIPzC2U9nbF9rFo')


# print(bot.getMe()) get info about bot


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    def send_answer(text):
        bot.sendMessage(chat_id, text)

    if content_type == 'text':
        if msg['text'] == '/start':
            send_answer('Добро пожаловать!')
        elif msg['text'].lower() == 'hi':
            send_answer('Hihihi!')
        else:
            send_answer(f'You type {msg["text"]}')


MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while 1:
    time.sleep(10)
