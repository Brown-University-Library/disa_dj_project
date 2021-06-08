
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

async function saveCitationToServer() {

  function convertFormDatesToAPI(dateString) {
    const [year, monthNumber, day] = dateString.split('-').map(x => parseInt(x)),
          month = [ null, 'January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August', 'September', 
                    'October', 'November', 'December'][monthNumber];
    return `${month} ${day}, ${year}`;
  }

  const requestBody = {
    citation_type_id: this.formData.doc.citation_type_id,
    comments: this.formData.doc.comments,
    acknowledgements: this.formData.doc.acknowledgements,
    fields: Object.assign({}, this.formData.doc.fields, {
      accessDate: convertFormDatesToAPI(this.formData.doc.fields.accessDate),
      date: convertFormDatesToAPI(this.formData.doc.fields.date)
    })
  };

  const url = `http://127.0.0.1:8000/data/documents/${this.formData.doc.id}/`,
        fetchOptions = {
          method: 'PUT', // apiDefinition.api_method,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': TOKEN
          },
          body: JSON.stringify(requestBody)
        };

  console.log('SAVING SOURCE', {url, fetchOptions});

  if (false) { return }  // Skip send if true

  this.saveStatus = this.SAVE_STATUS.SAVE_IN_PROGRESS;
  const response = await fetch(url, fetchOptions);
  if (response.ok) {
    const dataJSON = await response.json();
    // this.currentItem.relationships = dataJSON.store;
    this.saveStatus = this.SAVE_STATUS.SUCCESS;
    console.log('RESPONSE', {response, dataJSON}) ;
  } else {
    this.saveStatus = this.SAVE_STATUS.ERROR;
    throw Error(response.statusText);
  }
}


/*

{
  ISSN: saveData.ISSN,
  abstractNote: "",
  accessDate: "April 13, 2021",
  archive: "Accessible Archive",
  archiveLocation: "",
  callNumber: "",
  date: "January 2, 1745",
  edition: "",
  extra: "",
  language: "English",
  libraryCatalog: "",
  pages: "4",
  place: "Charleston, South Carolina ",
  publicationTitle: "The South Carolina Gazette",
  rights: "",
  section: "",
  shortTitle: "",
  title: "RUN AWAY Some Time Since",
  url: "https://accessible.com/accessible/docButton?AAWhat=builtPage&AAWhere=THESOUTHCAROLINAGAZETTE.17440102_001.JPG.image&AABeanName=toc1&AACheck=~&AANextPage=/printBuiltImagePage.jsp",
  author: "Rene Peyre",
}

*/

function initializeCitationForm(dataAndSettings) {  
  new Vue({
    el: '#citation-form',
    data: dataAndSettings,
    watch: {
      'formData.doc.citation_type_id': updateCitationFieldVisibility,
      watchMeToTriggerSave: saveCitationToServer
    },
    methods: {
      openItemTab: function () {
        document.getElementById('item-tab').click();
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