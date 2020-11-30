
(function () {

// USER SETTINGS

// MARKUP IDs

const elem = [
  'tabs_bibinfoanditems',
  'document_type'
].reduce((elemsById, id) => {
  elemsById[id] = document.getElementById(id);
  return elemsById;
}, {});

// Data structure for showing / hiding citation fields

const FIELDS_BY_DOC_TYPE = {

  // Book
  20: {
    required: ["author", "date", "pages", "place", "title"],
    optional: [
      "abstractNote",
      "edition",
      "language",
      "series",
      "seriesNumber",
      "shortTitle",
      "url"
    ]
  },
  // Book Section
  21: {
    required: ["author", "date", "pages", "place", "title"],
    optional: [
      "abstractNote",
      "edition",
      "language",
      "section",
      "series",
      "seriesNumber",
      "shortTitle",
      "url"
    ]
  },
  // Document
  26: {
    required: ["author", "date", "pages", "place", "title"],
    optional: [
      "abstractNote",
      "archive",
      "archiveLocation",
      "language",
      "url"
    ]
  },
  // Interview
  33: {
    required: ["author", "date", "place", "rights", "title"],
    optional: [
      "abstractNote",
      "archive",
      "archiveLocation",
      "language",
      "url"
    ]
  },
  // Journal Article
  34: {
    required: ["author", "date", "pages", "title"],
    optional: ["abstractNote", "language", "url"]
  },
  // Magazine Article
  36: {
    required: ["author", "date", "pages", "title"],
    optional: ["abstractNote", "language", "url"]
  },
  // Manuscript
  37: {
    required: [
      "archive",
      "archiveLocation",
      "author",
      "date",
      "pages",
      "title"
    ],
    optional: ["abstractNote", "language", "place", "url"]
  },
  // Newspaper Article
  39: {
    required: ["date", "edition", "place", "title"],
    optional: [
      "abstractNote",
      "archive",
      "archiveLocation",
      "author",
      "language",
      "pages",
      "section",
      "url"
    ]
  },
  // Thesis
  46: {
    required: ["author", "date", "rights", "title"],
    optional: [
      "abstractNote",
      "archive",
      "archiveLocation",
      "language",
      "url"
    ]
  },
  // Webpage
  49: {
    required: ["accessDate", "date", "title", "url"],
    optional: ["author", "language"]
  }
};

// Get callback for when the citation type dropdown changes

function getCitationFieldUpdateCallback() {

  // Load a bunch of form elements

  const requiredFieldsContainer = document.getElementById('required-fields'),
        requiredFieldsHeader = document.getElementById('required-fields-header'),
        optionalFieldsContainer = document.getElementById('optional-fields'),
        optionalFieldsHeader = document.getElementById('optional-fields-header'),
        hiddenFieldsContainer = document.getElementById('hidden-fields'),
        citationTypeSelector = elem.document_type, // document.getElementById('document_type'),
        citationFields = Array.from(document.getElementsByClassName('citation-field'));

console.log('HELOO HE::P', elem.document_type);

  // Return callback

  return () => {

    const citationTypeId = parseInt(citationTypeSelector.value),
          fieldStatus = FIELDS_BY_DOC_TYPE[citationTypeId];

    // Move citation fields to required / optional / hidden

    citationFields.forEach(citationField => {
      const citationFieldId = citationField.id;
      if (fieldStatus.required.includes(citationFieldId)) {
        requiredFieldsContainer.appendChild(citationField);
      } else if (fieldStatus.optional.includes(citationFieldId)) {
        optionalFieldsContainer.appendChild(citationField);
      } else {
        hiddenFieldsContainer.appendChild(citationField);
      }
    });

    // Unhide

    requiredFieldsHeader.removeAttribute('hidden');
    optionalFieldsHeader.removeAttribute('hidden');
  }  
}

  // Initialize form fields with DB values

  function initFormFields(citationData) {

    // Citation bib fields
    Object.keys(citationData.citation_type_fields).forEach(fieldId =>
      document.getElementById(`${fieldId}-value`).value = citationData.citation_type_fields[fieldId]
    );

    // Acknowledgements
    document.getElementById('formInputDISAAcknowledgements')
            .value = citationData.acknowledgements;
    // MORE TO COME ...
  }

  // On load ...

  document.addEventListener('DOMContentLoaded', () => {

    // Initialize the form fields with data from the DB

    initFormFields(citation_data);

    // Add listener for citation type dropdown selector

    const updateCitationFieldVisibility = getCitationFieldUpdateCallback();
    elem.document_type.addEventListener(
      'change', updateCitationFieldVisibility
    );

    // Initialize display based on current citation type selection
    // TEMPORARY WORKAROUND - wait for Birkin's code to run

    window.setTimeout(updateCitationFieldVisibility, 500);
  });
})();