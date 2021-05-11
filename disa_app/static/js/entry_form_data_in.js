
import {LOCAL_SETTINGS} from './entry_form_settings.js';

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

  // Convert array of references to hash of references (by ID)
  // @todo replace this with a cacluated field
  //       referenceByID = function(id) { 
  //         return formData.doc.references.find(reference => reference.id === id)
  //       }

  data.formData.doc.references = data.formData.doc.references.reduce(
    (refObj, ref) => { refObj[ref.id] = ref; return refObj },
    {}
  );

  data.NEW_USER_TEMPLATE = data.formData.new_user_template.sample_payload; 
  delete data.formData.new_user_template;

  // Add registers for Vue implementation

  data.currentItemId     = -1;
  data.currentReferentId = -1;
  data.currentNameId     = -1;

  return data;
}

async function getSourceData() {

  const dataURL = new URL(window.location.toString());

  dataURL.hash = '';
  dataURL.search = '?format=json';

  const response = await fetch(dataURL.href),
        dataJSON = await response.json(),
        dataWithSettings = Object.assign({}, LOCAL_SETTINGS, { formData: dataJSON });
  return preprocessCitationData(dataWithSettings);
}

function preprocessItemData(itemData, oldItemData) {

  const itemDate = new Date(itemData.rec.date);

  let processedData = {
    // date: itemData.rec.date,
    dateParts: {
      month: itemDate.getMonth() + 1,
      day: itemDate.getDate(),
      year: itemDate.getFullYear()
    },
    id: itemData.rec.id,
    location_info: oldItemData.location_info, // the old (non-enhanced) location data is richer
    national_context_id: itemData.rec.national_context,
    reference_type_id: itemData.rec.record_type.id,
    // reference_type_name: itemData.rec.record_type.label,
    // Convert array of referents to a hash by referent ID
    referents: itemData.entrants.reduce(
      (referentHash, referent) => { 
        referentHash[referent.id] = referent;
        referentHash[referent.id].hello = 'there'; // @todo temp
        return referentHash;
      },
      {}
    ),
    // referents: getAdditionalReferentInfo(itemData.entrants),
    groups: itemData.groups.group_data,
    transcription: itemData.rec.transcription,
    image_url: itemData.rec.image_url,
    FULL_DATA_LOADED: true // Flag
  }
  return processedData;
}

/*
async function getAdditionalReferentInfo(referents) {
  const referentIDs = referents.map(r => r.id);
} */

// async function getItemData(itemId) {
//   var foo_url = `/data/records/${itemId}/`;
//   console.log( "foo_url, ", foo_url );
//   if (itemId) {
//     const dataURL = `/data/records/${itemId}/`,
//     response = await fetch(dataURL),
//     dataJSON = await response.json();
//     return preprocessItemData(dataJSON);
//   } else {
//     return undefined
//   }
// }

async function getItemData(itemId, oldItemData) {
  // const fullLocationData = oldItemData.location_info;
  if (itemId) {
    // data_itemrecord_api_url_root variable set in redesign_citation.html
    const dataURL = `${data_itemrecord_api_url_root}${itemId}/`,
    response = await fetch(dataURL),
    dataJSON = await response.json();
    return preprocessItemData(dataJSON, oldItemData);
  } else {
    return undefined
  }
}

function preprocessReferentData(referentData) {
  referentData.FULL_DATA_LOADED = true;
  return referentData;
}

async function getReferentData(referentId, itemId, apiDefinition) {
  
  if (referentId === 'new' && false) { // DISABLED - actually, this is a SAVE function
    const dataURL = apiDefinition.api_url,
          fetchOptions = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              id: 'new',
              name: {
                first: '[none]', 
                id: 'name', 
                last: '[none]'
              },
              record_id: itemId,
              roles: [ {'id': '3', 'name': 'Priest'}]
            })
          },
          // response = await fetch(dataURL, fetchOptions); // @todo need to handle 404s etc.
          dataJSON = await response.json();
    console.log('GGGGGGG', dataJSON);
    // return preprocessReferentData(dataJSON.ent);
  } else if (referentId) {
    const dataURL = apiDefinition.api_url,
          response = await fetch(dataURL, { 
            method: apiDefinition.api_method,
            headers: {
              'Content-Type': 'application/json'
            }
          }), // @todo need to handle 404s etc.
          dataJSON = await response.json();
    return preprocessReferentData(dataJSON.ent);
  } else {
    return undefined;
  }
}

export { getSourceData, getItemData, getReferentData }
