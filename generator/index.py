import csv
from datetime import datetime

from helper import create_jinja_env
from parser import parse_events

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

with open('data/2020_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    events = parse_events(reader, today)

env = create_jinja_env()
template = env.get_template('index.html')
result = template.render(
    upcoming=events['upcoming'],
    has_upcoming=events['has_upcoming'],
    prev=events['prev'],
    has_prev=events['has_prev'],
    year='2020',
    other_year='2019',
    other_year_link='2019'
)
with open('build/index.html', 'a') as f:
    f.write(result)
