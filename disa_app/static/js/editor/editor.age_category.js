// autopopulate the age category if there's an age integer
let ageInteger = document.getElementById('formInputDISAPersonAge_integer');
let ageCategory = document.getElementById('formInputDISAPersonAge_category');

ageInteger.addEventListener("change", populateCategory);

function populateCategory(e) {
    var ageValue = ageInteger.value;
    console.log("ageValue is: " + ageValue);
    if (ageValue <= 2) {
        ageCategory.value("Infant");
    } else if (ageValue > 2 && ageValue <= 14) {
        ageCategory.value("Child");
    } else if (ageValue > 14 && ageValue <= 25) {
        ageCategory.value("Youth/Young Adult");
    } else if (ageValue > 25 && ageValue <= 40) {
        ageCategory.value("Adult");
    } else if (ageValue > 40 && ageValue <= 55) {
        ageCategory.value("Older person");
    } else if (ageValue > 55) {
        ageCategory.value("Elder");
    }
}
