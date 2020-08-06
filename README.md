# University-schedule-bot
Telegram bot for students to get a schedule
---
How to use it (All part of readme will be update)
1. Save your bot token in `token.txt` file in folder that has project folder
2. `Lessons.json` file has lessons like Dict, where lesson topic is `key`: and lesson description is `value`
3. `Groups.json` file has available groups, also like a Dict, where group number is `key`: and `value` 
is a string `'%d-%m-%Y,%d-%m-%Y'`, where first is start date, and second - end date.
Before starting you must parse this range into separate working days of week.
It's also simple:
    1. Just run `date_range_maker.py` it return `parsed_group_dates.json` witch will be used in application
4. `Users.json` file for storing users

---
Plan for making application
- [x] Make a bot, add possibility for register new user and get questions for lessons (till 14.08)
- [ ] Add possibility for students to take individual schedule, with dates and topics, and if 
student is on training add possibility to take question for today and tomorrow lessons  (till 21.08)
- [ ] Add admin role with possibility to send push notification, test application (till 28.08)

