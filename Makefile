$(shell mkdir -p build/2019)
$(shell mkdir -p build/2020)
$(shell mkdir -p build/img)
$(shell mkdir -p build/styles)

all: build/index.html build/2020/index.html build/styles/fossevents.css build/img/europe-wo-borders-250a.jpg build/img/logo.png build/img/fossevents_512.png build/img/fossevents_1024.png build/favicon.ico

build/styles/fossevents.css: src/styles/fossevents.css
	cp $< $@

build/img/europe-wo-borders-250a.jpg: src/img/europe-wo-borders-250a.jpg
	cp $< $@

build/img/logo.png: src/img/logo.png
	cp $< $@

build/img/fossevents_512.png: src/img/fossevents_512.png
	cp $< $@

build/img/fossevents_1024.png: src/img/fossevents_1024.png
	cp $< $@

build/favicon.ico: src/img/favicon.ico
	cp $< $@

build/index.html: 2019_events_db.csv
	rm -rf build/index.html
	pipenv run python3 generator/index.py

build/2020/index.html: 2020_events_db.csv
	rm -rf build/2020/index.html
	pipenv run python3 generator/events-2020.py

build/events/token: 2019_events_db.csv 2020_events_db.csv
	rm -rf build/events/*
	pipenv run python3 generator/gen.py
	touch build/events/token

clean:
	rm -rf build
