import csv
from datetime import datetime

from helper import create_jinja_env, generate_event_details_path
from parser import parse_events, parse_all_events

# this script generates the event detail pages

env = create_jinja_env()
template = env.get_template('event.html')


def generate_event_pages(events, all_events):
    for event in events:
        result = template.render(
            event=event,
            all_events=all_events
        )

        filepath = generate_event_details_path(event)
        with open('build/' + filepath, 'w') as f:
            f.write(result)


all_events = parse_all_events()
today = datetime.now()

for year in [2019, 2020, 2021]:
    events = parse_events('data/' + str(year) + '_events_db.csv', today)
    generate_event_pages(events['all'].values(), all_events)
