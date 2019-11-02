all: build/index.html build/flossevents.css build/img/europe-wo-borders-250a.jpg

build/flossevents.css: src/styles/flossevents.css
	mkdir -p build/styles
	cp src/styles/flossevents.css build/styles

build/img/europe-wo-borders-250a.jpg: src/img/europe-wo-borders-250a.jpg
	mkdir -p build/img
	cp src/img/europe-wo-borders-250a.jpg build/img

build/index.html: 2019_events_db.csv
	mkdir -p build
	rm -rf build/index.html
	python generator/index.py

build/events/token: 2019_events_db.csv
	rm -rf build/events/*
	python generator/gen.py
	touch build/events/token

clean:
	rm -rf build

