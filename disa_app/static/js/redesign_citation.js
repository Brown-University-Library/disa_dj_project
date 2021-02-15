

// Get callback for when the citation type dropdown changes

function getCitationFieldUpdateCallback(DATA) {

  // Load a bunch of form elements

  const requiredFieldsContainer = document.getElementById("required-fields"),
        requiredFieldsHeader    = document.getElementById("required-fields-header"),
        optionalFieldsContainer = document.getElementById("optional-fields"),
        optionalFieldsHeader    = document.getElementById("optional-fields-header"),
        hiddenFieldsContainer   = document.getElementById("hidden-fields"),
        citationFields = Array.from(
          document.getElementsByClassName("citation-field")
        );

  // Return callback

  return function (citationTypeId) {

    const fieldStatus = DATA.FIELDS_BY_DOC_TYPE[citationTypeId];

    // Move citation fields to required / optional / hidden
    // @todo this is not working with Vue - it's copying
    //       Maybe it's moving it, but then re-rendering to create a copy?

    citationFields.forEach((citationField) => { 
      const citationFieldId = citationField.id;
      console.log(citationFieldId, fieldStatus);
      if (fieldStatus.required.includes(citationFieldId)) {
        console.log('REQD');
        requiredFieldsContainer.appendChild(citationField);
      } else if (fieldStatus.optional.includes(citationFieldId)) {
        optionalFieldsContainer.appendChild(citationField);
        console.log('OPT');
      } else {
        hiddenFieldsContainer.appendChild(citationField);
        console.log('HIDDEN', { hiddenFieldsContainer, citationField } );
      }
    });

    // Unhide headers

    requiredFieldsHeader.removeAttribute("hidden");
    optionalFieldsHeader.removeAttribute("hidden");
  };
}





  });
}

export { main };
