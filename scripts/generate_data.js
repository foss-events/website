#!/usr/bin/env node

const csv = require('csv-parser');
const fs = require('fs');
const slugify = require('slugify');

const renderEvent = require('./helpers/renderEvent');
const parseEvent = require('./helpers/parseEvent');

const csvOptions = {
    separator: '\t'
};

fs.createReadStream('events_db.csv')
    .pipe(csv(csvOptions))
    .on('data', (data) => {

        const event = parseEvent(data);
        const dir = `content/events/${event.date_start_components.year}`;

        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }

        fs.writeFile(
            `${dir}/${event.date_start_components.month}_${slugify(event.title)}.md`,
            renderEvent(event),
            (err) => {

            }
        );
    });
