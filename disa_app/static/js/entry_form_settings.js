
export const LOCAL_SETTINGS = {

  AGE_BY_NUMBER_CHECKBOX_ID: "formInputSpecifiedByNumber",
  AGE_BY_NUMBER_DISPLAY_CSS_CLASS: "age-as-number",
  DOC_TYPE_ELEM_ID: "document_type",

  // API endpoints -- NOT BEING USED

  API_ENDPOINT_URL: {},

  // Data structure for showing / hiding citation fields

  FIELDS_BY_DOC_TYPE: {
    // Book
    20: {
      required: ["author", "date", "pages", "place", "publisher", "title"],
      optional: [
        "abstractNote",
        "edition",
        "language",
        "publisher",
        "series",
        "seriesNumber",
        "shortTitle",
        "url",
      ],
    },
    // Book Section
    21: {
      required: ["author", "date", "pages", "place", "publisher", "title"],
      optional: [
        "abstractNote",
        "edition",
        "language",
        "section",
        "series",
        "seriesNumber",
        "shortTitle",
        "url",
      ],
    },
    // Document
    26: {
      required: ["author", "date", "pages", "place", "title"],
      optional: ["abstractNote", "archive", "archiveLocation", "language", "publisher", "url"],
    },
    // Interview
    33: {
      required: ["author", "date", "place", "rights", "title"],
      optional: ["abstractNote", "archive", "archiveLocation", "language", "publisher", "url"],
    },
    // Journal Article
    34: {
      required: ["author", "date", "pages", "publisher", "title"],
      optional: ["abstractNote", "language", "url"],
    },
    // Magazine Article
    36: {
      required: ["author", "date", "pages", "publisher", "title"],
      optional: ["abstractNote", "language", "url"],
    },
    // Manuscript
    37: {
      required: [
        "archive",
        "archiveLocation",
        "author",
        "date",
        "pages",
        "title",
      ],
      optional: ["abstractNote", "language", "place", "publisher", "url"],
    },
    // Newspaper Article
    39: {
      required: ["date", "edition", "place", "title"],
      optional: [
        "abstractNote",
        "archive",
        "archiveLocation",
        "author",
        "language",
        "publisher",
        "pages",
        "section",
        "url",
      ],
    },
    // Thesis
    46: {
      required: ["author", "date", "rights", "title"],
      optional: ["abstractNote", "archive", "archiveLocation", "language", "url"],
    },
    // Webpage
    49: {
      required: ["accessDate", "date", "title", "url"],
      optional: ["author", "language"],
    }
  },

  // Save status codes

  SAVE_STATUS: {
    NO_CHANGE: 1, 
    SAVE_IN_PROGRESS: 2, 
    ERROR_BAD_API_ID: 3, 
    SUCCESS: 4
  },

  // What goes in the menus? (can be controlled from server)
  // (note: keys are same as element IDs)

  MENU_OPTIONS: {
    document_type: {
      '-1':'Unspecified / not clear',
      '20':'Book',
      '21':'Book Section',
      '26':'Document',
      '33':'Interview',
      '34':'Journal Article',
      '36':'Magazine Article',
      '37':'Manuscript',
      '39':'Newspaper Article',
      '46':'Thesis',
      '49':'Webpage'
    },
    formInputDISAPersonTribe: { 
      
      // With labels/values as ID ... (weird)

      'Bocotora':'Bocotora',
      'Eastern Pequot':'Eastern Pequot',
      'Mashantucket Pequot':'Mashantucket Pequot',
      'Mohegan':'Mohegan',
      'Naragansett':'Naragansett',
      'Pequot':'Pequot',
      'Wampanoag':'Wampanoag',
      'Woolwa':'Woolwa',
      'Unspecified / not clear':'Unspecified / not clear'
      
      /* WITH DB IDs AS KEYS ... (logical)

      '25':'Unspecified / not clear',
      '2':'Bocotora',
      '4':'Eastern Pequot',
      '5':'Mashantucket Pequot',
      '6':'Mohegan',
      '7':'Naragansett',
      '10':'Pequot',
      '20':'Wampanoag',
      '21':'Woolwa' */
    },
    formInputDISAPersonVocation: {
      '0': 'Not specified',
      '1': 'Baker',
      '2': 'Cordwainer',
      '3': 'Farmer',
      '4': 'Lawyer',
      '5': 'Leatherer',
      '6': 'Malster',
      '7': 'Mariner',
      '8': 'Merchant',
      '9': 'Sadler',
      '10': 'Ship Captain',
      '11': 'Shopkeeper'
    },
    formInputDISAPersonStatus: {
      'status0':'None specified',
      'status1':'Free',
      'status2':'Indentured Servant, Court-Ordered',
      'status3':'Indentured Servant, General',
      'status4':'Indentured Servant, Parental',
      'status5':'Indentured Servant, Voluntary',
      'status6':'Servant',
      'status7':'Slave',
      'status8':'Unclear',
      'status9':'Other'
    },
    formInputDISAPersonGender: {
      '0': 'Not specified',
      'Male': 'Male',
      'Female': 'Female',
      'Two spirit': 'Two spirit'
    },
    formInputDISAColonialContext: {

      '1':	'British',
      '2':	'American',
      '3':	'French',
      '4':	'Spanish',
      '5':	'Other'
/*
      1: 'Unspecified',
      2: 'American (U.S.)',
      3: 'British',
      4: 'Dutch',
      5: 'French',
      6: 'Portuguese',
      7: 'Spanish',
      8: 'Other' */
    },
    formInputDISAItemPersonNameType: {
      '1': 'Alias',
      '2': 'Baptismal',
      '3': 'English',
      '4': 'European',
      '5': 'Indian',
      '6': 'Nickname',
      '7': 'Given',
      '8': 'Unknown'
    },
    formInputDISAPersonRace: {
      'Not specified':'Not specified',
      'Black':'Black',
      'Indian':'Indian',
      'Multi-racial':'Multi-racial',
      'White':'White'
      /*
      '23':'Not specified',
      '30':'Black',
      '7':'Indian',
      '35':'Multi-racial',
      '24':'White' */
    },
    formInputDISAItemType: {	
      '1':'Baptism',
      '2':'Runaway',
      '3':'Sale',
      '4':'Capture',
      '5':'Inoculation',
      '6':'Execution',
      '7':'Manumission',
      '8':'Entry',
      '9':'Indenture',
      '10':'Account',
      '11':'Note',
      '12':'Inventory',
      '13':'Unspecified',
      '14':'Reference',
      '15':'Skating across the pond',
      '16':'Criminal charge',
      '17':'Council Minutes',
      '18':'Advertisement for Sale',
      '19':'Petition',
      '20':'Petition to Assembly',
      '21':'bug test',
      '22':'Arrest Warrant',
      '23':'Account (Letter)',
      '24':'Writ of Indenture',
      '25':'Town Council Records',
      '26':'Power of Attorney',
      '27':'Child Indenture',
      '28':'Deed of Sale',
      '29':'Burial Record',
      '30':'Notice of capture',
      '31':'Record of Death',
      '32':'Enclosure',
      '33':'Complaint',
      '34':'Report',
      '35':'Return',
      '36':'Instrument of sale',
      '37':'Decree',
      '38':'Order',
      '39':'Resolve',
      '40':'Council Order',
      '41':'Council Resolve',
      '42':'Petition Resolve',
      '43':'Manumission Application',
      '44':'Petition and Resolve',
      '45':'Petition and Order',
      '46':'House of Representatives Vote',
      '47':'Council Vote',
      '48':'Court Case',
      '49':'Test',
      '50':'Proclamation',
      '51':'House Resolution',
      '52':'Will',
      '53':'Runaway',
      '54':'Deposition',
      '55':'Affidavit',
      '56':'Criminal case abstract',
      '57':'Court records',
      '58':'Record of sale',
      '59':'Testimony',
      '60':'Diary entry',
      '61':'Letter',
      '62':'Newspaper Article',
      '63':'Journal Entry',
      '64':'Agreement',
      '65':'Correspondence',
      '66':'Presentments',
      '67':'Appraisal',
      '68':'Deed of Gift',
      '69':'Hire of Indian',
      '70':'Memorandum',
      '71':'Attestations',
      '72':'Receipt',
      '73':'Conference',
      '74':'Treaty',
      '75':'Narrative',
      '76':'Memoir',
      '77':'Abstract',
      '78':'Abstract',
      '79':'Notice of Runaway'
    },
    formInputDISAPersonStatus: {
      1: 'one',
      2: 'two',
      3: 'three',
      4: 'four'
    },

    // @todo THESE ARE NOT GOOD - this is only a partial reflection of what's
    //  in the DB (in table 1_roles), but this all needs to be reviewed

    formInputDISARelationship: {
      '1':'enslaved by',
      '2':'owner of',
      '3':'priest for',
      '4':'inoculated by',
      '5':'bought by',
      '6':'sold by',
      '7':'shipped by',
      '8':'delivered by',
      '9':'escaped from',
      '10':'captured',
      '11':'captured by',
      '12':'baptised by',
      '13':'released by',
      '14':'executed by',
      '15':'parent of',
      '16':'spouse of',
      '17':'child of',
      '18':'mother of',
      '19':'father of',
      '20':'buyer of',
      '21':'seller of',
      '22':'indentured by',
      '23':'master of',
      '34':'ran away with',
      '38':'servant of'
    },
    formInputDISAPersonGeoOrigins: {
      // Origins are joined to locations
      // but those are uncontrolled, so there's nothing to
      // suggest here
    }
  }
};
