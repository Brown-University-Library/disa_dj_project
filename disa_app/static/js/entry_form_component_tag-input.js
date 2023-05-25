
// @todo load tagify as module

// Tagify doc
//   https://yaireo.github.io/tagify/
// On two-way interactions between child components and their parent via v-model, see
//   https://vuejs.org/v2/guide/components.html#Using-v-model-on-Components

const template = `
    <input v-bind:value="value"
           v-on:change="$emit('input', $event.target.value)"
           class="disa-tags-input form-select"></input>
`;

const componentDefinition = {

  template,
  name: 'disa-tags',
  props: {
    // settings: Object,
    value: String,
    suggestions: Object,
    'single-value': Boolean,
    'on-change': String
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
              enabled: 0, // show suggestions on focus
              maxItems: 1000
            }
          };

    // Set the @single attribute to make it a drop-down equivalent
    // (with ability to add your own text)

    if (this.singleValue) {
      tagifySettings.mode = 'select';
    }

    console.log('TAGIFY INIT', {tagifySettings, el: this.$el, elVal: this.value, whitelist});
    this.tagify = new Tagify(this.$el, tagifySettings);

    // When tagify detects a blur event, pass it up
    //  to the v-on:blur attribute

    this.tagify.on('blur', () => this.$emit('blur'));
  },

  methods: {

    // Given a data structure (as returned from the server)
    // update the field

    updateFromServer(newTagData) {

      function convertDataStructureToTagify(data) {
        if (data.id && (data.label || data.value)) {
          return {
            dbID: data.id,
            value: (data.label || data.value)
          }
        }
      }

      const newTagDataArr = Array.isArray(newTagData) ? newTagData : [newTagData],
            newTagDataArr_tagObjects = newTagDataArr.filter(
              newTag => (typeof newTag === 'object') && (newTag.value || newTag.label)
            );

      // Check if a tag's ID has changed -- if yes, then update

      newTagDataArr_tagObjects.forEach(newTag => {
        const newTagValue = newTag.value || newTag.label,
              matchingOldTagElem = this.tagify.getTagElmByValue(newTagValue);
        if (matchingOldTagElem) {
          const matchingOldTagId = this.tagify.tagData(matchingOldTagElem).dbID;
          if (matchingOldTagId != newTag.id) {
            console.log('UPDATING', { matchingOldTag: this.tagify.tagData(matchingOldTagElem), newTag });
            console.log(`this.tagify.replaceTag(matchingOldTagElem, { dbID: ${newTag.id}, value: ${newTagValue} });`)
            this.tagify.replaceTag(matchingOldTagElem, { dbID: newTag.id.toString(), value: newTagValue });
          }
        }
      });
    }
  }
};

export { componentDefinition as TAG_INPUT_COMPONENT }
