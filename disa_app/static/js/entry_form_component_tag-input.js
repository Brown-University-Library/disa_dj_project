
// @todo load tagify as module

// Tagify doc
//   https://yaireo.github.io/tagify/
// On two-way interactions between child components and their parent via v-model, see
//   https://vuejs.org/v2/guide/components.html#Using-v-model-on-Components

const template = `
    <input v-bind:value="value" vv-on:change="onChange" 
           v-on:change="$emit('input', $event.target.value)"
           class="disa-tags-input"></input>
`;

const componentDefinition = {
  template,
  name: 'disa-tags',
  props: {
    // settings: Object,
    value: String,
    suggestions: Object,
    'single-value': Boolean
  },

  mounted() {

    // The dropdown suggestions are passed via the @suggestions attribute
    //  as a object with keys as IDs and values as the text

    const whitelist = Object.keys(this.suggestions).map(
            id => { 
              return { 
                value: this.suggestions[id], 
                dbID: id 
              }
            }
          ),

          tagifySettings = { 
            whitelist,
            dropdown: {
              enabled: 0 // show suggestions on focus
            }
          };

    // Set the @single attribute to make it a drop-down equivalent
    // (with ability to add your own text)

    if (this.singleValue) {
      tagifySettings.mode = 'select';
    }

    console.log('TAGIFY INIT', {tagifySettings, el: this.$el, elVal: this.value, whitelist});
    this.tagify = new Tagify(this.$el, tagifySettings);
  }
};

export { componentDefinition as TAG_INPUT_COMPONENT }
