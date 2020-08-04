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
            current_group = ''.join(filter(str.isdigit, msg['text']))
            if len(current_group) == 1:
                current_group = f"60{current_group}"
            elif len(current_group) == 2:
                current_group = f"6{current_group}"

            if len(current_group) == 3:
                with open("users.json", "r+") as users_storage:
                    users_data = json.load(users_storage)
                    users_data.append({
                        "id": msg['from']['id'],
                        "group": current_group,
                        "name": msg['from']['first_name'],
                        "role": 'student',
                        "feedback": []
                    })
                    users_storage.seek(0)
                    json.dump(users_data, users_storage)
                    run_student_dialogue(content_type, msg, chat_id, users_data[-1])
        else:
            send_answer(chat_id, 'Пожалуйста, введите номер группы ')


def send_answer(chat_id, text, reply_markup=''):
    bot.sendMessage(chat_id, text, reply_markup=reply_markup)


def run_student_dialogue(content_type, msg, chat_id, current_user):
    print(current_user)
    if content_type == 'text':
        if msg['text'] == 'bla':
            print('bla')
        else:
            keyboard_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Получить расписание")],
                    [KeyboardButton(text="Узнать тему занятия на завтра")],
                    [KeyboardButton(text="Узнать тему занятия на сегодня")],
                    [KeyboardButton(text="Оставить отзыв")]
                ]
            )
            send_answer(chat_id, 'Добро пожаловать! Пожалуйста, выбирите ', keyboard_markup)


def run_admin_dialogue(content_type, msg, chat_id, current_user):
    print(current_user)
    if content_type == 'text':
        if msg['text'] == 'bla':
            print('bla')
        else:
            keyboard_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Отправить пушку!")],
                ]
            )
            send_answer(chat_id, 'Жги, админ!', keyboard_markup)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    with open('users.json') as users_storage:
        users_data = json.load(users_storage)

    current_user = []

    for user in users_data:
        if user['id'] == msg['from']['id']:
            current_user.append(user)

    if len(current_user):
        if current_user[0]['role'] == 'admin':
            run_admin_dialogue(content_type, msg, chat_id, current_user[0])
        else:
            run_student_dialogue(content_type, msg, chat_id, current_user[0])
    else:
        register_user(content_type, msg, chat_id)


MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while 1:
    time.sleep(10)
