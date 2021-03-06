

// This module collects all the functionality related to saving to the server


function submitReferentDataToServer() {

  console.log('CALLING ROUTINE TO SUBMIT REFERENT DATA');

  if (this.currentReferent.FULL_DATA_LOADED) {

    // Map data in Vue to what's expected by the API

    const requestBody = JSON.stringify({
      id: this.currentReferent.id,
      age: this.currentReferent.age,
      // name: this.currentReferent.names[0], // @todo - only one name?? BD's test has a .name field
      names: this.currentReferent.names.map(
        name => { name.name_type = "7"; return name }
      ),
      origins: this.currentReferent.origins,
      races: this.currentReferent.races,
      sex: this.currentReferent.sex,
      statuses: [], // this.currentReferent.statuses, // ??
      titles: this.currentReferent.titles.map(
        title => {
          title.name = title.label.valueOf();
          return title 
        }
      ),
      tribes: this.currentReferent.tribes,
      vocations: this.currentReferent.vocations
    });

    console.log('SAVE CURRENT REFERENT');
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
}

function submitItemDataToServer() {

  console.log('CALLING ROUTINE TO SUBMIT ITEM DATA');

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



const saveFunctionsMixin = {

  computed: {

      // Computed properties that are watched to trigger saves

      watchMeToTriggerReferentSave: function () { // (may not be necessary)
        return JSON.stringify(this.currentReferent);
      },

      watchMeToTriggerItemSave: function () {
        // Ignores changes in referents
        const {referents, ...rest} = this.currentItem;
        return JSON.stringify(rest);
      }
  },

  watch: {

      // If current referent info changes, save
      //  (but only if full referent data has been previously loaded)

      currentReferent: {
        handler: submitReferentDataToServer,
        deep: true
      },

      // If the Item data changes (as defined by computed field)
      //  then save

      watchMeToTriggerItemSave: {
        handler: submitItemDataToServer
      }
  }
}

export { saveFunctionsMixin }

