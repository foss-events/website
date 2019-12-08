$(shell mkdir -p build/2019)
$(shell mkdir -p build/img)
$(shell mkdir -p build/styles)
SOURCE_IMGS=$(wildcard src/img/*.png) $(wildcard src/img/*.jpg)
TARGET_IMGS=$(subst src,build,$(SOURCE_IMGS))
all: build/.htaccess build/index.html build/2019/index.html build/styles/fossevents.css  build/favicon.ico $(TARGET_IMGS)

build/img/%: src/img/%
	cp $< $@

build/styles/fossevents.css: src/styles/fossevents.css
	cp $< $@

build/.htaccess: src/.htaccess
	cp $< $@

build/favicon.ico: src/img/favicon.ico
	cp $< $@

build/index.html: 2020_events_db.csv
	rm -rf build/index.html
	pipenv run python3 generator/index.py

build/2019/index.html: 2019_events_db.csv
	rm -rf build/2019/index.html
	pipenv run python3 generator/events-2019.py

build/events/token: 2019_events_db.csv 2020_events_db.csv
	rm -rf build/events/*
	pipenv run python3 generator/gen.py
	touch build/events/token

clean:
	rm -rf build
