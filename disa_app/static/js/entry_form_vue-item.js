import { getItemData } from './entry_form_data_in.js';
import { saveFunctionsMixin } from './entry_form_vue-item_mixin_save.js';
import { dataBackupMixin } from './entry_form_vue-item_mixin_backup.js';
import { DATA_TEMPLATES } from './entry_form_data_templates.js';


// UUID generator
// Source: https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid/2117523#2117523

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

// Routine to initialize the Item form in Vue

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

    created: async function () {

      // If there are no items, create a new one
      // If there ARE items, load extra details for current

      if (!this.formData.doc.references || 
          Object.keys(this.formData.doc.references).length === 0) {
        console.log('NO ITEMS FOUND - CREATING NEW ITEM');
        this.createNewItem();
      } else if (this.currentItemId !== -1) {
        getItemData(this.currentItemId, this.currentItem, this.formData.user_api_info).then(
          currentItemDetails => {
            Object.assign(
              this.formData.doc.references.find(item => item.id === this.currentItemId),
              currentItemDetails
            );
          }
        )
      }

      // Initialize save status

      this.saveStatus = this.SAVE_STATUS.NO_CHANGE;

    },

    computed: {

      currentItem: function() {
        const timeStamp = (new Date()).valueOf(); // TEMP for debugging
        return Object.assign({ timeStamp }, this.formData.doc.references.find(
          item => item.id === this.currentItemId
        ));
      },
      },

      currentReferent: {
        get: function () {
          console.warn(`CurrentRef`, this.currentItem);
          if (this.currentItem && this.currentItem.referents) {
            return this.currentItem.referents.find(
              referent => referent.id === this.currentReferentId
            );
          } else {
            return undefined;
          }
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

      currentItemId: function(itemId) {
        this.updateUrl();
        if (!this.currentItem.FULL_DATA_LOADED) {
          const oldItemData = this.currentItem;
          getItemData(itemId, oldItemData, this.formData.user_api_info).then(itemData => {
            const currentItemIndex = this.formData.doc.references.findIndex(
              item => item.id === itemId
            );
            console.log("UPDATING ITEM", {
              currentItemIndex,
              itemData,
              references: JSON.stringify(this.formData.doc.references, null, 2)
            });
            this.formData.doc.references.splice(currentItemIndex, 1, itemData);
            // this.currentItem = itemData;
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

      // Called when user clicks on +new referent button
      //  Adds a blank data structure to .referents array

      makeNewReferent: function (e) {
        e.preventDefault(); // Link doesn't behave like a link
        const newReferentId = 'new';

        // Copy new referent data structure from template
        //  and add to referent hash

        const blankReferentDataStructure = DATA_TEMPLATES.REFERENT,
              updatedFields = {
                id: newReferentId,
                record_id: this.currentItemId
              },
              newReferentData = Object.assign({},
                blankReferentDataStructure, 
                updatedFields
              );

        console.log('CREATE REFERENT DATA', newReferentData);

        this.currentItem.referents.push(newReferentData);
        this.currentReferentId = newReferentId; // Note: triggers referent save
        return false;
      },

      deleteReferent: function (referent) {
        // e.preventDefault(); // Link doesn't behave like a link
        console.log('DELETE REFERENT', referent);
        this.deleteReferentOnServer(referent).then(
          _ => {
            const referentIndex = this.currentItem.referents.findIndex(r => r === referent);
            this.currentItem.referents.splice(referentIndex, 1);
          }
        );
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


        this.currentNameId = -1;
        this.currentReferentId = -1;
        this.currentItemId = newItemId;
      },

      // Delete Item on server, then delete locally.
      //  Set current Item to first in references array,
      //  or (if no others exist) create a new Item

      deleteItem: function(item) {
        console.log('DELETE ITEM', item);
        this.deleteItemOnServer(item).then(_ => {
          console.log('DELETE ITEM LOCALLY');
          const itemIndex = this.formData.doc.references.findIndex(r => r.id === item.id);
          this.formData.doc.references.splice(itemIndex, 1);
          if (this.formData.doc.references.length > 0) {
            this.currentItemId = this.formData.doc.references[0].id
          } else {
            this.createNewItem();
          }
        });
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

        if (!referent || !referent.id || referent.id === 'new') {
          displayLabel = 'New person';
        } else if (referent.first || referent.last) {
          displayLabel = (referent.first ? referent.first : '') +
                          (referent.last ? ' ' + referent.last : '');
        } else if ( referent.names && referent.names.length && 
                    (referent.names[0].first || referent.names[0].last)) {
          displayLabel = `${referent.names[0].first} ${referent.names[0].last}`
        } else {
          displayLabel = `Individual-${referent.id}`;
        }

        return displayLabel;
      },

      // Update URL to reflect current item and referent

      updateUrl: function () {

        let hash = '';

        if (this.currentItemId && this.currentItemId !== -1) {
          hash += `/${this.currentItemId}`;
          if (this.currentReferentId && this.currentReferentId !== -1) {
            hash += `/${this.currentReferentId}`;
          }
        }

        window.location.hash = hash;
      }
    }
  });
}

export { initializeItemForm }
