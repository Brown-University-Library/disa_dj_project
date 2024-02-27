
function updateSourceFieldVisibility() {

  const citationTypeId = this.formData.doc.citation_type_id,
        requiredFieldsHeader = document.getElementById('required-fields-header'),
        optionalFieldsHeader = document.getElementById('optional-fields-header'),
        citationFields = document.querySelectorAll('#citation-fields > div'),
        fieldStatus = this.FIELDS_BY_DOC_TYPE[citationTypeId];

  requiredFieldsHeader.hidden = (fieldStatus.required.length === 0);
  optionalFieldsHeader.hidden = (fieldStatus.optional.length === 0);

  citationFields.forEach((citationField, defaultOrderIndex) => { 
    const fieldId = citationField.id;
    const citationFieldInputElem = citationField.querySelector(':scope > input, :scope > textarea');
    let tabOrder = 1;

    if (fieldStatus.required.includes(fieldId)) {
      citationField.hidden = false;
      citationField.style.order = (100 + defaultOrderIndex);
      citationFieldInputElem.tabIndex = 100 + tabOrder++;
    } else if (fieldStatus.optional.includes(fieldId)) {
      citationField.hidden = false;
      citationField.style.order = (200 + defaultOrderIndex);
      citationFieldInputElem.tabIndex = 200 + tabOrder++;
    } else {
      citationField.hidden = true;
    }
  });
}

async function saveSourceToServer() {

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
    fields: this.formData.doc.fields
    /* COMMENTED OUT FOR NOW -- until we figure out how to enter dates in a flexible way
    fields: Object.assign({}, this.formData.doc.fields, {
      accessDate: convertFormDatesToAPI(this.formData.doc.fields.accessDate),
      date: convertFormDatesToAPI(this.formData.doc.fields.date)
    }) */
  };

  const url = `${API_URL_ROOT}documents/${this.formData.doc.id}/`,
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
    console.log('SAVING SOURCE - RESPONSE', {response, dataJSON}) ;
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

function initializeSourceForm(dataAndSettings) {  
  new Vue({
    el: '#source-form',
    data: dataAndSettings,
    watch: {
      'formData.doc.citation_type_id': updateSourceFieldVisibility
    },
    methods: {
      openItemTab: function () {
        document.getElementById('item-tab').click();
      },
      saveSourceToServer
    },
    mounted: updateSourceFieldVisibility
  });
}

export { initializeSourceForm };