
function updateCitationFieldVisibility() {

  const citationTypeId = this.formData.doc.citation_type_id,
        requiredFieldsHeader = document.getElementById('required-fields-header'),
        optionalFieldsHeader = document.getElementById('optional-fields-header'),
        citationFields = document.querySelectorAll('#citation-fields > div'),
        fieldStatus = this.FIELDS_BY_DOC_TYPE[citationTypeId];

  requiredFieldsHeader.hidden = (fieldStatus.required.length === 0);
  optionalFieldsHeader.hidden = (fieldStatus.optional.length === 0);

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
    mounted: updateCitationFieldVisibility,
    computed: {
      watchMeToTriggerSave: function () {
        return this.formData.doc.citation_type_id + JSON.stringify(this.formData.doc.fields) +
               this.formData.doc.acknowledgements + this.formData.doc.comments;
      }
    }
  });
}

export { initializeCitationForm };