

// Get callback for when the citation type dropdown changes

function getCitationFieldUpdateCallback() {
  // Load a bunch of form elements

  const requiredFieldsContainer = document.getElementById("required-fields"),
    requiredFieldsHeader = document.getElementById("required-fields-header"),
    optionalFieldsContainer = document.getElementById("optional-fields"),
    optionalFieldsHeader = document.getElementById("optional-fields-header"),
    hiddenFieldsContainer = document.getElementById("hidden-fields"),
    citationTypeSelector = document.getElementById('document_type'),
    citationFields = Array.from(
      document.getElementsByClassName("citation-field")
    );

  // Return callback

  return () => {
    const citationTypeId = parseInt(citationTypeSelector.value),
      fieldStatus = SETTINGS.FIELDS_BY_DOC_TYPE[citationTypeId];

    // Move citation fields to required / optional / hidden

    citationFields.forEach((citationField) => {
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

    requiredFieldsHeader.removeAttribute("hidden");
    optionalFieldsHeader.removeAttribute("hidden");
  };
}





  });
}

export { main };
