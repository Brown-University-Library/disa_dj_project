
// Constants for the Tabulator-based Experimental search page  

export const 
  NAME_DISPLAY_OVERRIDES = {
    'unrecorded': 'No name is recorded ',
    'Unknown': 'No name is known '
  },
  NO_RESULTS_MESSAGE = 'No records match these criteria<br />Try removing filters to broaden your search',
  BIO_THEME_CLASSNAME = 'biographical',
  TABULATOR_CONTAINER_ID = 'data-display',
  VIEW_OPTIONS_RADIO_BUTTONS_ID = 'view-options',
  BIO_VIEW_SELECTOR_ID = 'biographical-view-option',
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
  RACIAL_DESIGNATION = {
    "part african and part indian":[
      "Multi-racial",
      "Black",
      "Indian"
    ],
    "carolina indian":[
      "Indian"
    ],
    "creole":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "criollo":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "east india negro":[
      "Black"
    ],
    "half indian":[
      "Multi-racial",
      "Indian"
    ],
    "indian":[
      "Indian"
    ],
    "indian mulatto":[
      "Multi-racial",
      "Indian",
      "Black"
    ],
    "indio":[
      "Indian"
    ],
    "martha's vineyard indian":[
      "Indian"
    ],
    "mestiza":[
      "Multi-racial",
      "Indian",
      "White"
    ],
    "mestizo":[
      "Multi-racial",
      "Indian",
      "White"
    ],
    "mulatto":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "mustee":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "sambo":[
      "Black"
    ],
    "spanish indian":[
      "Multi-racial",
      "White",
      "Indian"
    ],
    "surinam indian":[
      "Indian"    
    ],
    "surrinam indian":[
      "Indian"
    ],
    "west india mulatto":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "white":[
      "White"
    ],
    "unknown":[
      "Not specified"
    ],
    "unspecified":[
      "Not specified"
    ],
    "negro":[
      "Black"
    ],
    "black":[
      "Black"
    ],
    "white indian":[
      "Multi-racial",
      "White",
      "Indian"
    ],
    "negro-indian":[
      "Multi-racial",
      "Black",
      "Indian"
    ],
    "half negro":[
      "Multi-racial",
      "Black"
    ],
    "mulatta":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "mixed race":[
      "Multi-racial"
    ],
    "white mother":[
      "Multi-racial",
      "White"
    ],
    "east-indian":[
      
    ],
    "east-india indian":[
      
    ],
    "dark mulatto":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "\"looks much like an indian\"":[
      "Indian"
    ],
    "\"resembles an indian in colour\"":[
      "Indian"
    ],
    "\"he resembles an indian, as his father was one\"":[
      "Indian"
    ],
    "mulattoe":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "\"has an indian look\"":[
      "Indian"
    ],
    "\"half indian and half irish\"":[
      "Multi-racial",
      "Indian",
      "White"
    ],
    "\"half indian (his father being an indian and his mother a white woman)\"":[
      "Multi-racial",
      "Indian",
      "White"
    ],
    "\"of dark complection\"":[
      "Not specified"
    ],
    "molattoe":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "\"of a negroe father, and an indian mother\"":[
      "Multi-racial",
      "Black",
      "Indian"
    ],
    "molatto":[
      "Multi-racial",
      "Black",
      "White"
    ],
    "mustizo":[
      "Multi-racial"
    ],
    "asiatic indian":[
      
    ],
    "\"some what the color of an indian\"":[
      "Indian"
    ],
    "mulatto indian":[
      "Multi-racial",
      "Indian"
    ],
    "dark melattress or light griffon":[
      "Multi-racial",
      "Black"
    ],
    "indi":[
      "Indian"
    ],
    "unclear":[
      "Not specified"
    ],
    "indian wench":[
      "Indian"
    ],
    "multi-racial":[
      "Multi-racial"
    ],
    "not specified":[
      "Not specified"
    ]
  },
  MAX_NUMBER_OF_ENTRIES = 100000,
  REF_COUNT_ELEM_ID = 'ref-count',
  ITEM_COUNT_ELEM_ID = 'item-count',
  CF_CONTENT_ID = 'dcf-content',
  WP_API_BASE = 'https://api-test.cody.digitalscholarship.brown.edu/blog/wp-json/wp/v2/posts?category=context';
