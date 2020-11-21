# University-schedule-bot
Telegram bot for students to get a schedule
---
How to use it
1. Save your bot token in `token.txt` file in folder that has project folder
2. `data\lessons.json` file has lessons like Dict, where lesson topic is `key`: and lesson description (questions) is `value`
3. `data\groups.json` file has available groups, also like a Dict, where group number is `key`: and `value` 
is a string `'%d.%m.%Y-%d.%m.%Y'`, where first is start date, and second - end date.
Before starting you must parse this range into separate working days of week.
It's also simple:
    1. Just run `date_range_maker.py` it return `parsed_group_dates.json` witch will be used in application, 
    if you haven't any messages in console => move forward, in other cases check dates of lessons for group from console
4. For run bot just run `index.py`
5. `data\users.json` file for storing users, after user will be added, you can change role of user to `admin`

---
Plan for making application
- [x] Make a bot, add possibility for register new user and get questions for lessons (till 14.08)
- [x] Add possibility for students to take individual schedule, with dates and topics  (till 21.08)
- [x] Add admin role with possibility to send push notification for some group, test application (till 28.08)
