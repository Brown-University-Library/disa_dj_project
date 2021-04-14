
// A DISA form ID badge

const template = `
  <span class="badge rounded-pill bg-secondary text-light"
        vv-on:click="optionsMenu()"
        data-bs-toggle="popover"
        data-bs-content="And here's some amazing content. It's very engaging. Right?" 
        title="yes yes yes"
        >
    ID:{{ displayId(forthis.id || forthis.uuid) }}
  </span>
`;

/*

<span data-bs-toggle="popover" 
      data-bs-content="And here's some amazing content. It's very engaging. Right?" 
      class="badge rounded-pill bg-secondary text-light float-end" 
      data-bs-original-title="LLLLLLink" title="Link to this item">
  ID:895
</span>


*/

/*

  <button type="button" class="btn btn-lg btn-danger" 
          data-bs-toggle="popover" 
          title="Popover title" 
          data-bs-content="And here's some amazing content. It's very engaging. Right?">
          Click to toggle popover
  </button>

*/

const componentDefinition = {
  props: ['forthis'],
  template,
  methods: {
    displayId: function (longId) {
      return longId.toString().slice(-5);
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
