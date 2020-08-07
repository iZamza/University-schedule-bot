from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from datetime import datetime
import json


def date_range(start_date, end_date):
    return list(rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR)))


parsed_group_dates = {}

with open('groups.json') as groups_list:
    groups = json.load(groups_list)

for group in groups:
    current_group_dates = groups[group].split(', ')
    group_start_date = datetime.strptime(current_group_dates[0], '%d-%m-%Y')
    group_end_date = datetime.strptime(current_group_dates[1], '%d-%m-%Y')
    parsed_group_dates[group] = [date.strftime('%d-%m-%Y') for date in date_range(group_start_date, group_end_date)]

with open('parsed_group_dates.json', 'w') as parsed_dates:
    json.dump(parsed_group_dates, parsed_dates, indent=2)
