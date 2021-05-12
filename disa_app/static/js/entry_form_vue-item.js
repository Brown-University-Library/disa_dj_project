import { getItemData, getReferentData } from './entry_form_data_in.js';
import { saveFunctionsMixin } from './entry_form_vue-item_mixin_save.js';
import { dataBackupMixin } from './entry_form_vue-item_mixin_backup.js';

function initializeItemForm(dataAndSettings, {DISA_ID_COMPONENT, TAG_INPUT_COMPONENT, SAVE_STATUS_COMPONENT}) {

  dataAndSettings.dataHistory = []; // not sure why Vue doesn't let me add this in the mixin ...

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

    mixins: [ saveFunctionsMixin, dataBackupMixin ],

    // Initializing routine

    created: function () {

      // Initialize item data
      // @todo THIS SHOULD CALL A METHOD this.loadItemData(itemID)

      if (this.currentItemId !== -1) {
        getItemData(this.currentItemId, this.currentItem, this.formData.user_api_info).then(currentItemDetails => {
          this.formData.doc.references[this.currentItemId] = currentItemDetails;
        });
      }
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

      // Computed properties for translating to/from 
      //  Tagify's input requirements

      currentReferentTribesForTagify: {
        get: function() {
          if (Array.isArray(this.currentReferent.tribes)) {
            return JSON.stringify(this.currentReferent.tribes.map(
              tribe => {
                return {
                  value: tribe.value,
                  dbID: tribe.id
                }
              }
            ));
          } else {
            return '';
          }
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

      // LOAD ROUTINES

      // If currentItemId changes, load new item data (if necessary)
      //  Also update date fields for this item

      currentItemId: function(itemId) {
        this.updateUrl();
        const oldItemData = this.currentItem;
        if (!this.currentItem.FULL_DATA_LOADED) {
          getItemData(itemId, oldItemData).then(
            itemData => this.formData.doc.references[itemId] = itemData
          );
        }
      },

      // If currentReferentId changes, load new referent data & update URL

      currentReferentId: function(referentId) {
        this.updateUrl();
        if (!this.currentReferent.FULL_DATA_LOADED) {
          getReferentData(referentId, this.currentItemId, this.loadCurrentReferentAPI).then(
            referentData => this.currentItem.referents[referentId] = referentData
          );
        }
      },

      // If date fields in form change, update data structure with
      //  form field values
      /*
      watchMeToTriggerItemDateSync: function (dateString) {
        this.currentItem.date = [
          this.currentItemDate_month,
          this.currentItemDate_day,
          this.currentItemDate_year
        ].join('-');
      } */
    },

    methods: {

      makeNewReferent: function (e) {
        const newReferentId = 'new'; // uuidv4();
        e.preventDefault(); // Link doesn't behave like a link
        /* EVENTUALLY ...

          const newReferent = getReferentData(), // No parameter = new
                newReferentId = newReferent.id,
                this.currentItem.referents[newReferentId] = newReferent;

        */

        // Copy new referent data structure from template
        //  and add to referent hash

        const blankReferentDataStructure = JSON.parse(
          JSON.stringify(this.NEW_USER_TEMPLATE)
        );

        console.log('Adding new referent', blankReferentDataStructure);

        blankReferentDataStructure.id = newReferentId;
        blankReferentDataStructure.FULL_DATA_LOADED = true;

        this.currentItem.referents[newReferentId] = blankReferentDataStructure;
        this.currentReferentId = newReferentId;
        return false;
      },
      // (is this used?)
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
      },

      getReferentDisplayLabel: function (referent) {
        let displayLabel;
        if (referent.first || referent.last) {
          displayLabel = `${referent.first} ${referent.last}`;
        } else if ( referent.names && referent.names.length && 
                    (referent.names[0].first || referent.names[0].last)) {
          displayLabel = `${referent.names[0].first} ${referent.names[0].last}`
        } else if (!referent.id || referent.id === 'new') {
          displayLabel = 'New person';
        } else {
          displayLabel = `Individual-${referent.id}`;
        }

        return displayLabel;
      },

      // Update URL to reflect current source, item, referent

      updateUrl: function () {
        window.location.hash = `/${this.currentItemId}/${this.currentReferentId}`;
      }
    }
  });
}

export { initializeItemForm }
