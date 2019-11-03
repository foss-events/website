import csv
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

months = {
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
    },
    '11': {
        'label': 'November',
        'events': []
    },
    '12': {
        'label': 'December',
        'events': []
    }
}

with open('2019_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        date_start = datetime.strptime(row['datestart'], '%Y%m%d')
        day_start = date_start.strftime('%d')
        month_start = date_start.strftime('%m')
        print('start: ' + month_start)
        event = {
            "label": row['label'],
            "start_day": day_start
        }
        months[month_start]['events'].append(event)

file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')
result = template.render(months=months)
with open("build/index.html", "a") as f:
    f.write(result)
