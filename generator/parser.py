import csv
import io
import sys
from datetime import datetime
from pprint import pprint

from helper import get_start_of_month, get_end_of_day, generate_event_details_path, generate_event_ical_path
from consts import iso_3166_countries, months
from parse_helper import extract_cfp, extract_meta_keywords, translate_iso639_code2name

event_type_class_map = {
    'Global Day': 'event--highlighted',
    'Regional Day': 'event--highlighted'
}


def open_file(path):
    with open(path) as file:
        file_content = file.read()

        # fix quotes
        file_content = file_content.replace('”', '\"')
        file_content = file_content.replace('“', '\"')

        content_io = io.StringIO(file_content)
        return csv.DictReader(content_io, delimiter='\t')


def parse_all_events():
    """
    :return: dict containing all events by id
    """
    today = datetime.now()
    events2019 = parse_events('data/2019_events_db.csv', today)
    events2020 = parse_events('data/2020_events_db.csv', today)
    events2021 = parse_events('data/2021_events_db.csv', today)
    return {**events2019['all'], **events2020['all'], **events2021['all']}


def parse_events(file_path, today):

    reader = open_file(file_path)

    all_events = {}
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

        try:
            event = parse_event(row, today)
        except:
            print('Error parsing event ' + row.get('label', 'n/a'))
            print(sys.exc_info())
            event = None

        if event is None:
            continue

        event_id = event['id']
        all_events[event_id] = event
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
    end_month = end_date.strftime('%m')
    end_year = end_date.strftime('%Y')

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
        country = iso_3166_countries.get(country_code, country_code)

    if not row.get('Main language', None) or row.get('Main language') == "?":
        has_language_info = False
        main_language = ""
        main_language_string = ""
    else:
        has_language_info = True
        main_language = row.get('Main language')

        languages = main_language.split("/")
        iso_language_names = [translate_iso639_code2name(lang) for lang in languages]
        main_language_string = "/".join(iso_language_names)

    if row['EntranceFee'] != '0':
        fee = row['EntranceFee']
    else:
        fee = None

    if row['ParticipantsLastTime']:
        participants = row['ParticipantsLastTime']
    else:
        participants = '?'

    if row.get('Mastodon', '').startswith('http'):
        mastodon = row.get('Mastodon')
    else:
        mastodon = None

    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
        geo = 'geo:' + str(lat) + ',' + str(lon)
    except:
        lat = None
        lon = None
        geo = None

    cfp = extract_cfp(row, today)

    main_organiser = row.get('Main Organiser', None)
    if main_organiser == "?":
        main_organiser = None

    event = {
        'id': row['id'],
        'label': row['label'],
        'name': row['name'],
        'shortname': row.get('shortname', None),
        'online': row.get('presentation form', None) == 'online',
        'onlinebanner': row.get('onlinebanner', None),
        'editions_topic': row.get('Edition’s Topic', None),
        'main_organiser': main_organiser,
        'description': row['Self-description'],
        'specialities': row.get('Specialties', None),
        'cancelled': row.get('cancelled', None) == 'cancelled',
        'postponed': row.get('cancelled', None) == 'postpone',
        'replacement': row.get('replacement', None),
        'replaces': row.get('replaces', None),
        'only_online': row.get('cancelled', None) == 'online',
        'cancellation_description': row.get('cancellation_description', None),
        'start_date': start_date,
        'start_day': start_day,
        'start_month': start_month,
        'start_month_string': months[start_month],
        'start_year': start_year,
        'end_date': end_date,
        'end_day': end_day,
        'end_month': end_month,
        'end_month_string': months[end_month],
        'end_year': end_year,
        'homepage': row['homepage'],
        'fee': fee,
        'venue': row['venue'],
        'city': city,
        'country': country,
        'osm_link': row['OSM-Link'],
        'geo': geo,
        'has_language_info': has_language_info,
        'main_language': main_language,
        'main_language_string': main_language_string,
        'cfp_date': cfp['cfp_date'],
        'cfp_passed': cfp['cfp_passed'],
        'cfp_link': cfp['cfp_link'],
        'cfp_raw_link': cfp['cfp_raw_link'],
        'coc_link': coc_link,
        'registration': row['Registration'],
        'timezone': row.get('Timezone', None),
        'classes': classes,
        'type': row.get('type', '?'),
        'upcoming': upcoming_event,
        'participants': participants,
        'lat': lat,
        'lon': lon,
        'first_edition': row.get('First Edition', None),
        'main_sponsors': row.get('Main Sponsors', None),
        'tags': row.get('tags', None),
        'tech_in_use': row.get('Technologies in use', None),
        'interactivity': row.get('Online Interactivity', None),
        'technical_liberties': row.get('Technical Liberties', None),
        'mastodon': row.get('Mastodon', None),
        "matrix": row.get('Matrix', None),
        "mailinglist": row.get('Mailinglist', None),
        "hashtag": row.get('hashtag', None),
    }

    printable_date = ""

    if event["start_year"] != event["end_year"]:
        printable_date = event["start_day"] + " " + event["start_month_string"] + " " + event["start_year"] + " - "
    elif event["start_month"] != event["end_month"]:
        printable_date = event['start_day'] + " " + event['start_month_string'] + " - "
    elif event["start_day"] != event["end_day"]:
        printable_date = event["start_day"] + "-"

    printable_date = printable_date + event["end_day"] + " " + event["end_month_string"] + " " + event["end_year"]
    event["printable_date"] = printable_date

    event['ical_path'] = generate_event_ical_path(event)

    printable_short_location = event["city"]

    if event["city"] and event["country"]:
        printable_short_location = printable_short_location + ", " + event["country"]

    event["printable_short_location"] = printable_short_location

    readable_location = event['venue']

    if event['venue'] and event['city']:
        readable_location += ', '

    readable_location += event['city']

    if (event['venue'] or event['city']) and event['country']:
        readable_location += ', '

    readable_location += event['country']

    if event['venue'] and event['online']:
        readable_location = event['venue']

    event['readable_location'] = readable_location

    if row['type'] == 'Global Day' or row['type'] == 'Regional Day':
        event['has_details'] = False
        event['details_url'] = row['homepage']
        event['abs_details_url'] = row['homepage']
    else:
        event['has_details'] = True
        event['details_url'] = generate_event_details_path(event)
        event['abs_details_url'] = 'https://foss.events/' + str(event['details_url'])

    if event['cancelled'] or event['postponed']:
        event['cfp_date'] = None
        event['cfp_link'] = None
        event['cfp_passed'] = None

    meta_keywords = extract_meta_keywords(row)
    keyword_sep = ', '
    event['keywords_string'] = keyword_sep.join(meta_keywords)

    return event
