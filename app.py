import csv
import time

from flask import abort, Flask, request
from jinja2 import Environment, FileSystemLoader

from fe.renderer.index import render_index
from fe.renderer.form import render_form
from generator.helper import generate_event_details_path
from generator.helper import create_jinja_env
from generator.parser import parse_all_events
from generator.parser import load_event_revisions
from fe.renderer.toots import render_toots

app = Flask(
    __name__,
    static_url_path="",
    static_folder="build",
)


@app.get('/')
def handle_index():
    return render_index()


@app.get('/<int:year>/')
def handle_index_year(year, slash):
    return render_index(year)


@app.get("/toots.html")
def handle_get_toots():
    return render_toots()


@app.get("/about.html")
def handle_about():
    file_loader = FileSystemLoader("src/templates")
    env = Environment(loader=file_loader)
    template = env.get_template("about.html")
    result = template.render()
    return result


@app.get('/<int:year>/<event>.html')
def handle_event_page(year, event):
    path = request.path
    events = parse_all_events()
    event = None

    for maybe_event in events.values():
        event_path = "/" + generate_event_details_path(maybe_event)

        if event_path == path:
            event = maybe_event
            break

    if not event:
        abort(404)

    env = create_jinja_env()
    template = env.get_template('event.html')
    result = template.render(
        event=event,
        all_events=[]
    )

    return result


@app.get("/event/<event_id>/edit")
def handle_edit_event(event_id):
    if event_id == "new":
        data = {}
    else:
        events = parse_all_events()

        if event_id not in events:
            abort(404)

        data = events[event_id]["raw"]

    return render_form(data)


@app.get("/event/<event_id>/revisions")
def handle_event_revisions(event_id):
    revisions = load_event_revisions(event_id)

    if len(revisions) == 0:
        abort(404, "event not found")

    revisions_raw = []

    for revision in revisions:
        revisions_raw.append(revision["raw"])

    return revisions_raw


@app.get("/event/<event_id>/revisions/<revision_index>/approve")
def handle_activate_revision(event_id, revision_index):
    # if len(revisions) == 0:
    #     abort(404, "event not found")
    #
    # if len(revisions) < revision_index + 1:
    #     abort(404, "revision not found")

    return "ok"


@app.post("/event/<event_id>/save")
def handle_save_event(event_id):
    data = request.values.copy()
    revisions = load_event_revisions(event_id)

    main_languages = request.form.getlist("main_language")
    data["main_language"] = "/".join(main_languages)

    presentation_form = request.form.getlist("presentation_form")
    data["presentation_form"] = ",".join(presentation_form)

    event_type = request.form.getlist("type")
    data["type"] = ",".join(event_type)

    if data["date_start"]:
        data["date_start"] = data["date_start"].replace("-", "")

    if data["date_end"]:
        data["date_end"] = data["date_end"].replace("-", "")

    if data["cfp_date"]:
        data["cfp_date"] = data["cfp_date"].replace("-", "")

    if len(revisions) == 0:
        abort(404, "event not found")

    if event_id != "new":
        data["id"] = event_id
    else:
        data["id"] = int(time.time())

    data["approved"] = "no"
    data["revision"] = len(revisions) + 1

    with open('data/events.csv', 'a') as csvfile:
        fieldnames = revisions[0]["raw"].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writerow(data)

    return "ok"
