$(shell mkdir -p build/events)

all: build/events/token

build/events/token: 2019_events_db.csv
	rm build/events/* -Rf
	python generator/gen.py
	touch build/events/token
