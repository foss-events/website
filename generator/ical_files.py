import csv
from datetime import datetime
from icalendar import Calendar, Event, vDate

from helper import generate_event_ical_path
from parser import parse_events

# this script generates the event detail pages

def generate_event_ical_files(events):
    for event in events:

        cal = Calendar()
        cal.add('prodid', '-//foss.events//foss.events//')
        cal.add('version', '1.3.3.7')

        cal_event = Event()
        cal_event.add('summary', event['label'])
        cal_event.add('dtstart', vDate(event['start_date']))
        cal_event.add('dtend', vDate(event['end_date']))

        cal.add_component(cal_event)

        filepath = generate_event_ical_path(event)
        with open('build/' + filepath, 'wb') as f:
            f.write(cal.to_ical())

today = datetime.now()

for year in [2019, 2020]:
    with open('data/' + str(year) + '_events_db.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        events = parse_events(reader, today)
        generate_event_ical_files(events['all'])
