
import {LOCAL_SETTINGS} from './entry_form_settings.js';

// Convert an array into a form that Tagify understands

function prepareForTagify(data) {

  let tagifiedData;
  if (Array.isArray(data) && data.length > 0) {
    if (data[0].id && data[0].label) {
      tagifiedData = JSON.stringify(data.map(dataItem => {
        return { value: dataItem.label, dbID: dataItem.id }
      }));
    }
  } else {
    tagifiedData = '[]';
  }

  console.log('TAGIFYING FROM ', data, ' TO ', tagifiedData);

  return tagifiedData;
}




// SOURCE

function preprocessSourceData(data) {

  // Convert date formats so that they can be inserted into
  //  date input element

  function getDateInFormFormat(dbDateString) {
    const date = new Date(dbDateString),
          yyyy = date.getFullYear(),
          mm = (date.getMonth() + 1).toString().padStart(2,'0'),
          dd = date.getDate().toString().padStart(2,'0')
    return `${yyyy}-${mm}-${dd}`;
  }
  
  data.formData.doc.fields.date = getDateInFormFormat(data.formData.doc.fields.date);
  data.formData.doc.fields.accessDate = getDateInFormFormat(data.formData.doc.fields.accessDate);
  
  // Make array of references/items into a hash by ID
  //  Use the template data structure

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


// ITEM

function preprocessItemData(itemData, oldItemData, relationshipsData, referentData) {

  const itemDate = itemData.rec.date ? new Date(itemData.rec.date) : null;

  // Location info: ID is present only in oldItemData BUT
  //  Type is located only in itemData -- need to combine

  const locationInfo = itemData.rec.locations.map(location1 => {
    const location2 = oldItemData.location_info.find(
      loc2 => loc2.location_name === location1.label
    );
    return {
      id: location1.id,
      name: location2.location_name,
      type: location2.location_type
    }
  });

  const locationDefaults = {
      'Locale': { name: '' },
      'City': { name: '' },
      'Colony/State': { name: '' }
    },
    locationInfoByType = locationInfo.reduce(
      (locationHash, location) => Object.assign(
        {}, locationHash, { [location.type]: location }
      ), locationDefaults
    );

  console.log("LOCATIONS", {locationInfo, locationInfoByType});

  let processedData = {
    // date: itemData.rec.date,
    dateParts: {
      day:   itemDate ? itemDate.getDate()      : undefined,
      month: itemDate ? (itemDate.getMonth() + 1).toString().padStart(2, '0') : -1,
      year:  itemDate ? itemDate.getFullYear()  : undefined
    },
    id: itemData.rec.id,
    location_info: locationInfoByType,
    national_context_id: itemData.rec.national_context,
    reference_type_id: 'IGNORE ME', // itemData.rec.record_type.id,
    // reference_type_name: itemData.rec.record_type.label,
    // Convert array of referents to a hash by referent ID
    referents: referentData.reduce(
      (referentHash, referent) => {
        referentHash[referent.id] = referent;
        return referentHash;
      },
      {}
    ),
    relationships: relationshipsData,
    // referents: getAdditionalReferentInfo(itemData.entrants),
    groups: itemData.groups.group_data,
    transcription: 'IGNORE ME', // itemData.rec.transcription,
    image_url: itemData.rec.image_url,

    // I have no idea why this works -- without these properties being inside of a
    //  wrapper object, they're not Vue-responsive

    kludge: {
      transcription: itemData.rec.transcription,
      reference_type_id: itemData.rec.record_type.id,
      image_url: itemData.rec.image_url
    },

    FULL_DATA_LOADED: true // Flag
  }

  return processedData;
}

// Get item data (including relationships) -- return Promise

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


// REFERENT

// Referent data - called by getItemData

async function getReferentsData(referentIDs, itemID, apiDefinition) {
  return Promise.all(referentIDs.map(
    referentID => getReferentData(referentID, itemID, apiDefinition))
  );
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

  // Tagify fields -- races, tribes, vocation

  referentData.races     = prepareForTagify(referentData.races);
  referentData.tribes    = prepareForTagify(referentData.tribes);
  referentData.vocations = prepareForTagify(referentData.vocations);

  referentData.FULL_DATA_LOADED = true;

  return referentData;
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


// RELATIONSHIP

// Get relationships data

function preprocessRelationshipsData(relationshipData) {
  return relationshipData.store;
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

export { getSourceData, getItemData, getRelationshipsData }
