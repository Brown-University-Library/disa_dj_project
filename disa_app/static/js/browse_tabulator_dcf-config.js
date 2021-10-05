

/*

  Essentially a pattern-matching declaration, that looks for a 
  pattern in the search conditions, and if the pattern is fulfilled,
  displays designated resources in the ContextFrame.

  Format:

    [
      { 
        searchRule: <SEARCH-RULE>, 
        resources: <RESOURCES>
      } 
      <... MORE RULES>
    ]

  Search rules are:

    For matching values:

    {
      ruleType: <one of: "matches", "equals">,
      fieldId: <string>,
      value: <string> (if it's a 'matches' rule, then this is a regular expression)
    }

    NOTE: Regular expressions need to do the "double backslash" for symbols, 
          e.g. whitespace = \\s (not \s)

    For "and"/"or":

    {
      ruleType: <either "and" or "or">,
      rules: [<two or more rules>]
    }

    You can defined what is shown in the initial state, before
    the user does anything -- this is done by:

    {
      ruleType: 'init'
    }

    You can also check if a filter is not empty:

    {
      ruleType: 'isNotEmpty',
      fieldId: <string>
    }


  Resources:

    {
      tag: <either a single integer, or an array of integers>,
      category:  <either a single integer, or an array of integers>,
      id:  <either a single integer, or an array of integers>
    }

    These are ORed together -- so the designated tags PLUS the designated categories
    PLUS the IDs. For example, you can't select for an item that has a tag, but 
    only if it's in a category.

  See schema for this data structure at browse_tabulator_dcf-config_schema.js

  You can validate this config by putting the array (i.e. the code between "START/END RULE DATA") 
  and the schema into https://www.jsonschemavalidator.net/

*/



const rules = 

// START RULE DATA

[
    {
      searchRule: {
        ruleType: 'init'
      },
      resourceSelector: {
        tag: 9
      }
    },
    {
      searchRule: {
        ruleType: 'equals',
        fieldId: 'filter.all_tribes',
        value: 'Narragansett'
      },
      resourceSelector: {
        tag: 15
      }
    },
    {
      searchRule: {
        ruleType: 'equals',
        fieldId: 'filter.all_tribes',
        value: 'Eastern Pequot'
      },
      resourceSelector: {
        tag: 14
      }
    },
    {
      searchRule: {
        ruleType: 'isNotEmpty',
        fieldId: 'general-search'
      },
      resourceSelector: {
        tag: 36
      }
    },
    {
      searchRule: {
        ruleType: 'isNotEmpty',
        fieldId: 'filter.all_tribes'
      },
      resourceSelector: {
        tag: 6
      }
    },
    {
      searchRule: {
        ruleType: 'isNotEmpty',
        fieldId: 'filter.sex'
      },
      resourceSelector: {
        tag: 5
      }
    },
    {
      searchRule: {
        ruleType: 'isNotEmpty',
        fieldId: 'filter.all_races'
      },
      resourceSelector: {
        tag: 7
      }
    },
    {
      searchRule: {
        ruleType: 'isNotEmpty',
        fieldId: 'filter.reference_data.all_locations'
      },
      resourceSelector: {
        tag: 8
      }
    },
    {
      searchRule: {
        ruleType: 'matches',
        fieldId: 'record.name_first',
        value: '^Eliz'
      },
      resourceSelector: {
        id: 88
      }
    },
    {
      searchRule: {
        ruleType: 'and',
        rules: [
          {
            ruleType: 'equals',
            fieldId: 'record.sex',
            value: '^Eliz'
          },
          {
            ruleType: 'matches',
            fieldId: 'record.name_last',
            value: '^Smi'
          }
        ]
      },
      resourceSelector: {
        id: 88
      }
    }
  ];

// END RULE DATA

// Add IDs to rules

const rulesWithIDs = rules.map(
  (rule, index) => Object.assign({}, rule, { id: index })
);

export default Object.freeze(rulesWithIDs);
