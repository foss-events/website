$(shell mkdir -p build/2019 build/2020 build/2021 build/2022 build/2023 build/img/eventlogos/2020 build/js build/styles/images)
$(shell mkdir -p build/img/eventbanners/2020 build/img/eventbanners/2021 build/img/eventbanners/2022 build/img/eventbanners/2023)
$(shell mkdir -p build/img/blog)
# here is the import of all images from src/img into the build process, see https://github.com/foss-events/website/pull/179/commits/b695c04ec9eecf9dbda4efe0646cc592a8c746ef
SOURCE_IMGS=$(shell find src/img/ -type f -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.svg')
TARGET_IMGS=$(subst src,build,$(SOURCE_IMGS))
COMMON=generator/parser.py generator/parse_helper.py
CSVS=$(wildcard data/*.csv)
POSTS=$(wildcard blog/*.html)
export PYTHONWARNINGS = ignore

all: build/robots.txt css js img build/toots.html build/blog/% build/.htaccess build/index.html build/2019/index.html build/2020/index.html build/2021/index.html build/2022/index.html build/2023/index.html build/about.html build/events_token

.PHONY: css
css: build/styles/fossevents.css build/styles/images/marker-icon.png build/styles/images/marker-icon-2x.png build/styles/images/marker-shadow.png

.PHONY: js
js: build/js/event.js build/js/leaflet.js

.PHONY: img
img: build/favicon.ico $(TARGET_IMGS)

build/styles/fossevents.css: tmp/npm_deps_token

build/styles/fossevents.css: src/styles/fossevents.css src/lib/leaflet/leaflet.css
	cat $^ | node_modules/postcss-cli/bin/postcss -o $@

build/img/%: src/img/%
	@mkdir -p $(@D)
	cp $< $@

build/img/%.svg: tmp/npm_deps_token

build/img/%.png: tmp/npm_deps_token

build/img/%.jpg: tmp/npm_deps_token

build/img/%.svg: src/img/%.svg
	node_modules/svgo/bin/svgo $< -o $@

build/img/%.png: src/img/%.png
	node_modules/imagemin-cli/cli.js $< > $@

build/img/%.jpg: src/img/%.jpg
	node_modules/imagemin-cli/cli.js $< > $@

build/robots.txt: src/robots.txt
	cp src/robots.txt build/robots.txt

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

build/index.html: data/2023_events_db.csv tmp/pip_deps_token src/templates/partials/header-logo.html src/templates/partials/head.html src/templates/index.html generator/index.py $(COMMON)
	pipenv run python3 -m generator.index 2023 build/index.html

build/%/index.html: data/%_events_db.csv tmp/pip_deps_token src/templates/partials/header-logo.html src/templates/partials/head.html src/templates/index.html generator/index.py $(COMMON)
	pipenv run python3 -m generator.index $* build/$*/index.html

build/blog/%: $(POSTS)
	pipenv run python3 -m generator.blog

build/about.html: src/templates/about.html tmp/pip_deps_token
	pipenv run python3 -m generator.about

build/toots.html: data/2023_events_db.csv src/templates/toots.html
	pipenv run python3 -m generator.toots

build/events_token: $(CSVS) generator/parser.py src/templates/partials/header-logo.html src/templates/partials/head.html src/templates/event.html tmp/pip_deps_token
	pipenv run python3 -m generator.event_pages
	pipenv run python3 -m generator.ical_files
	touch build/events_token

tmp/npm_deps_token: package.json package-lock.json
	npm ci
	touch tmp/npm_deps_token

tmp/pip_deps_token: Pipfile Pipfile.lock
	pipenv install
	touch tmp/pip_deps_token

.PHONY: clean
clean:
	rm -rf build
	rm -f tmp/npm_deps_token tmp/pip_deps_token
