import csv
from datetime import datetime, timedelta

from icalendar import Calendar, Event, vDate, vUri, vGeo

from helper import generate_event_ical_path, remove_tags
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

        cal_end_date = event['end_date'] + timedelta(days=1)
        cal_event.add('dtend', vDate(cal_end_date))

        cal_event.add('location', event['readable_location'])
        cal_event.add('url', vUri(event['abs_details_url']))

        description = event['description'] or ''
        description += '\n\n'

        if event['has_details']:
            description += 'Read everything about ' + event['label'] + ' in a nutshell on // foss.events: ' + event['abs_details_url'] + '\n\n'

        description += 'Official Homepage: ' + event['homepage'] + '\n\n'

        if event['osm_link']:
            description += 'Find your way: ' + event['osm_link'] + '\n'

        cal_event['description'] = remove_tags(description)

        cal.add_component(cal_event)

        if event['lat'] and event['lon']:
            cal_event['geo'] = vGeo([event['lat'], event['lon']])

        filepath = generate_event_ical_path(event)
        with open('build/' + filepath, 'wb') as f:
            f.write(cal.to_ical())

today = datetime.now()

for year in [2019, 2020]:
    with open('data/' + str(year) + '_events_db.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        events = parse_events(reader, today)
        generate_event_ical_files(events['all'])
