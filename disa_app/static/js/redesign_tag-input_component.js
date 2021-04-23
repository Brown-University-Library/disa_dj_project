
// @todo load tagify as module

// https://yaireo.github.io/tagify/


const template = `
    <input :value="value" v-on:change="onChange" class="disa-tags-input"
           :data-whitelist="suggestions"></input>
`;

const componentDefinition = {
  template,
  name: 'disa-tags',
  props: {
    mode: String,
    settings: Object,
    value: [String, Array],
    suggestions: [String, Array]
  },
  watch: {
    value(newVal, oldVal) {
      this.tagify.loadOriginalValues(newVal);
      console.log('yessss', this.$el);
    },
  },
  mounted() {
    this.tagify = new Tagify(this.$el, this.settings);
  },
  methods: {
    onChange: function(x) { 
      console.log('AAAA', x);
    }
  }
};

export { componentDefinition as TAG_INPUT_COMPONENT }
