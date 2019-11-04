import csv
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

now = datetime(2019, 11, 1, 0, 0, 0)

iso_label_dict = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'BY': 'Belarus',
    'CH': 'Switzerland',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'ES': 'Spain',
    'FR': 'France',
    'GR': 'Greece',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IT': 'Italy',
    'KO': 'Kosova',
    'NL': 'the Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SQ': 'Albania',
    'UK': 'UK'
}

upcoming = {
    '11': {
        'label': 'November',
        'events': []
    },
    '12': {
        'label': 'December',
        'events': []
    }
}

prev = {
    '01': {
        'label': 'January',
        'events': []
    },
    '02': {
        'label': 'February',
        'events': []
    },
    '03': {
        'label': 'March',
        'events': []
    },
    '04': {
        'label': 'April',
        'events': []
    },
    '05': {
        'label': 'May',
        'events': []
    },
    '06': {
        'label': 'June',
        'events': []
    },
    '07': {
        'label': 'July',
        'events': []
    },
    '08': {
        'label': 'August',
        'events': []
    },
    '09': {
        'label': 'September',
        'events': []
    },
    '10': {
        'label': 'October',
        'events': []
    }
}

with open('2019_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        start_date = datetime.strptime(row['datestart'], '%Y%m%d')
        start_day = start_date.strftime('%d')
        start_month = start_date.strftime('%m')

        end_date = datetime.strptime(row['dateend'], '%Y%m%d')
        end_day = end_date.strftime('%d')

        upcoming_event = start_date > now

        if row['city'] == '--' or not row['city']:
            city = ''
        else:
            city = row['city']

        if row['country'] == '--' or not row['country']:
            country = ''
        else:
            country_code = row['country'].strip()
            country = iso_label_dict.get(country_code, country_code)

        if upcoming_event:
            print(row['label'])
            print(row['cfplink'])
            cfp_link = row['cfplink']

            if row['cfpdate']:
                if row['cfpdate'] == 'open':
                    cfp_date = None
                else:
                    cfp_date = datetime.strptime(row['cfpdate'], '%Y%m%d')
        else:
            cfp_date = None
            cfp_link = None

        event = {
            'label': row['label'],
            'start_day': start_day,
            'end_day': end_day,
            'homepage': row['homepage'],
            'city': city,
            'country': country,
            'cfp_date': cfp_date,
            'cfp_link': cfp_link
        }

        if upcoming_event:
            upcoming[start_month]['events'].append(event)
        else:
            prev[start_month]['events'].append(event)

file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')
result = template.render(upcoming=upcoming, prev=prev)
with open('build/index.html', 'a') as f:
    f.write(result)
