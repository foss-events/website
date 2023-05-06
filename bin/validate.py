#!/usr/bin/env python3

from pprint import pprint
import sys

import yaml

from generator.parser import open_file

data_file = sys.argv[1]

with open("data/fieldspec.yml", "r") as specfile:
    try:
        fieldspec = yaml.safe_load(specfile)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

if not fieldspec:
    print("error loading fieldspec")
    exit(1)

fieldnames = []

for section in fieldspec["sections"]:
    for field in section["fields"]:
        fieldnames.append(field["name"])

reader = open_file(data_file)

for row in reader:
    csv_names = row.keys()
    break

field_diff = csv_names - fieldnames
print(field_diff)
