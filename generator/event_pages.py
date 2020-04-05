import csv
from datetime import datetime

from helper import create_jinja_env, generate_event_details_path
from parser import parse_events

# this script generates the event detail pages

env = create_jinja_env()
template = env.get_template('event.html')


def generate_event_pages(events, year):
    for event in events:
        result = template.render(
            event=event,
        )

        filepath = generate_event_details_path(event)
        with open('build/' + filepath, 'w') as f:
            f.write(result)


today = datetime.now()

for year in [2019, 2020]:
    events = parse_events('data/' + str(year) + '_events_db.csv', today)
    generate_event_pages(events['all'], year)
