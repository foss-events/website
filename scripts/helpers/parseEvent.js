const parseDate = require('./parseDate');

/**
 * Parses a CSV line and returns an event object.
 *
 * @param {{}} data
 * @return {{}}
 */
module.exports = (data) => {
    const startDate = parseDate(data.datestart);
    const endDate = parseDate(data.dateend);
    const cfpdate = parseDate(data.cfpdate);

    const event = {
        type: 'event',
        title: data.name,
        homepage: data.homepage,
        date_start: `${startDate.year}-${startDate.month}-${startDate.day}`,
        date_start_components: startDate,
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

    return event;
};
