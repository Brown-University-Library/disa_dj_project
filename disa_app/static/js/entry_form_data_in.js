
import {LOCAL_SETTINGS} from './entry_form_settings.js';

function preprocessSourceData(data) {

  // Make array of references into a hash by reference ID

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

  // Add accessors for API registry

  data.formData.user_api_info.get_user_info.api_url_forID = function (referentID) {
    return data.formData.user_api_info.get_user_info.api_url.replace('THE-REFERENT-ID', referentID);
  }

  return data;
}

async function getSourceData() {

  const dataURL = new URL(window.location.toString());

  dataURL.hash = '';
  dataURL.search = '?format=json';

  const response = await fetch(dataURL.href),
        dataJSON = await response.json(),
        dataWithSettings = Object.assign({}, LOCAL_SETTINGS, { formData: dataJSON });
  return preprocessSourceData(dataWithSettings);
}

function preprocessItemData(itemData, oldItemData, relationshipsData, referentData) {

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
    referents: referentData.reduce(
      (referentHash, referent) => {
        referentHash[referent.id] = referent;
        referentHash[referent.id].hello = 'there'; // @todo temp
        referentHash[referent.id].relationships = relationshipsData[referent.id];
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

async function getItemData(itemId, oldItemData, apiInfo) {
  if (itemId) {

    // data_itemrecord_api_url_root variable set in redesign_citation.html
    // @todo but is also available in apiInfo?

    const dataURL = `${data_itemrecord_api_url_root}${itemId}/`,
          itemDataPromise = fetch(dataURL).then(response => response.json()),
          referentDataPromise = itemDataPromise.then(itemData => {
            return getReferentsData(
              itemData.entrants.map(referent => referent.id), 
              itemId,
              apiInfo
            );
          }),
          relationshipsDataPromise = getRelationshipsData(itemId);

    return Promise.all([].concat(referentDataPromise, relationshipsDataPromise, itemDataPromise))
           .then(([referentData, relationshipsData, itemData]) => {
      return preprocessItemData(itemData, oldItemData, relationshipsData, referentData);
    });
  } else {
    return undefined
  }
}

function preprocessReferentData(referentData) {

  // The API gives us name types as string labels, but borks
  //   the entry upon save if it's anything but a number (ID).
  // Convert name type to number

  const nameTypesEntries = Object.entries(LOCAL_SETTINGS.MENU_OPTIONS.formInputDISAItemPersonNameType);
  referentData.names.forEach(name => {
    const nameTypeAsLabel = name.name_type,
          nameTypeAsID_all = nameTypesEntries.find(n => n[1] === nameTypeAsLabel);
    name.name_type = nameTypeAsID_all ? nameTypeAsID_all[0] : '';
  });

  referentData.FULL_DATA_LOADED = true;

  return referentData;
}

async function getReferentsData(referentIDs, itemID, apiDefinition) {
  return Promise.all(referentIDs.map(referentID => getReferentData(referentID, itemID, apiDefinition)))
}

async function getReferentData(referentId, itemId, apiDefinitions) {

  const apiDefinition = apiDefinitions.get_user_info;
  
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
    const dataURL = apiDefinition.api_url_forID(referentId),
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

// Convert relationships to a hash of arrays by the subject's ID
//  i.e. r[<user ID>] = [ rel1, rel2, etc. ]

function preprocessRelationshipsData(relationshipData) {

  const relHash = {};

  relationshipData.store.forEach(rel => {
    if (!relHash[rel.data.sbj.id]) {
      relHash[rel.data.sbj.id] = []
    } 
    relHash[rel.data.sbj.id] = relHash[rel.data.sbj.id].concat(
      relationshipData.store
        .filter(rel2 => rel2.data.sbj === rel.data.sbj)
        .map(x => Object.assign({ relTripleId: x.id }, x.data))
    )
  });
// console.log('QQQQQQ', relHash)
  return relHash;
}

async function getRelationshipsData(itemId, apiDefinition) {
  const dataURL = `/data/sections/${itemId}/relationships/`, // @todo Birkin needs to include this in his APIs list
        response = await fetch(dataURL, { 
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        }), // @todo need to handle errors
        dataJSON = await response.json();
  return preprocessRelationshipsData(dataJSON);
}

window.getRelationshipsData = getRelationshipsData;

export { getSourceData, getItemData, getReferentData, getRelationshipsData }
