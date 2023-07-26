// Find the timeline dots
let dots = document.querySelectorAll(".timeline li");
function timelineFilter() {
  // Set the start date
  let start_date = document.getElementById("startDate").value;
  // Set the end date
  let end_date = document.getElementById("endDate").value;
  // Loop through the dots
  for (var i = 0; i < dots.length; i++) {
    // If the start date is greater than or equal to the data-year...
    if (
      dots[i].getAttribute("data-year") >= start_date &&
      dots[i].getAttribute("data-year") <= end_date
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
