from datetime import datetime

from generator.helper import create_jinja_env, generate_event_details_path
from generator.parser import parse_all_events

env = create_jinja_env()
template = env.get_template("toots.html")


def render_toots():
    events = parse_all_events()

    toots = []

    for event in events.values():
        if not event['upcoming']:
            continue

        cfp = None

        if event["cfp_link"] and not event["cfp_passed"]:
            cfp = event["cfp_date"].strftime('%d.%m.%Y')

        toots.append({
            "label": event["label"],
            "main_organiser": event["main_organiser"],
            "printable_date": event["printable_date"],
            "printable_short_location": event["printable_short_location"],
            "url": "https://foss.events/" + generate_event_details_path(event),
            "hashtags": event["hashtag"],
            "cfp": cfp,
            "mastodon": event["mastodon"],
        })

    return template.render(toots=toots)
