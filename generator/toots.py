from datetime import datetime

from helper import create_jinja_env, generate_event_details_path
from parser import parse_events

env = create_jinja_env()
template = env.get_template("toots.html")

now = datetime.now()
events = parse_events('data/2023_events_db.csv', now)

toots = []

for event in events["all"].values():
    if not event['upcoming']:
        continue

    cfp = None

    if event["cfp_link"] and not event["cfp_passed"]:
        cfp = event["cfp_date"].strftime('%d.%m.%Y')

    print(event["label"])
    toots.append({
        "label": event["label"],
        "main_organiser": event["main_organiser"],
        "printable_date": event["printable_date"],
        "printable_short_location": event["printable_short_location"],
        "url": "https://foss.events/" + generate_event_details_path(event),
        "hashtags": event["hashtag"],
        "cfp": cfp,
    })

with open("build/toots.html", "w") as f:
    rendered = template.render(toots=toots)
    f.write(rendered)
