$(shell mkdir -p build/2019 build/2020 build/img build/js build/styles/images)
SOURCE_IMGS=$(wildcard src/img/*.png) $(wildcard src/img/*.jpg)
TARGET_IMGS=$(subst src,build,$(SOURCE_IMGS))

all: css js img build/.htaccess build/index.html build/2019/index.html build/events_token

.PHONY: css
css: build/styles/fossevents.css build/styles/leaflet.css build/styles/images/marker-icon.png build/styles/images/marker-icon-2x.png build/styles/images/marker-shadow.png

.PHONY: js
js: build/js/event.js build/js/leaflet.js

.PHONY: img
img: build/favicon.ico $(TARGET_IMGS)

build/img/%: src/img/%
	cp $< $@

build/styles/fossevents.css: src/styles/fossevents.css
	cp $< $@

build/styles/leaflet.css: src/lib/leaflet/leaflet.css
	cp $< $@

build/styles/images/marker-icon.png: src/lib/leaflet/images/marker-icon.png
	cp $< $@

build/styles/images/marker-icon-2x.png: src/lib/leaflet/images/marker-icon-2x.png
	cp $< $@

build/styles/images/marker-shadow.png: src/lib/leaflet/images/marker-shadow.png
	cp $< $@

build/js/event.js: src/js/event.js
	cp $< $@

build/js/leaflet.js: src/lib/leaflet/leaflet.js
	cp $< $@

build/.htaccess: src/.htaccess
	cp $< $@

build/favicon.ico: src/img/favicon.ico
	cp $< $@

build/index.html: data/2020_events_db.csv
	pipenv run python3 generator/index.py

build/2019/index.html: data/2019_events_db.csv
	pipenv run python3 generator/index_2019.py

build/events_token: data/2019_events_db.csv data/2020_events_db.csv
	pipenv run python3 generator/event_pages.py
	touch build/events_token

.PHONY: clean
clean:
	rm -rf build/*
