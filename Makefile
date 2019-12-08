$(shell mkdir -p build/2019 build/2020 build/img build/styles)
SOURCE_IMGS=$(wildcard src/img/*.png) $(wildcard src/img/*.jpg)
TARGET_IMGS=$(subst src,build,$(SOURCE_IMGS))
all: build/.htaccess build/index.html build/2019/index.html build/styles/fossevents.css build/events_token build/favicon.ico $(TARGET_IMGS)

build/img/%: src/img/%
	cp $< $@

build/styles/fossevents.css: src/styles/fossevents.css
	cp $< $@

build/.htaccess: src/.htaccess
	cp $< $@

build/favicon.ico: src/img/favicon.ico
	cp $< $@

build/index.html: 2020_events_db.csv
	pipenv run python3 generator/index.py

build/2019/index.html: 2019_events_db.csv
	pipenv run python3 generator/events-2019.py

build/events_token: 2019_events_db.csv 2020_events_db.csv
	pipenv run python3 generator/event_pages.py
	touch build/events_token

clean:
	rm -rf build
