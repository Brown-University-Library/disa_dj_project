
// Constants for the Tabulator-based Experimental search page  

export const 

  // Biographical narrative constants

  BIO_NAME_DISPLAY_OVERRIDES = {
    'unrecorded': 'No name is recorded ',
    'Unknown': 'No name is known '
  },
  BIO_SEX_DISPLAY_TERMS = {
    'child': {
      'Female' : 'girl',
      'Male': 'boy',
      'Other': 'child',
      '': 'child'
    },
    'adult': {
      'Female': 'woman',
      'Male': 'man',
      'Other': 'individual',
      '': 'individual'
    },
    'pronoun': {
      'Female': { cap: 'She', nocap: 'she', be_conj: 'was'},
      'Male': { cap: 'He', nocap: 'he', be_conj: 'was'},
      'Other': { cap: 'They', nocap: 'they', be_conj: 'were'},
      '': { cap: 'They', nocap: 'they', be_conj: 'were'}
    }
  },
  BIO_THEME_CLASSNAME = 'biographical',
  BIO_VIEW_SELECTOR_ID = 'biographical-view-option',

  NO_RESULTS_MESSAGE = 'No records match these criteria<br />Try removing filters to broaden your search',
  TABULATOR_CONTAINER_ID = 'data-display',
  VIEW_OPTIONS_RADIO_BUTTONS_ID = 'view-options',
  DOWNLOAD_BUTTON_ID = 'download-data',
  GENERAL_SEARCH_INPUT_ID = 'general-search',
  MIN_TIME_BETWEEN_LUNR_INDEXES = 1000,
  ADULT_CHILD_CUTOFF_AGE = 16,
  ENSLAVED_STATUSES = [
    "Freed", "Captive", "Captive to be sold", "Enslaved", 
    "Formerly Enslaved", "Indenture, Court-Ordered", "Indenture, Parental",
    "Indenture, Voluntary", "Indentured Servant",  "Maidservant",
    "Manservant", "Manslave", "Paid for", "Possible servant or slave",
    "Prisoner", "Prospective Enslavement", "Runaway", "Servant",
    "Slave", "Slave, Court-Ordered", "Threatened Enslavement",
    "Woman Servant", "Unlawfully Detained"
  ],
  ENSLAVED_ROLES = [
    'Enslaved',
    'Bought',
    'Sold',
    'Shipped',
    'Arrived',
    'Escaped',
    'Captured',
    'Emancipated'
  ],
  ENSLAVER_STATUSES = [
    "Owner", "captor", "Enslaver", "Master", "propery owner"
  ],
  ENSLAVER_ROLES = [
    'Owner', 'Captor', 'Buyer', 'Seller', 'Master'
  ],
  ENSLAVEMENT_STATUS = {
    ENSLAVED: 'Enslaved',
    ENSLAVER: 'Enslaver',
    DEFAULT: 'Other or unknown'
  },
  MAX_NUMBER_OF_ENTRIES = 100000,
  REF_COUNT_ELEM_ID = 'ref-count',
  ITEM_COUNT_ELEM_ID = 'item-count',
  CF_CONTENT_ID = 'dcf-content',
  WP_API_BASE = 'https://api-test.cody.digitalscholarship.brown.edu/blog/wp-json/wp/v2/posts?category=context';
