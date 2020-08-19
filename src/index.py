import telepot
import time
import os
from telepot.loop import MessageLoop
import json
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

# get telegram bot token
with open(os.path.join('..', '..', 'token.txt')) as f:
    bot = telepot.Bot(f.readline())


# to get info about bot delete '#' from next line
# print(bot.getMe())

def send_answer(chat_id, text, reply_markup=''):
    bot.sendMessage(chat_id, text, reply_markup=reply_markup)


with open(os.path.join('data', 'parsed_group_dates.json')) as groups:
    groups_data = json.load(groups)


def register_user(content_type, msg, chat_id):
    user_name = msg['from']['first_name']

    if content_type == 'text':
        if msg['text'] != '/start':
            current_group = ''.join(filter(str.isdigit, msg['text']))
            if len(current_group) == 1:
                current_group = f"60{current_group}"
            elif len(current_group) == 2:
                current_group = f"6{current_group}"

            if len(current_group) == 3 and current_group in groups_data.keys():
                with open(os.path.join("data", "users.json"), "r+", encoding='utf8') as users_storage:
                    users_data = json.load(users_storage)
                    users_data.append({
                        "chat_id": chat_id,
                        "group": current_group,
                        "name": user_name,
                        "role": 'student',
                        "message": ''
                    })
                    users_storage.seek(0)
                    json.dump(users_data, users_storage)
                    run_student_dialogue(content_type, msg, users_data[-1])
            else:
                send_answer(chat_id, f'{user_name}, Вы уверены, что ввели правильный номер группы? '
                                     f'Пожалуйста, введите номер группы')
        else:
            send_answer(chat_id, 'Пожалуйста, введите номер группы ')


def run_student_dialogue(content_type, msg, current_user):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить расписание занятий на весь цикл")],
            [KeyboardButton(text="Получить вопросы к занятию")]
        ]
    )
    if content_type == 'text':
        with open(os.path.join('data', 'lessons.json'), encoding='utf8') as lessons:
            lessons_data = json.load(lessons)

        if msg['text'] == 'Получить расписание занятий на весь цикл':
            send_answer(current_user['chat_id'], '\n'.join([f'{groups_data[current_user["group"]][i]} - {lesson}'
                                                            for i, lesson in enumerate(lessons_data)]))
        elif msg['text'] == 'Получить вопросы к занятию':
            send_answer(current_user['chat_id'], f'Выберите тему занятия', ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=f'{lesson}')] for lesson in lessons_data]
            ))
        elif msg['text'] in lessons_data.keys():
            send_answer(current_user['chat_id'], lessons_data[msg['text']], main_menu)
        else:
            send_answer(current_user['chat_id'], f'{current_user["name"]}! Выберите, что бы Вы хотели узнать',
                        main_menu)


def run_admin_dialogue(content_type, msg, current_user):
    if content_type == 'text':
        with open(os.path.join("data", "users.json"), "r", encoding='utf8') as users_storage:
            users_data = json.load(users_storage)

        if msg['text'] not in groups_data.keys():
            for user in users_data:
                if user['chat_id'] == current_user['chat_id']:
                    user['message'] = msg['text']

            with open(os.path.join("data", "users.json"), "w", encoding='utf8') as users_storage:
                json.dump(users_data, users_storage, ensure_ascii=False)

            send_answer(current_user['chat_id'], f'Выберите группу, которой вы отправляете сообщение',
                        ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text=f'{group}')] for group in groups_data.keys()]
                        ))
        else:
            for user in users_data:
                if user['group'] == msg["text"]:
                    send_answer(user['chat_id'],
                                f'Ваш преподаватель отправил вам следующее сообщение: \n {current_user["message"]}')

            send_answer(current_user['chat_id'], f'Ваше сообщение успешно отправлено выбранной группе.')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    with open(os.path.join('data', 'users.json'), 'r', encoding='utf8') as users_storage:
        users_data = json.load(users_storage)

    current_user = []

    for user in users_data:
        if user['chat_id'] == msg['from']['id']:
            current_user.append(user)

    if len(current_user):
        if current_user[0]['role'] == 'admin':
            run_admin_dialogue(content_type, msg, current_user[0])
        else:
            run_student_dialogue(content_type, msg, current_user[0])
    else:
        register_user(content_type, msg, chat_id)


MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while True:
    time.sleep(10)
