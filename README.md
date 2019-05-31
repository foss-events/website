# floss.events website

## Build instructions

### TL;DR

* Install [Hugo (extended)](https://gohugo.io/getting-started/installing/)
* Install [Node.js](https://nodejs.org/en/download/package-manager/)
* Run `npm run serve`
* Open the website in the link provided

### Details

#### Requirements

This website requires [Hugo (extended)](https://gohugo.io/) and
[Node.js](https://nodejs.org/en/download/package-manager/) to build.

#### Building

The idea is to generate Hugo content 
from the [events_db.csv](events_db.csv) 
by running the script [generate_data.csv](scripts/generate_data.js).
The target files go to [content/events](content/events).

If the events_db.csv has been updated the script has to run again.

The entire build workflow looks like that

* clone the project
* install Node dependencies `npm install`
* update the [events_db.csv](events_db.csv) 
* generate the Hugo data via `./scripts/generate_data.js`
* start the Hugo by running `hugo server -D` 
* open the link displayed
