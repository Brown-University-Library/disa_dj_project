
// @todo load tagify as module

/*
const template = `
  <div v-once>
    <textarea v-if="mode === 'textarea'" v-model="value"/>
    <input v-else :value="value" v-on:change="onChange">
  </div>
`; */

const template = `
    <input :value="value" v-on:change="onChange"></input>
`;

const componentDefinition = {
  template,
  name: 'disa-tags',
  props: {
    mode: String,
    settings: Object,
    value: [String, Array],
    onChange: Function
  },
  watch: {
    value(newVal, oldVal) {
      this.tagify.loadOriginalValues(newVal)
    },
  },
  mounted() {
    this.tagify = new Tagify(this.$el, this.settings)
  }
};

export { componentDefinition as TAG_INPUT_COMPONENT }

