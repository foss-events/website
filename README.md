# // foss.events

## About the software

// foss.events is a data-driven Free Software community calendar to enable communities setting up their own customized calendars, thus helping to connect its members. [www.foss.events](https://www.foss.events) is one running instance and showcase of the software. 

## Purpose

Many communities have smaller or larger events as one element to bring together its members and help them to interconnect. However, many of these communities miss a good calendar for people to find these events. On one hand because proper software is missing, in particular if proprietary software is not a solution. On the other hand because data collection and preparation is intense and time-consuming. // foss.events solves these problems by offering a Free Sofware calendar solution and the ability for community maintenance of such calendar.

Initially we have envisioned a static website generator that creates its pages from a Libre Office sheet. The idea was that this way it is easy also for non-tech-communities and maintainers of such calendar to keep data accurate. With further development this might be subject to change, however. In particular as we envision further autmatization of event-entries for future developments and so we might adapt the system as it needs fit. 

## Install

## Local Build instructions

Requirements:

* [Node.js](https://nodejs.org/en/download/package-manager/) >= 12
* Python >= 3.6
* pipenv
* make

```
pipenv install
make
```

Start the dev server

```shell script
pipenv run bin/serve.py
```

You may now access the website locally in your browser [https://localhost:1337/](https://localhost:1337/).

##  Usage

The build script creates webpages out of the date listed in /data/*_events_db.csv. You can specify the fields of data you need for your event within this sheet and collect the data in question.

In /src/templates/ you find the templates that are used to create the static pages. index.html is a list of all events within the sheet to give an oversight and event.html creates the individual event pages. Here you can specify the data that is shown and the design.

The calendar also comes with its own news-channels: /generator/blog.py creates blog-posts so you can reflect and spread news on your own blog. /generator/toots.py creates toots that you can use on your mastodon-instance, for example. 

## Contributing

There are two ways you can help: You can help to improve the software itself. A good start would be to have a [look at our issue-tracker](https://github.com/foss-events/website/issues). 

Or you can help by adding events on our instance www.foss.events. To do so, please read the [contribute section on the website](https://foss.events/about.html#contributing).

### Missing an event?

Send an e-mail to [onemore@foss.events](mailto:onemore@foss.events).

### Add an event via Git

* Fork [this repo](https://github.com/foss-events/website)
* Add you event to [the CSV file](https://github.com/foss-events/website/tree/master/data)
* Optionally [provide a logo](https://github.com/foss-events/website/tree/master/src/img/eventbanners)
* Open a pull request

## License

All code of the software // foss.events is published under AGPL-3.0 license.

The database on www.foss.events is published under ODBL 1.0 license

Content of these databases is published under Creative Commons Attribution-ShareAlike 4.0 International 
