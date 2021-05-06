

// This module has all the functionality for the auto-data backup

// Basically, it's just an array of copies of the data that gets
//  saved every time there's a change

// @todo - throttle this!

const dataBackupMixin = {
/* Vue throws an error if I add this here, 
   so I added it in the entry form initialization ...

  data: function () {
    return {
      dataHistory: []
    }
  }, */
  watch: {
    formData: {
      handler() {
        this.dataHistory.push({
          timestamp: Date.now(),
          data: JSON.stringify(this.formData)
        });

        // Limit backup history
        // @todo - be smarter about this

        while (this.dataHistory.length > 100) {
          this.dataHistory.shift();
        }
        console.log('BACKED UP DATA', this.dataHistory);
      },
      deep: true
    }
  }
}

export { dataBackupMixin }


