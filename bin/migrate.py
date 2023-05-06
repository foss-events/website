#!/usr/bin/env python3

import csv

from generator.parser import parse_all_events_as_list

events = parse_all_events_as_list()

fieldnames = []

for event in events:
    for field_name in event["raw"].keys():
        if field_name not in fieldnames:
            fieldnames.append(field_name)

fieldnames.append("changed_at")
fieldnames.append("change_email")
fieldnames.append("change_comment")
fieldnames.append("revision")


with open('data/events.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()

    for event in events:
        event["raw"]["revision"] = 1
        writer.writerow(event["raw"])
