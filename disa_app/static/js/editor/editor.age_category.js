// autopopulate the age category if there's an age integer
let ageInteger = document.getElementById('formInputDISAPersonAge_integer');
let ageCategory = document.getElementById('formInputDISAPersonAge_category');

ageInteger.addEventListener("change", populateCategory);

function populateCategory(e) {
    var ageValue = ageInteger.value;
    console.log(ageValue);
    if (ageValue <= 2) {
        ageCategory.value("Infant");
    } else if (ageValue > 2 && <= 14) {
        ageCategory.value("Child");
    } else if (ageValue > 14 && <= 25) {
        ageCategory.value("Youth/Young Adult");
    } else if (ageValue > 25 && <= 40) {
        ageCategory.value("Adult");
    } else if (ageValue > 40 && <= 55) {
        ageCategory.value("Older person");
    } else if (ageValue > 55) {
        ageCategory.value("Elder");
    }
}
