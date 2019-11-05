all: build/index.html build/events-2020.html build/flossevents.css build/img/europe-wo-borders-250a.jpg build/img/logo.png build/favicon.ico

build/flossevents.css: src/styles/flossevents.css
	mkdir -p build/styles
	cp src/styles/flossevents.css build/styles

build/img/europe-wo-borders-250a.jpg: src/img/europe-wo-borders-250a.jpg
	mkdir -p build/img
	cp src/img/europe-wo-borders-250a.jpg build/img

build/img/logo.png: src/img/logo.png
	mkdir -p build/img
	cp src/img/logo.png build/img

build/favicon.ico: src/img/favicon.ico
	mkdir -p build
	cp src/img/favicon.ico build

build/index.html: 2019_events_db.csv
	mkdir -p build
	rm -rf build/index.html
	pipenv run python3 generator/index.py

build/events-2020.html: 2020_events_db.csv
	mkdir -p build
	rm -rf build/events-2020.html
	pipenv run python3 generator/events-2020.py

build/events/token: 2019_events_db.csv 2020_events_db.csv
	rm -rf build/events/*
	pipenv run python3 generator/gen.py
	touch build/events/token

clean:
	rm -rf build
