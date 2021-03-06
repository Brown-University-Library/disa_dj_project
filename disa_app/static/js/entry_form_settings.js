
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
        1: 'Unspecified',
        2: 'American (U.S.)',
        3: 'British',
        4: 'Dutch',
        5: 'French',
        6: 'Portuguese',
        7: 'Spanish',
        8: 'Other'
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
        'item-type-1':'Birth',
        'item-type-2':'Correspondence',
        'item-type-3':'Court',
        'item-type-4':'Death',
        'item-type-5':'Governmental',
        'item-type-6':'Indenture',
        'item-type-7':'Legal',
        'item-type-8':'Minutes',
        'item-type-9':'Petition',
        'item-type-10':'Purchase',
        'item-type-11':'Other',
        'item-type-12':'Runaway',
        'item-type-13':'Sale',
      },
      formInputDISAPersonStatus: {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four'
      }	
    }
  };
  