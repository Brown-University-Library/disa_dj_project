
// Constants for the Tabulator-based Experimental search page  

export const 
  NAME_DISPLAY_OVERRIDES = {
    'unrecorded': 'No name is recorded ',
    'Unknown': 'No name is known '
  },
  BIO_THEME_CLASSNAME = 'biographical',
  VIEW_OPTIONS_RADIO_BUTTONS_ID = 'view-options',
  MIN_TIME_BETWEEN_LUNR_INDEXES = 1000,
  ADULT_CHILD_CUTOFF_AGE = 16,
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
  ENSLAVER_ROLES = [
    'Owner',
    'Captor',
    'Buyer',
    'Seller',
    'Master'
  ],
  ENSLAVEMENT_STATUS = {
    ENSLAVED: 'Enslaved',
    ENSLAVER: 'Enslaver',
    DEFAULT: 'Neither or unknown'
  },
  MAX_NUMBER_OF_ENTRIES = 100000,
  REF_COUNT_ELEM_ID = 'ref-count',
  ITEM_COUNT_ELEM_ID = 'item-count';
