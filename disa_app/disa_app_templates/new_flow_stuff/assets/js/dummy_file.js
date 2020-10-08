

const AGE_BY_NUMBER_CHECKBOX_ID = 'formInputSpecifiedByNumber',
      AGE_BY_NUMBER_DISPLAY_CSS_CLASS = 'age-as-number';

document.getElementById(AGE_BY_NUMBER_CHECKBOX_ID)
        .onchange = function() {
          const classOp = this.checked ? 'add' : 'remove';
          document.body.classList[classOp](AGE_BY_NUMBER_DISPLAY_CSS_CLASS);
        };

