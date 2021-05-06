


// Get callback for change in source type
// (it's a callback in order to bake in the dataAndSettings object)

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


function initializeCitationForm(dataAndSettings) {

  const updateCitationFieldVisibility = getUpdateCitationFieldVisibilityCallback(dataAndSettings.FIELDS_BY_DOC_TYPE);
  
  new Vue({
    el: '#citation-form',
    data: dataAndSettings,
    watch: {
      'formData.doc.citation_type_id': updateCitationFieldVisibility
    },
    methods: {
      openItemTab: function () {
        document.getElementById('item-tab').click();
      },
      onSubmitForm: function(x) { 
        // @todo finish this
        console.log({ 
          submitEvent: x, 
          data: JSON.parse(JSON.stringify(this.formData))
        })
      }
    },
    mounted: updateCitationFieldVisibility(dataAndSettings.formData.doc.citation_type_id)
  });
}

export { initializeCitationForm };