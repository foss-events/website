/**
 * @param {string} string
 * @return {{year, month, day}}
 */
module.exports = (string) => {
    if (string.trim() === 'open') {
        return null;
    }

    const stringLength = string.length;
    const date = {
        day: '01'
    };

    if (stringLength >= 4) {
        date.year = string.substr(0, 4);
    }

    if (stringLength >= 6) {
        date.month = string.substr(4, 2);
    }

    if (stringLength >= 8) {
        date.day = string.substr(6, 2);
    }

    return date;
};
