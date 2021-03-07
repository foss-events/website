$(shell mkdir -p build/2019 build/2020 build/2021 build/img/eventlogos/2020 build/img/eventbanners/2020 build/js build/styles/images)
$(shell mkdir -p build/img/eventbanners/2020 build/img/eventbanners/2021)
# here is the import of all images from src/img into the build process, see https://github.com/foss-events/website/pull/179/commits/b695c04ec9eecf9dbda4efe0646cc592a8c746ef
SOURCE_IMGS=$(shell find src/img/ -type f -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.svg')
TARGET_IMGS=$(subst src,build,$(SOURCE_IMGS))

all: css js img build/.htaccess build/index.html build/2019/index.html build/2020/index.html build/2021/index.html build/about.html build/events_token

.PHONY: css
css: build/styles/fossevents.css build/styles/images/marker-icon.png build/styles/images/marker-icon-2x.png build/styles/images/marker-shadow.png

.PHONY: js
js: build/js/event.js build/js/leaflet.js

.PHONY: img
img: build/favicon.ico $(TARGET_IMGS)

build/styles/fossevents.css: npm_deps_token

build/styles/fossevents.css: src/styles/fossevents.css src/lib/leaflet/leaflet.css
	cat $^ | node_modules/postcss-cli/bin/postcss -o $@

build/img/%: src/img/%
	@mkdir -p $(@D)
	cp $< $@

build/img/%.svg: npm_deps_token

build/img/%.png: npm_deps_token

build/img/%.jpg: npm_deps_token

build/img/%.svg: src/img/%.svg
	node_modules/svgo/bin/svgo $< -o $@

build/img/%.png: src/img/%.png
	node_modules/imagemin-cli/cli.js $< > $@

build/img/%.jpg: src/img/%.jpg
	node_modules/imagemin-cli/cli.js $< > $@

build/styles/images/%.png: src/lib/leaflet/images/%.png
	cp $< $@

build/js/event.js: src/js/event.js
	cp $< $@

build/js/leaflet.js: src/lib/leaflet/leaflet.js
	cp $< $@

build/.htaccess: src/.htaccess
	cp $< $@

build/favicon.ico: src/img/favicon.ico
	cp $< $@

build/index.html: data/2021_events_db.csv pip_deps_token
	pipenv run python3 generator/index.py

build/2019/index.html: data/2019_events_db.csv pip_deps_token
	pipenv run python3 generator/index_2019.py

build/2020/index.html: data/2020_events_db.csv pip_deps_token
	pipenv run python3 generator/index_2020.py

build/2021/index.html: data/2021_events_db.csv pip_deps_token
	pipenv run python3 generator/index_2021.py

build/about.html: src/templates/about.html pip_deps_token
	pipenv run python3 generator/about.py

build/events_token: data/2019_events_db.csv data/2020_events_db.csv data/2021_events_db.csv pip_deps_token
	pipenv run python3 generator/event_pages.py
	pipenv run python3 generator/ical_files.py
	touch build/events_token

npm_deps_token: package.json package-lock.json
	npm ci

pip_deps_token: Pipfile Pipfile.lock
	pipenv install

.PHONY: clean
clean:
	rm -rf build
