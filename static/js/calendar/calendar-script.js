$(document).ready(function () {
    $('#calendar').evoCalendar({

        theme: 'Royal Navy',
        color: "#72baff",
        calendarEvents: [
            {
                id: 'event1', // Event's ID (required)
                name: "event", // Event name (required)
                date: "January/1/2020", // Event date (required)
                description: " the heart touching greeting will make feel anyone very special.jbijsknjckcjkdnvjnviavnjkvn dfkjn kjn kfkjfnv kjdf.",
                type: "holiday", // Event type (required)
                everyYear: true // Same event every year (optional)
            },
            {

                name: "Vacation Leave",
                badge: "02/13 - 02/15", // Event badge (optional)
                date: ["February/13/2020", "February/15/2020"], // Date range
                description: "Vacation leave for 3 days.", // Event description (optional)
                type: "event",
                color: "#72baff" // Event custom color (optional)
            }
        ]

    })
})
