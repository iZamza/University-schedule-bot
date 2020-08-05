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
    user_name = msg['from']['first_name']
    with open('groups.json') as groups:
        groups_data = json.load(groups)

    if content_type == 'text':
        if msg['text'] != '/start':
            current_group = ''.join(filter(str.isdigit, msg['text']))
            if len(current_group) == 1:
                current_group = f"60{current_group}"
            elif len(current_group) == 2:
                current_group = f"6{current_group}"

            if len(current_group) == 3 and current_group in groups_data.keys():
                with open("users.json", "r+") as users_storage:
                    users_data = json.load(users_storage)
                    users_data.append({
                        "id": msg['from']['id'],
                        "group": current_group,
                        "name": user_name,
                        "role": 'student'
                    })
                    users_storage.seek(0)
                    json.dump(users_data, users_storage)
                    run_student_dialogue(content_type, msg, chat_id, users_data[-1])
            else:
                send_answer(chat_id, f'{user_name}, Вы уверены, что ввели правильный номер группы? '
                                     f'Пожалуйста, введите номер группы')
        else:
            send_answer(chat_id, 'Пожалуйста, введите номер группы ')


def send_answer(chat_id, text, reply_markup=''):
    bot.sendMessage(chat_id, text, reply_markup=reply_markup)


def run_student_dialogue(content_type, msg, chat_id, current_user):
    if content_type == 'text':
        with open('lessons.json', encoding='utf8') as lessons:
            lessons_data = json.load(lessons)

        if msg['text'] == 'Получить расписание занятий на весь цикл':
            send_answer(chat_id, '1. занятие тогда-то')

        if msg['text'] in lessons_data.keys():
            send_answer(chat_id, lessons_data[msg['text']])

        if msg['text'] == 'Получить вопросы к занятию':
            lessons_list = []
            for lesson in lessons_data:
                lessons_list.append([KeyboardButton(text=f'{lesson}')])
            keyboard_markup = ReplyKeyboardMarkup(
                keyboard=lessons_list
            )
            send_answer(chat_id, f'{current_user["name"]}! Выберите тему занятия', keyboard_markup)
        else:
            keyboard_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Получить расписание занятий на весь цикл")],
                    [KeyboardButton(text="Получить вопросы к занятию")]
                ]
            )
            send_answer(chat_id, f'{current_user["name"]}! Выберите, что бы Вы хотели узнать', keyboard_markup)


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
