
import { getSourceData }              from './entry_form_data_in.js';
import { DISA_ID_COMPONENT }          from './entry_form_component_id-badge.js';
import { TAG_INPUT_COMPONENT }        from './entry_form_component_tag-input.js';
import { SAVE_STATUS_COMPONENT }      from './entry_form_component_save-status.js';
import { initializeSourceForm }       from './entry_form_vue-citation.js';
import { initializeItemForm }         from './entry_form_vue-item.js';

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

  // Load the source data

  let dataAndSettings = await getSourceData();

  // Set currentItemId (initial item to display):
  //  either from URL, or the first item, or undefined

  if (initDisplay.itemId) {
    dataAndSettings.currentItemId = initDisplay.itemId
  } else if (false && dataAndSettings.formData.doc.references[0] && 
             dataAndSettings.formData.doc.references[0].id) { // @todo DISABLED
    dataAndSettings.currentItemId = dataAndSettings.formData.doc.references[0].id;
  } else {
    dataAndSettings.currentItemId = -1;
  }

  // Set first referent to display: from URL or none

  const NO_REFERENT = -1;
  dataAndSettings.currentReferentId = initDisplay.referentId || NO_REFERENT;

  // Initialize save status register

  dataAndSettings.saveStatus = dataAndSettings.SAVE_STATUS.NO_CHANGE;

  // New relationship form visibility toggle

  dataAndSettings.newRelationshipFormVisible = false;

  // Current group ID register

  dataAndSettings.currentGroupId = -1;

  // confirm-delete modal

  dataAndSettings.CONFIRM_DELETE_MODAL = undefined;

  return dataAndSettings;
}

// Main routine

async function main() {

  // Get initial item/referent display selector from URL

  const initDisplay = getRoute();

  // Get the data structure to pass to Vue

  let dataAndSettings = await loadAndInitializeData(initDisplay);
  console.log('SOURCE DATA PRIOR TO VUE (item details not yet loaded)', JSON.stringify(dataAndSettings, null, 2));

  // If item specified in URL, select tab

  if (initDisplay.itemId) {
    document.getElementById('item-tab').click();
  }

  // TEMP: Fill in source title at top
  // @todo this will be better when the two tabs fall under the same Vue instance

  document.getElementById('sourceTitle').innerText = dataAndSettings.formData.doc.fields.title || '[New source]';

  // Initialize forms in Vue

  initializeSourceForm(dataAndSettings);
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