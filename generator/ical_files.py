from datetime import datetime, timedelta

from icalendar import Calendar, Event, vDate, vDatetime, vUri, vGeo

from helper import generate_event_ical_path, remove_tags
from parser import parse_events

# this script generates the event detail pages


def generate_ical_event(event, now):
    cal_event = Event()
    cal_event.add('DTSTAMP', vDatetime(now))
    cal_event.add('SEQUENCE', 0)
    cal_event.add('UID', 'event_{}@foss.events'.format(event['id']))

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

    if event['lat'] and event['lon']:
        cal_event['geo'] = vGeo([event['lat'], event['lon']])

    return cal_event


def generate_event_ical_files(events, now):
    for event in events:
        cal = Calendar()
        cal.add('prodid', '-//foss.events//foss.events//')
        cal.add('version', '2.0')
        cal_event = generate_ical_event(event, now)
        cal.add_component(cal_event)

        filepath = generate_event_ical_path(event)
        with open('build/' + filepath, 'wb') as f:
            f.write(cal.to_ical())


def generate_calendar(events, now):
    cal = Calendar()
    cal.add('prodid', '-//foss.events//foss.events//')
    cal.add('version', '2.0')

    for event in events:
        cal_event = generate_ical_event(event, now)
        cal.add_component(cal_event)

    with open('build/events.ics', 'wb') as f:
        f.write(cal.to_ical())


now = datetime.now()

for year in [2019, 2020, 2021, 2022, 2023]:
    events = parse_events('data/' + str(year) + '_events_db.csv', now)
    generate_event_ical_files(events['all'].values(), now)

events_2022 = parse_events('data/2022_events_db.csv', now)
generate_calendar(events_2022['all'].values(), now)
