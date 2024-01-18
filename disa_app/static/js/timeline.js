// create the timeline items from json
/*let timeline = document.querySelector(".timeline");
let timelineUL = document.createElement('ul');

async function populate() {
    const request = new Request(timeline_data_url);
    const response = await fetch(request);
    const events = await response.json();
    populateTimeline(events);
}

function populateTimeline(obj) {
    let events = obj.timeline;

    for (const event of events) {
        let item = document.createElement("li");
        let eventTitle = document.createElement("h2");
        let eventDesc = document.createElement("p");

        eventYear = event.year;
        eventTitle.textContent = eventYear + ": " + event.title;
        eventDesc.textContent = event.event;

        item.setAttribute("data-year", eventYear);
        item.appendChild(eventTitle);
        item.appendChild(eventDesc);

        timelineUL.appendChild(item);
    }
}
timeline.appendChild(timelineUL);
populate();
*/
// Find the timeline dots
let dots = document.querySelectorAll(".timeline li");

function timelineFilter() {
    // Set the start date
    let startDate = document.getElementById("startDate").value;
    // Set the end date
    let endDate = document.getElementById("endDate").value;
    // Loop through the dots
    for (var i = 0; i < dots.length; i++) {
        // If the start date is greater than or equal to the data-year...
        if (
            dots[i].getAttribute("data-year") >= startDate &&
            dots[i].getAttribute("data-year") <= endDate
        ) {
            // ...remove the `.is-hidden` class.
            dots[i].classList.remove("d-none");
        } else {
            // Otherwise, add the class.
            dots[i].classList.add("d-none");
        }
    }
}
//A little delay
let typingTimer;
let typeInterval = 500;
let startInput = document.getElementById("startDate");
let endInput = document.getElementById("endDate");

startInput.addEventListener("input", () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(timelineFilter, typeInterval);
});
endInput.addEventListener("input", () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(timelineFilter, typeInterval);
});
