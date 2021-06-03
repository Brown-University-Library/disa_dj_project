import { getItemData, getRelationshipsData } from './entry_form_data_in.js';
import { saveFunctionsMixin } from './entry_form_vue-item_mixin_save.js';
import { dataBackupMixin } from './entry_form_vue-item_mixin_backup.js';


// UUID generator
// Source: https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid/2117523#2117523

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}


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

      currentReferent: {
        get: function () {
          return this.currentItem.referents[this.currentReferentId.toString()]
          /*
          return this.currentItem.referents.find(
            referent => referent.id === this.currentReferentId
          ); */
        },
        set: function (referentData) { // @todo I don't think this is used
          let oldReferentData = this.currentItem.referents.find(
            referent => referent.id === this.currentReferentId
          );
          if (oldReferentData) {
            oldReferentData = referentData;
          }
        }
      },

      currentReferentRelationships: function () {
        return this.currentItem.relationships.filter(
          relationship => relationship.data.sbj.id === this.currentReferentId
        )
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
        if (!this.currentItem.FULL_DATA_LOADED) {
          const oldItemData = this.currentItem;
          getItemData(itemId, oldItemData).then(itemData => {
            this.formData.doc.references[itemId] = itemData;
          });
        }
      },

      // If currentReferentId changes, load new referent data & update URL

      currentReferentId: function(referentId) {
        this.updateUrl();
        /* DISABLED FOR NOW
        if (!this.currentReferent.FULL_DATA_LOADED) {
          getReferentData(referentId, this.currentItemId, this.loadCurrentReferentAPI).then(
            referentData => this.currentItem.referents[referentId] = referentData
          );
        } */
      }
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

      // Creates a new, empty item in the data structure and make it 
      //  the current item
      // NOTE: does not communicate with server -- that is handled
      //       by the currentItemId watcher

      createNewItem: function () {
        const newItemId = 'new'; // uuidv4();
        const initData = Object.assign(DATA_TEMPLATES.ITEM, {
          national_context_id:'2',
          reference_type_id:'13',
          FULL_DATA_LOADED: true
        });
        this.formData.doc.references[newItemId] = initData;

        /*
        this.formData.doc.references[newItemId] = {
          "dateParts":{
             "day":"",
             "month":"-1",
             "year":""
          },
          "id":8,
          "location_info":{
             "Locale":{
                "id": -1,
                "name":"",
                "type":"Locale"
             },
             "City":{
                "id": -1,
                "name":"",
                "type":"City"
             },
             "Colony/State":{
                "id": -1,
                "name":"",
                "type":"Colony/State"
             }
          },
          "national_context_id":"2",
          "reference_type_id":"13",
          "referents":{},
          "relationships":[],
          "groups":[],
          "transcription":"",
          kludge: {
            transcription: '',

          },
          "image_url":"",
          "FULL_DATA_LOADED":true
        }; */

        this.currentNameId = -1;
        this.currentReferentId = -1;
        this.currentItemId = newItemId;
      },

      // Take a long string (especially transcriptions) 
      // and make it into a display title

      makeItemDisplayTitle: function (item, length=100) {

        let displayTitle;

        if (item.transcription) {
          const transcriptionNoHTML = item.kludge.transcription.replaceAll(/<[^>]+>/g, ''),
                truncatedTitle = transcriptionNoHTML.slice(0,length);
          displayTitle = truncatedTitle + (truncatedTitle.length < transcriptionNoHTML.length ? '…' : '');
        } else {
          displayTitle = '[No title]';
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
