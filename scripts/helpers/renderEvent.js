module.exports = (event) => {
    return `
---
type: ${event.type}
title: ${event.title}
homepage: ${event.homepage}
date_start: ${event.date_start}
date_end: ${event.date_end}
city: ${event.city}
cfp: ${event.cfp}
cfp_date: ${event.cfp_date}
cfp_link: ${event.cfp_link}
---
`;
};
