

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
  referents:{},
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

const DATA_TEMPLATES = {
  get ITEM() {
    return JSON.parse(
      JSON.stringify(ITEM_TEMPLATE)
    )
  }
}


export { DATA_TEMPLATES }

