from jinja2 import Template
import csv

template = Template('Hello {{ name }}!')
result = template.render(name='John Doe')
print(result)

with open('2019_events_db.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        with open("build/events/" + row['label'].replace('/', '-') + ".html", "a") as f:
            f.write(row['label'])
        # print(row['label'])
