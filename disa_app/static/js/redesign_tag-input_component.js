
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
    suggestions: Object
  },

  mounted() {

    const whitelist = Object.keys(this.suggestions).map(
            id => { 
              return { 
                value: this.suggestions[id], 
                dbID: id 
              }
            }
          ),
          // tagifySettings = Object.assign({}, this.settings, whitelist);
          tagifySettings = { whitelist: whitelist };
    console.log('TAGIFY INIT', {tagifySettings, el: this.$el, elVal: this.value});
    this.tagify = new Tagify(this.$el, tagifySettings);
  },
  
  methods: {
    onChange: function(x) { 

      const oldTags = this.value,
            newTags = this.tagify.value.map(tag => { 
                        return { id: tag.dbID, label: tag.value, value: tag.value } 
                      });

      const tagsHaveChanged = oldTags.length !== newTags.length ||
                              newTags.map(newTag => newTag.value)
                                     .some(newTagVal => ! oldTags.includes(newTagVal));

      console.log('TAGIFY ONCHANGE', {event: x, tagify: this.tagify});
      console.log('OLD', oldTags);
      console.log('NEW', newTags);
      console.log('INPUT EL VALUE', this.$el.value);
      console.log('CHANGED', tagsHaveChanged);

      if (tagsHaveChanged) {

      }
    }
  }
};

export { componentDefinition as TAG_INPUT_COMPONENT }
