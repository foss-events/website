#!/usr/bin/env python3

import sys

from iso639 import iter_langs
import yaml

from .helper import create_jinja_env
from .consts import iso_3166_countries, supported_languages
from generator.parser import open_file

with open("data/fieldspec.yml", "r") as specfile:
    try:
        fieldspec = yaml.safe_load(specfile)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

if not fieldspec:
    print("error loading fieldspec")
    exit(1)

for section in fieldspec["sections"]:
    for field in section["fields"]:
        if field["name"] == "type":
            field_type = field
        if field["name"] == "presentation_form":
            field_presentation_form = field

countries = [
    {
        "value": "",
        "label": "Please select",
    },
]

for key, value in iso_3166_countries.items():
    countries.append({
        "value": key,
        "label": value,
    })

languages = [
    {
        "value": "",
        "label": "Please select",
    },
    {
        "value": "?",
        "label": "Unknown",
    },
    {
        "value": "Universal picture language",
        "label": "Universal picture language",
    },
]

for language in iter_langs():
    if language.pt1 not in supported_languages:
        continue

    languages.append({
        "value": language.pt1,
        "label": language.name,
    })

db_file = None
event_id = None

if len(sys.argv) >= 3:
    db_file = sys.argv[1]
    event_id = sys.argv[2]

data = {}


def convert_date(input):
    if not input:
        return

    return input[0:4] + "-" + input[4:6] + "-" + input[6:]


def validate_options(field, data):
    for value in data:
        value_found = False

        for option in field["options"]:
            if value == option["value"]:
                value_found = True
                break

        if not value_found:
            return False

    return True


if db_file and event_id:
    reader = open_file(db_file)

    for row in reader:
        if row["id"] == event_id:
            raw_data = row
            break

    if not raw_data:
        print("Event not found")
        exit(1)

    data = raw_data.copy()
    data["main_language"] = raw_data.get("main_language", "").split("/")
    data["main_language"] = list(map(lambda l: l.strip().lower(), data["main_language"]))

    data["type"] = raw_data.get("type", "").split(",")
    data["type"] = list(map(lambda t: t.strip(), data["type"]))

    if not validate_options(field_type, data["type"]):
        print(f"Unknown type(s) {data['type']}")

    if not validate_options(field_presentation_form, [data["presentation_form"]]):
        print(f"Unknown presentation form {data['presentation_form']}")

    data["date_start"] = convert_date(raw_data["date_start"])
    data["date_end"] = convert_date(raw_data["date_end"])
    data["cfp_date"] = convert_date(raw_data["cfp_date"])

env = create_jinja_env()
template = env.get_template('form.html')
result = template.render(
    fieldspec=fieldspec,
    countries=countries,
    languages=languages,
    data=data,
)

with open("build/form.html", "w") as f:
    f.write(result)
