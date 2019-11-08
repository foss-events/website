import csv
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from parser import parse_events

today = datetime.now()

with open('2020_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    events = parse_events(reader, today, False)

file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')
result = template.render(
    upcoming=events['upcoming'],
    prev=events['prev'], year='2020',
    other_year='2019',
    other_year_link='/'
)

target_dir = 'build/2020'
target_file = target_dir + '/index.html'

os.makedirs(target_dir, exist_ok=True)

with open(target_file, 'a') as f:
    f.write(result)
