from jinja2 import Template, Environment, FileSystemLoader
import csv

events = []

with open('2019_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        event = {
            "label": row['label']
        }
        events.append(event)


file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')
result = template.render(events=events)
with open("build/index.html", "a") as f:
    f.write(result)

