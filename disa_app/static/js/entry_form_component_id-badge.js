
// A DISA form ID badge

const template = `
  <span class="badge rounded-pill bg-secondary text-light disa-id-badge"
        vv-on:click="optionsMenu()"
        data-bs-toggle="popover"
        data-bs-animation="false"
        title="Click for sharing options">
    ID:{{ displayId(forthis.id || forthis.uuid) }}
  </span>
`;

const componentDefinition = {
  props: ['forthis'],
  template,
  methods: {
    displayId: function (longId) {
      return longId.toString().slice(0,5);
    },
    optionsMenu: function(x, e) {
      console.log('options!', x, e);
    }
  },
  mounted: function () {
    const tooltip =  new bootstrap.Tooltip(this.$el);
    tooltip.html = true;
    tooltip.title = "YES and <em>yes</em>!";
    console.log('MOUNTED', tooltip);
/*
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    }); */
  }
};

export { componentDefinition as DISA_ID_COMPONENT }
