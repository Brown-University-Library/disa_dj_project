

const template = `
  <span>
  <!-- STATUS BUTTON -->

  <span id="save-status"
        class="badge" 
        v-bind:class="STATUS_INFO[$root.saveStatus].classname"
        v-html="STATUS_INFO[$root.saveStatus].displayText"
        data-bs-toggle="modal" data-bs-target="#data-history-modal">
  </span>
  
  <!-- HISTORY MODAL -->
  
  <div class="modal" tabindex="-1" id="data-history-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">
          Version history<br />
          Click on an entry to restore
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-start"
              data-bs-dismiss="modal"
              v-for="snapshot in $root.dataHistory"
              v-on:click="$root.formData = JSON.parse(snapshot.data)"
              v-text="(new Date(snapshot.timestamp)).toLocaleTimeString()">
          </li>
        </ul>
      <!--
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-start"
              data-bs-dismiss="modal"
              v-for="item in formData.doc.references"
              v-on:click="currentItemId = item.id">
            <div class="ms-2 me-auto"
                 v-text="makeItemDisplayTitle(item, 50)">
            </div>
            <disa-id v-bind:forthis="currentItem" class="float-end"></disa-id>
          </li>
        </ul> -->
      </div>
    </div>
  </div>
</div>
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
          displayText: 'Saving<br />&nbsp;'
        },
        [this.$root.SAVE_STATUS.ERROR_BAD_API_ID]: {
          classname: 'bg-danger',
          displayText: 'Bad URL ID'
        },
        [this.$root.SAVE_STATUS.SUCCESS]: {
          classname: 'bg-success',
          get displayText() { 
            const now = new Date(),
                  h = now.getHours(),
                  m = (now.getMinutes() < 10 ? '0' : '') + now.getMinutes(),
                  s = (now.getSeconds() < 10 ? '0' : '') + now.getSeconds();
            return `Saved<br />${h}:${m}:${s}`;
          }
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


