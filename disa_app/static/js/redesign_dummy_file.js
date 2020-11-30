

const AGE_BY_NUMBER_CHECKBOX_ID = 'formInputSpecifiedByNumber',
      AGE_BY_NUMBER_DISPLAY_CSS_CLASS = 'age-as-number';

const ageByNumberCheckbox = document.getElementById(AGE_BY_NUMBER_CHECKBOX_ID);

if (ageByNumberCheckbox) {
  ageByNumberCheckbox.onchange = function(e) {
    const classOp = this.checked ? 'add' : 'remove';
    document.body.classList[classOp](AGE_BY_NUMBER_DISPLAY_CSS_CLASS);
  };
}


