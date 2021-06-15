

// These are the definitions of 'blank' data structures
// They're necessary in part because Vue likes to have all
//  the properties defined upon creation, which doesn't mix well
//  with incremental enhancement (which is the way that the API works).
// Also, they're useful when creating a blank entry to create a 
//  new record


const ITEM_TEMPLATE = {
  dateParts: {
    day:undefined,
    month:-1,
    year:undefined
  },
  id: '',
  location_info: {
    Locale:{name: ''},
    City:{name: ''},
    'Colony/State':{
      id: '',
      name: '',
      type: ''
    }
  },
  national_context_id: '',
  reference_type_id: 'IGNORE ME',
  referents:[],
  relationships:[],
  groups:[],
  transcription: 'IGNORE ME',
  image_url: 'IGNORE ME',
  kludge:{
    transcription: '',
    reference_type_id: '13',
    image_url: ''
  },
  FULL_DATA_LOADED:false
};

const REFERENT_TEMPLATE = {
  age: undefined,
  id: 'new',
  names:[
    {
      first:'',
      id:'name',
      last:'',
      name_type:'Unknown'
    }
  ],
  origins:'[]', // Tagify
  races:'[]', // Tagify
  record_id: undefined,
  roles:'[]', // Tagify
  sex:'',
  titles:[],
  tribes:'[]', // Tagify
  vocations:'[]', // Tagify
  FULL_DATA_LOADED: true
};

// Make a copy of the given template

function copyTemplate(template) {
  return JSON.parse(
    JSON.stringify(template)
  )
}
const DATA_TEMPLATES = {
  get ITEM() {
    return JSON.parse(
      JSON.stringify(ITEM_TEMPLATE)
    )
  get REFERENT() {
    return copyTemplate(REFERENT_TEMPLATE)
  }
}

export { DATA_TEMPLATES }
