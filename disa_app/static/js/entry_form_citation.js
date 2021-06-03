
import { getSourceData } from './entry_form_data_in.js';
import { DISA_ID_COMPONENT }          from './entry_form_component_id-badge.js';
import { TAG_INPUT_COMPONENT }        from './entry_form_component_tag-input.js';
import { SAVE_STATUS_COMPONENT }      from './entry_form_component_save-status.js';
import { initializeCitationForm }     from './entry_form_vue-citation.js';
import { initializeItemForm }         from './entry_form_vue-item.js';

// UUID generator
// Source: https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid/2117523#2117523

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

// Parse URL for item and/or person to display
//  URL format: <url><DOC ID>/#/<ITEM ID>/<PERSON ID>

function getRoute() {
  const [itemId, personId] = window.location.hash.replace(/^[#\/]+/, '').split('/');
  return { 
    itemId: parseInt(itemId) || undefined,
    referentId: parseInt(personId) || undefined
  };
}

async function loadAndInitializeData(initDisplay) {

  let dataAndSettings = await getSourceData();

  // Set initial item to display:
  //  from URL, assign to first item, or undefined

  dataAndSettings.currentItemId = 
    initDisplay.itemId || 
    Object.keys(dataAndSettings.formData.doc.references)[0] ||
    undefined;

  // Set first referent to display: from URL or none

  const NO_REFERENT = -1;
  dataAndSettings.currentReferentId = initDisplay.referentId || NO_REFERENT;

  // Initialize save status register

  dataAndSettings.saveStatus = dataAndSettings.SAVE_STATUS.NO_CHANGE;

  // New relationship register

  dataAndSettings.newRelationship = { obj: null, rel: null }

  return dataAndSettings;
}

// Main routine

async function main() {

  // Get initial item/referent display selector from URL

  const initDisplay = getRoute();

  // Get the data structure to pass to Vue

  let dataAndSettings = await loadAndInitializeData(initDisplay);
  console.log('MAIN DATA PRIOR TO VUE', JSON.stringify(dataAndSettings, null, 2));

  // If item specified in URL, select tab

  if (initDisplay.itemId) {
    document.getElementById('item-tab').click();
  }

  // TEMP: Fill in source title at top
  // @todo this will be better when the two tabs fall under the same Vue instance

  document.getElementById('sourceTitle').innerText = dataAndSettings.formData.doc.fields.title || '[New source]';

  // Initialize forms in Vue

  initializeCitationForm(dataAndSettings);
  initializeItemForm(dataAndSettings, {DISA_ID_COMPONENT, TAG_INPUT_COMPONENT, SAVE_STATUS_COMPONENT});
}

main();

/*
window.addEventListener('load', () => { 
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  });
 }) */




/*

  @todo
  Only have one Vue instance for both tabs
  Add GUI editor for transcription (convert to markdown?)

*/

