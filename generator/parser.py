from datetime import datetime
from pprint import pprint

from helper import get_start_of_month, get_end_of_day, generate_event_details_path, generate_event_ical_path
from consts import iso_label_dict, months
from parse_helper import extract_cfp

event_type_class_map = {
    'Global Day': 'event--highlighted',
    'Regional Day': 'event--highlighted'
}

def parse_events(reader, today):

    all_events = []
    upcoming = {}
    prev = {}

    for month_key, month in months.items():
        upcoming[month_key] = {
            'label': month,
            'events': []
        }
        prev[month_key] = {
            'label': month,
            'events': []
        }

    has_upcoming = False
    has_prev = False

    for row in reader:

        if row['approved'] != 'yes':
            continue

        event = parse_event(row, today)

        if event is None:
            continue

        all_events.append(event)
        start_month = event['start_month']

        if event['upcoming']:
            upcoming[start_month]['events'].append(event)
            has_upcoming = True
        else:
            prev[start_month]['events'].append(event)
            has_prev = True

    for month_key,month in upcoming.items():
        month['events'] = sorted(month['events'], key=lambda event: event['start_day'] + event['end_day'])

    for month_key,month in prev.items():
        month['events'] = sorted(month['events'], key=lambda event: event['start_day']  + event['end_day'])

    return {
        'all': all_events,
        'upcoming': upcoming,
        'has_upcoming': has_upcoming,
        'prev': prev,
        'has_prev': has_prev
    }


def parse_event(row, today):

    start_of_month = get_start_of_month(today)
    end_of_today = get_end_of_day(today)

    try:
        start_date = datetime.strptime(row['datestart'], '%Y%m%d')
    except ValueError:
        pprint('error parsing datestart')
        pprint(row)
        return None

    start_day = start_date.strftime('%d')
    start_month = start_date.strftime('%m')
    start_year = start_date.strftime('%Y')

    end_date = datetime.strptime(row['dateend'], '%Y%m%d')
    end_day = end_date.strftime('%d')

    upcoming_event = end_date >= today

    classes = event_type_class_map.get(row['type'], '')

    if row['coclink'] and row['coclink'] != 'nococ':
        coc_link = row['coclink']
    else:
        coc_link = None

    if row['city'] == '--' or not row['city']:
        city = ''
    else:
        city = row['city']

    if row['country'] == '--' or not row['country']:
        country = ''
    else:
        country_code = row['country'].strip()
        country = iso_label_dict.get(country_code, country_code)

    if row['EntranceFee'] != '0':
        fee = row['EntranceFee']
    else:
        fee = None

    if row['ParticipantsLastTime']:
        participants = row['ParticipantsLastTime']
    else:
        participants = '?'

    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
        geo = 'geo:' + str(lat) + ',' + str(lon)
    except:
        lat = None
        lon = None
        geo = None

    cfp = extract_cfp(row, today)

    event = {
        'label': row['label'],
        'description': row['Self-description'],
        'start_date': start_date,
        'start_day': start_day,
        'start_month': start_month,
        'start_month_string': months[start_month],
        'start_year': start_year,
        'end_date': end_date,
        'end_day': end_day,
        'homepage': row['homepage'],
        'fee': fee,
        'venue': row['venue'],
        'city': city,
        'country': country,
        'osm_link': row['OSM-Link'],
        'geo': geo,
        'cfp_date': cfp['cfp_date'],
        'cfp_passed': cfp['cfp_passed'],
        'cfp_link': cfp['cfp_link'],
        'cfp_raw_link': cfp['cfp_raw_link'],
        'coc_link': coc_link,
        'registration': row['Registration'],
        'classes': classes,
        'type': row['type'],
        'upcoming': upcoming_event,
        'participants': participants,
        'lat': lat,
        'lon': lon
    }

    event['ical_path'] = generate_event_ical_path(event)

    readable_location = event['venue']

    if event['venue'] and event['city']:
        readable_location += ', '

    readable_location += event['city']

    if (event['venue'] or event['city']) and event['country']:
        readable_location += ', '

    readable_location += event['country']

    event['readable_location'] = readable_location

    if row['type'] == 'Global Day' or row['type'] == 'Regional Day':
        event['has_details'] = False
        event['details_url'] = row['homepage']
        event['abs_details_url'] = row['homepage']
    else:
        event['has_details'] = True
        event['details_url'] = generate_event_details_path(event)
        event['abs_details_url'] = 'https://foss.events/' + str(event['details_url'])

    return event
