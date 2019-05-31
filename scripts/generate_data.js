#!/usr/bin/env node

const csv = require('csv-parser');
const fs = require('fs');
const slugify = require('slugify');

const parseDate = require('./helpers/parseDate');
const renderEvent = require('./helpers/renderEvent');

const csvOptions = {
    separator: ';'
};

fs.createReadStream('events_db.csv')
    .pipe(csv(csvOptions))
    .on('data', (data) => {

        const startDate = parseDate(data.datestart);
        const endDate = parseDate(data.dateend);
        const cfpdate = parseDate(data.cfpdate);

        const event = {
            type: 'event',
            title: data.name,
            homepage: data.homepage,
            date_start: `${startDate.year}-${startDate.month}-${startDate.day}`,
            date_end: `${endDate.year}-${endDate.month}-${endDate.day}`,
            city: data.city,
            cfp: !!data.cfplink,
            cfp_link: data.cfplink
        };

        if (cfpdate) {
            event.cfp_date = `${cfpdate.year}-${cfpdate.month}-${cfpdate.day}`;
        } else {
            event.cfp_date = 'open';
        }

        const dir = `content/events/${startDate.year}`;

        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }

        fs.writeFile(
            `${dir}/${startDate.month}_${slugify(event.title)}.md`,
            renderEvent(event),
            (err) => {

            }
        );
    });
