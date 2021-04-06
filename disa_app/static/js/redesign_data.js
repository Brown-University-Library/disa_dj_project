
import {LOCAL_SETTINGS} from '/static/js/redesign_settings.js';



function preprocessCitationData(data) { 
/*
  // Convert dates to YYYY-MM-DD format
  // @todo should be done on server

  if (data.citation_type_fields.date) {
    data.citation_type_fields.date = 
      (new Date(data.citation_type_fields.date))
      .toISOString()
      .slice(0,10);
  }

  if (data.citation_type_fields.accessDate) {
    data.citation_type_fields.accessDate = 
      (new Date(data.citation_type_fields.accessDate))
      .toISOString()
      .slice(0,10);
  }
  */

  // Add registers for Vue implementation

  data.currentItemId     = -1;
  data.currentReferentId = -1;
  data.currentNameId     = -1;

  return data;
}


async function getData() {

  const dataURL = new URL(window.location.toString());

  dataURL.hash = '';
  dataURL.search = '?format=json';

  const response = await fetch(dataURL.href),
        dataJSON = await response.json(),
        dataWithSettings = Object.assign({}, LOCAL_SETTINGS, { formData: dataJSON });
  return preprocessCitationData(dataWithSettings);
}

export { getData }
