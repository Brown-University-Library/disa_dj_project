

const template = `
  <span id="save-status"
        class="badge" 
        v-bind:class="STATUS_INFO[$root.saveStatus].classname"
        v-text="STATUS_INFO[$root.saveStatus].displayText">
  </span>`;

const componentDefinition = {
  props: [],
  template,
  data: function () {
    return {
      
      // Bootstrap classnames: Primary Secondary Success Danger Warning Info Light Dark

      STATUS_INFO: {
        [this.$root.SAVE_STATUS.NO_CHANGE]: { 
          classname: 'bg-secondary',
          displayText: 'No changes'
        },
        [this.$root.SAVE_STATUS.SAVE_IN_PROGRESS]: {
          classname: 'bg-warning',
          displayText: 'Saving ...'
        },
        [this.$root.SAVE_STATUS.ERROR_BAD_API_ID]: {
          classname: 'bg-danger',
          displayText: 'Bad URL ID'
        },
        [this.$root.SAVE_STATUS.SUCCESS]: {
          classname: 'bg-success',
          displayText: 'Saved'
        }
      }
    }
  },
  computed: {},
  methods: {
    // DOES SAVING TO SERVER BELONG HERE?
    /*
    saveDataToServer({ apiId, data, displayText }) {
      const url = this.$root.API_ENDPOINT_URL[apiId];

      if (url) {
        this.currentStatus = STATUS.SAVE_IN_PROGRESS;
        console.log('SAVING', this.$root.API_ENDPOINT_URL);
      } else {
        this.currentStatus = STATUS.ERROR_BAD_API_ID;
      }
    } */
  }
};

export { componentDefinition as SAVE_STATUS_COMPONENT }


