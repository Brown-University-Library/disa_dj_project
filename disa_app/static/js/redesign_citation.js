
import {getSourceData, getItemData, getReferentData, saveReferentData} from './redesign_data.js';
import { DISA_ID_COMPONENT } from './redesign_id_component.js';
import { TAG_INPUT_COMPONENT } from './redesign_tag-input_component.js';
import { SAVE_STATUS_COMPONENT } from './redesign_save-status_component.js';


const DATA_BACKUP = [];

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

// Get callback for change in source type
// (it's a callback in order to bake in the dataAndSettings object)

function getUpdateCitationFieldVisibilityCallback(FIELDS_BY_DOC_TYPE) {

  const requiredFieldsHeader = document.getElementById('required-fields-header'),
        optionalFieldsHeader = document.getElementById('optional-fields-header');

  return function(citationTypeId) {

    const citationFields = document.querySelectorAll('#citation-fields > div'),
          fieldStatus = FIELDS_BY_DOC_TYPE[citationTypeId];

    requiredFieldsHeader.hidden = fieldStatus.required.length === 0;
    optionalFieldsHeader.hidden = fieldStatus.optional.length === 0;

    citationFields.forEach((citationField, defaultOrderIndex) => { 
      const fieldId = citationField.id;
      if (fieldStatus.required.includes(fieldId)) {
        citationField.hidden = false;
        citationField.style.order = (100 + defaultOrderIndex);
      } else if (fieldStatus.optional.includes(fieldId)) {
        citationField.hidden = false;
        citationField.style.order = (200 + defaultOrderIndex);
      } else {
        citationField.hidden = true;
      }
    });
  }
}

function initializeCitationForm(dataAndSettings) {

  const updateCitationFieldVisibility = getUpdateCitationFieldVisibilityCallback(dataAndSettings.FIELDS_BY_DOC_TYPE);
  
  new Vue({
    el: '#citation-form',
    data: dataAndSettings,
    watch: {
      'formData.doc.citation_type_id': updateCitationFieldVisibility
    },
    methods: {
      openItemTab: function () {
        document.getElementById('item-tab').click();
      },
      onSubmitForm: function(x) { 
        // @todo finish this
        console.log({ 
          submitEvent: x, 
          data: JSON.parse(JSON.stringify(this.formData))
        })
      }
    },
    mounted: updateCitationFieldVisibility(dataAndSettings.formData.doc.citation_type_id)
  });
}

