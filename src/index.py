import telepot
import time
import os
from telepot.loop import MessageLoop
import json
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

# get telegram bot token
current_dir = os.curdir
with open(os.path.join('..', '..', 'token.txt')) as f:
    bot = telepot.Bot(f.readline())

# to get info about bot delete '#' from next line
# print(bot.getMe())


def send_answer(chat_id, text, reply_markup=''):
        bot.sendMessage(chat_id, text, reply_markup=reply_markup)

def run_application(content_type, msg, chat_id):
    if content_type == 'text':
        if msg['text'] == '/start':
            keyboard_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Получить расписание")],
                    [KeyboardButton(text="Узнать тему занятия на завтра")],
                    [KeyboardButton(text="Узнать тему занятия на сегодня")],
                    [KeyboardButton(text="Оставить отзыв")]
                ]
            )
            send_answer(chat_id, 'Добро пожаловать! Пожалуйста, выбирите ', keyboard_markup)
        elif msg['text'] == 'Получить расписание':
            send_answer(chat_id, 'Следующее занятие 01.09. Тема: введение в сосудистую хирургию')
        elif msg['text'] == 'Узнать тему занятия на завтра':
            send_answer(chat_id, 'Тема: введение в сосудистую хирургию')
        elif msg['text'] == 'Узнать тему занятия на сегодня':
            send_answer(chat_id, 'Тема: Варикозное расширение вен нижних конечностей')
        else:
            send_answer(chat_id, f'You type {msg["text"]}')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)

    with open('users.json') as users_storage:
        users_data = json.load(users_storage)

    for user in users_data:
        if user['user_id'] == msg['from']['id']:
            run_application(content_type, msg, chat_id)


MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while 1:
    time.sleep(10)
