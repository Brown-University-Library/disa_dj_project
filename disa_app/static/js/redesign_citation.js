
// Get callback for change in source type
// (it's a callback in order to bake in the DATA object)

function getUpdateCitationFieldVisibilityCallback(FIELDS_BY_DOC_TYPE) {

  const requiredFieldsHeader = document.getElementById('required-fields-header'),
        optionalFieldsHeader = document.getElementById('optional-fields-header');

  return function(citationTypeId) {

    const citationFields = document.querySelectorAll('#citation-fields > div'),
          fieldStatus = FIELDS_BY_DOC_TYPE[citationTypeId];

    requiredFieldsHeader.hidden = fieldStatus.required.length === 0;
    optionalFieldsHeader.hidden = fieldStatus.optional.length === 0;

    citationFields.forEach((citationField, defaultOrderIndex) => { 
      const fieldId = citationField.id;
      if (fieldStatus.required.includes(fieldId)) {
        citationField.hidden = false;
        citationField.style.order = (100 + defaultOrderIndex);
      } else if (fieldStatus.optional.includes(fieldId)) {
        citationField.hidden = false;
        citationField.style.order = (200 + defaultOrderIndex);
      } else {
        citationField.hidden = true;
      }
    });
  }
}

function main(DATA) {

  // Citation form (tab 1)

  const updateCitationFieldVisibility = getUpdateCitationFieldVisibilityCallback(DATA.FIELDS_BY_DOC_TYPE);

  const citationForm = new Vue({
    el: '#citation-form',
    data: DATA,
    watch: {
      'citation_data.citation_type_id': updateCitationFieldVisibility
    },
    methods: {
      onSubmitForm: function(x) { 
        // @todo finish this
        console.log({ 
          submitEvent: x, 
          data: JSON.parse(JSON.stringify(this._data))
        })
      }
    },
    mounted: updateCitationFieldVisibility(DATA.citation_data.citation_type_id)
  });

  // Item form (tab 2)
  // @todo finish item form

  const itemForm = new Vue({
    delimiters: ['v{','}v'] // So as not to clash with Django templates
  });
}

export { main };