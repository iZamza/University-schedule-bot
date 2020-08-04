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


def register_user(content_type, msg, chat_id):
    if content_type == 'text':
        if msg['text'] != '/start':
            print(msg)
            current_group = ''.join(filter(str.isdigit, msg['text']))
            if len(current_group) == 1:
                current_group = f"60{current_group}"
            elif len(current_group) == 2:
                current_group = f"6{current_group}"
            with open("users.json", "r+") as users_storage:
                users_data = json.load(users_storage)
                users_data.append({
                    "user_id": msg['from']['id'],
                    "user_group": current_group,
                    "user_name": msg['from']['first_name'],
                    "user_feedback": []})
                users_storage.seek(0)
                json.dump(users_data, users_storage)
            run_application(content_type, msg, chat_id)
        else:
            send_answer(chat_id, 'Пожалуйста, введите номер группы ')


def send_answer(chat_id, text, reply_markup=''):
    bot.sendMessage(chat_id, text, reply_markup=reply_markup)


def run_application(content_type, msg, chat_id):
    if content_type == 'text':
        keyboard_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Получить расписание")],
                [KeyboardButton(text="Узнать тему занятия на завтра")],
                [KeyboardButton(text="Узнать тему занятия на сегодня")],
                [KeyboardButton(text="Оставить отзыв")]
            ]
        )
        send_answer(chat_id, 'Добро пожаловать! Пожалуйста, выбирите ', keyboard_markup)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    with open('users.json') as users_storage:
        users_data = json.load(users_storage)

    current_user = []

    for user in users_data:
        if user['user_id'] == msg['from']['id']:
            current_user.append(user)

    if len(current_user):
        run_application(content_type, msg, chat_id)
    else:
        register_user(content_type, msg, chat_id)


MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while 1:
    time.sleep(10)
