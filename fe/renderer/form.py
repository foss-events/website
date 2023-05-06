from iso639 import iter_langs
import yaml

from generator.helper import create_jinja_env
from generator.consts import iso_3166_countries, supported_languages


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


def render_form(event=None):
    with open("data/fieldspec.yml", "r") as specfile:
        try:
            fieldspec = yaml.safe_load(specfile)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    if not fieldspec:
        print("error loading fieldspec")
        exit(1)

    event_id = "new"

    if event:
        event_id = event["id"]

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

    data = {}

    if event:
        data = event.copy()

        if data["registration"] == "no":
            data["registration"] = ""

        data["main_language"] = event.get("main_language", "").split("/")
        data["main_language"] = list(map(lambda l: l.strip().lower(), data["main_language"]))

        data["type"] = event.get("type", "").split(",")
        data["type"] = list(map(lambda t: t.strip(), data["type"]))

        if not validate_options(field_type, data["type"]):
            print(f"Unknown type(s) {data['type']}")

        if not validate_options(field_presentation_form, [data["presentation_form"]]):
            print(f"Unknown presentation form {data['presentation_form']}")

        data["date_start"] = convert_date(event["date_start"])
        data["date_end"] = convert_date(event["date_end"])
        data["cfp_date"] = convert_date(event["cfp_date"])

    env = create_jinja_env()
    template = env.get_template('form.html')
    result = template.render(
        event_id=event_id,
        fieldspec=fieldspec,
        countries=countries,
        languages=languages,
        data=data,
    )

    return result