function initializeItemForm(dataAndSettings) {

  window.itemFormVue = new Vue({

    el: '#Items',

    // Data is not a function (as usual with Vue) b/c changes should be 
    //  reflected between this and the previous form

    data: dataAndSettings, 

    components: {
      'disa-id': DISA_ID_COMPONENT,
      'disa-tags': TAG_INPUT_COMPONENT,
      'disa-save-status': SAVE_STATUS_COMPONENT
    },

    mounted: function () {

      // Initialize item date fields

      const itemDate = new Date(this.currentItem.date);
      this.currentItemDate_day = itemDate.getDate();
      this.currentItemDate_month = itemDate.getMonth();
      this.currentItemDate_year = itemDate.getFullYear();
      Array.from(document.getElementsByClassName('taggedInput')).forEach(
        taggedInput => new Tagify(taggedInput)
      )
    },

    computed: {

      currentItem: function() {
        return this.formData.doc.references[this.currentItemId]
      },
      currentReferent: function () {
        return this.currentItem.referents[this.currentReferentId]
      },

      currentItemLocationCity: function () {
        if (this.currentItem.location_info) {
          const cityLocation = this.currentItem.location_info.find(
            loc => loc.location_type === 'City'
          );
          return cityLocation && cityLocation.location_name 
            ? cityLocation.location_name : undefined;
        } else {
          return undefined;
        }
      },

      currentItemLocationColonyState: function () {
        if (this.currentItem.location_info) {
          const colonyStateLocation = this.currentItem.location_info.find(
            loc => loc.location_type === 'Colony/State'
          );
          return colonyStateLocation && colonyStateLocation.location_name 
            ? colonyStateLocation.location_name : undefined;
        } else {
          return undefined;
        }
      },

      currentItemLocationLocale: function () {
        if (this.currentItem.location_info) {
          const localeLocation = this.currentItem.location_info.find(
            loc => loc.location_type === 'Locale'
          );
          return localeLocation && localeLocation.location_name 
            ? localeLocation.location_name : undefined;
        } else {
          return undefined;
        }
      },

      // Computed properties to trigger saves

      watchMeToTriggerReferentSave: function () { // (may not be necessary)
        return JSON.stringify(this.currentReferent);
      },

      watchMeToTriggerItemSave: function () {
        // Ignore changes in referents
        const {referents, ...rest} = this.currentItem;
        return JSON.stringify(rest);
      },

      // Computed properties to translate to/from server data structure
      //  (this is watched for changes to update data structure)

      watchMeToTriggerItemDateSync: function () {
        return `${this.currentItemDate_month}/${this.currentItemDate_day}/${this.currentItemDate_year}`;
      },

      // Computed properties for translating to/from 
      //  Tagify's input requirements

      currentReferentTribesForTagify: {
        get: function() {
          return JSON.stringify(this.currentReferent.tribes.map(
            tribe => {
              return {
                value: tribe.value,
                dbID: tribe.id
              }
            }
          ));
        },
        set: function(newValue) {
          console.log('CHANGING TRIBES TO', newValue);
          this.currentReferent.tribes = JSON.parse(newValue).map(
            tribeTag => { 
              return { 
                label: tribeTag.value, 
                value: tribeTag.value, 
                id: tribeTag.dbID 
              } 
            }
          );
        }
      },

      currentReferentRaceID: {
        get: function () {
          return (Array.isArray(this.currentReferent.races) && this.currentReferent.races.length)
            ? this.currentReferent.races[0].id 
            : undefined;
        },
        set: function (raceID) {
          if (! Array.isArray(this.currentReferent.races)) {
            this.currentReferent.races = [];
          }
          this.currentReferent.races[0] = { id: raceID };
        }
      },

      // Compute API endpoints

      saveCurrentReferentAPI: function () {
        const apiDefinition = this.formData.user_api_info.update_user_info_DETAILS,
              qualifiedURL = apiDefinition.api_url.replace('THE-REFERENT-ID', this.currentReferentId);
        return Object.assign({}, apiDefinition, { api_url: qualifiedURL });
      },

      loadCurrentReferentAPI: function () {
        const apiDefinition = this.formData.user_api_info.get_user_info,
              qualifiedURL = apiDefinition.api_url.replace('THE-REFERENT-ID', this.currentReferentId);
        return Object.assign({}, apiDefinition, { api_url: qualifiedURL });
      }
    },

    // So as not to clash with Django templates, if needed

    delimiters: ['v{','}v'], 

    watch: {

      // SAVE ROUTINES

      // Backup data whenever anything changes

      formData: {
        handler() {
          DATA_BACKUP.push({
            timestamp: Date.now(),
            data: JSON.stringify(this.formData)
          });

          // Limit backup history
          // @todo - be smarter about this

          while (DATA_BACKUP.length > 100) {
            DATA_BACKUP.shift();
          }
          console.log('BACKED UP DATA', DATA_BACKUP);
        },
        deep: true
      },

      // If current referent info changes, save
      //  (if full referent data has been previously loaded)

      currentReferent: {
        handler() {
          if (this.currentReferent.FULL_DATA_LOADED) {

            const requestBody = JSON.stringify({
              id: this.currentReferent.id,
              age: this.currentReferent.age,
              // name: this.currentReferent.names[0], // @todo - only one name?? BD's test has a .name field
              "names": this.currentReferent.names.map(
                name => { name.name_type = "7"; return name }
              ),
              "origins": this.currentReferent.origins,
              "races": this.currentReferent.races,
              "sex": this.currentReferent.sex,
              "statuses": [], // this.currentReferent.statuses, // ??
              "titles": this.currentReferent.titles.map(
                title => {
                  title.name = title.label.valueOf();
                  return title 
                }
              ),
              "tribes": this.currentReferent.tribes,
              "vocations": this.currentReferent.vocations
            });

            console.log('SAVE CURRENT REFERENT');
            console.log('WTF WTF?', requestBody);
            this.saveStatus = this.SAVE_STATUS.SAVE_IN_PROGRESS;
            saveReferentData(
              this.currentReferentId, 
              this.currentItemId,
              this.saveCurrentReferentAPI,
              requestBody
            );
            window.setTimeout( // FAKE FETCH
              () => { 
                this.saveStatus = this.SAVE_STATUS.SUCCESS; 
                console.log('SAVED!'); 
              }, 
              2000
            );
          }
        },
        deep: true
      },

      // If current Item info changes, save

      watchMeToTriggerItemSave: {
        handler() {
          if (this.currentItem.FULL_DATA_LOADED) {
            this.saveStatus = this.SAVE_STATUS.SAVE_IN_PROGRESS;

            // Only save current Item (without Referent data)
  
            const { referents, ...currentItemDataNoReferents } = this.currentItem;
            const currentItemCopy = JSON.parse(JSON.stringify(currentItemDataNoReferents));
  
            console.log('SAVING ITEM DATA ...', currentItemCopy);
  
            window.setTimeout( // FAKE FETCH
              () => this.saveStatus = this.SAVE_STATUS.SUCCESS, 
              2000
            );
          }
        }
      },

      // LOAD ROUTINES

      // If currentItemId changes, load new item data (if necessary)
      //  Also update date fields for this item

      currentItemId: function(itemId) {
        const oldItemData = this.currentItem;
        if (!this.currentItem.FULL_DATA_LOADED) {
          getItemData(itemId, oldItemData).then(
            itemData => this.formData.doc.references[itemId] = itemData
          );
        }
      },

      // If currentReferentId changes, load new referent data

      currentReferentId: function(referentId) {
        if (!this.currentReferent.FULL_DATA_LOADED) {
          getReferentData(referentId, this.currentItemId, this.loadCurrentReferentAPI).then(
            referentData => this.currentItem.referents[referentId] = referentData
          );
        }
      },

      // If date fields in form change, update data structure with
      //  form field values

      watchMeToTriggerItemDateSync: function (dateString) {
        this.currentItem.date = [
          this.currentItemDate_month,
          this.currentItemDate_day,
          this.currentItemDate_year
        ].join('-');
      }
    },

    methods: {

      makeNewReferent: function (e) {
        const newReferentId = 'new'; // uuidv4();
        e.preventDefault(); // Link doesn't behave like a link
        this.currentItem.referents[newReferentId] = {
          id: newReferentId,
          names: []
        };
        this.currentReferentId = newReferentId;
        return false;
      },
      getReferentDisplayLabel: function (referent) {
        return referent ? `${referent.first} ${referent.last}` : 'Hmmm';
      },
      makeNewReferentName: function () {
        const newReferentId = uuidv4();
        this.currentReferent.names.push({
          id: newReferentId
        });
        this.currentNameId = newReferentId;
      },
      makeNewItem: function () {
        const newItemId = uuidv4();
        this.formData.doc.references[newItemId] = {
          id: newItemId,
          citation_id: this.formData.doc.id,
          referents: {}
        };
        this.currentItemId = newItemId;
      },

      // Take a long UUID and make a display version
      // @todo only have this in the ID badge component?

      displayId: function (longId) {
        return longId.toString().slice(-5);
      },

      // Take a long string (especially transcriptions) 
      // and make it into a display title

      makeItemDisplayTitle: function (item, length=100) {

        let displayTitle;

        if (item.transcription) {
          displayTitle = item.transcription.replaceAll(/<[^>]+>/g, '')
              .slice(0,length) + '…';
        } else {
          // displayTitle = `Item ID:${this.displayId(item.id)}`;
          displayTitle = 'New item';
        }
        return displayTitle
      }
    }
  });
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

  dataAndSettings.currentReferentId = initDisplay.referentId || -1;

  // Load full data for current item

  dataAndSettings.formData.doc.references[dataAndSettings.currentItemId] 
    = await getItemData(dataAndSettings.currentItemId, 
                        dataAndSettings.formData.doc.references[dataAndSettings.currentItemId]);

  // Initialize save status register

  dataAndSettings.saveStatus = dataAndSettings.SAVE_STATUS.NO_CHANGE;

  // 'glue' between form fields and data structure

  dataAndSettings.currentItemDate_day = undefined;
  dataAndSettings.currentItemDate_month = undefined;
  dataAndSettings.currentItemDate_year = undefined;

  return dataAndSettings;
}

// Main routine

async function main() {

  // Get initial item/referent display selector from URL

  const initDisplay = getRoute();

  // Get the data structure to pass to Vue

  let dataAndSettings = await loadAndInitializeData(initDisplay);
  console.log(dataAndSettings);

  // If item specified in URL, select tab

  if (initDisplay.itemId) {
    document.getElementById('item-tab').click();
  }

  // Initialize forms

  initializeCitationForm(dataAndSettings);
  initializeItemForm(dataAndSettings);
}

main();

/*

  @todo

  Use Tagify (as a Vue component?) on appropriate fields
    https://yaireo.github.io/tagify/
  Create a Vue component for ID badges
  Add relationships between people
  Add GUI editor for transcription (convert to markdown?)

*/

