
import dcfConfig from './browse_tabulator_dcf-config.js';
import { getDcfResources } from './browse_tabulator_dcf-resources.js';


// BEGIN NEW FOOTNOTE THINGY

const recordTestFactory = {
  equals: (recordProp, ruleValue) => {
    return (record) => (record[recordProp] === ruleValue);
  },
  matches:  (recordProp, ruleValue) => {
    const matchRegEx = new RegExp(ruleValue);
    return (record) => matchRegEx.test(record[recordProp]);
  }
};


function getRecordTestFunction(cfConfig) {

  // Get all rules that apply to records

  const recordRules = cfConfig.filter(
    rule => rule.searchRule.fieldId && rule.searchRule.fieldId.startsWith('record.')
  );

  // For every rule, return an object with: 
  //  - a function that runs the test on a record and returns a boolean
  //  - the ID of the rule (which forms the footnote reference)

  const tests = recordRules.map(
    rule => {
      const getTest = recordTestFactory[rule.searchRule.ruleType],
            recordPropertyId = rule.searchRule.fieldId.slice(7);
      return {
        func: getTest(recordPropertyId, rule.searchRule.value),
        id: rule.id
      }
    }
  );

  // Return a function that takes a record and returns an
  //  array of IDs of rules that pass

  return record => tests.filter(test => test.func(record)).map(test => test.id);
}


// Get a function that goes through each visible table entry
//  and gets a list of rule IDs that apply, and adds a footnote
//  at the end of the entry for each

function getVisibleRecordsUpdater(table, cfConfig) {
  const getRecordFootnoteIDs = getRecordTestFunction(cfConfig);
  return () => {
    table.getVisibleData().forEach(
      entry => {
        const entryFootnoteElemId = `referent-footnote-id-${entry.referent_db_id}`,
              entryFootnoteElem = document.getElementById(entryFootnoteElemId),
              footnoteHtmlArr = getRecordFootnoteIDs(entry)
                .map((n, i) => `<a class="cf-footnote cf-footnote-${i}">${n}</a>`);

        if (footnoteHtmlArr.length) {
          entryFootnoteElem.innerHTML = 'Notes:&nbsp;' + footnoteHtmlArr.join();
        }
      }
    )
  }
}

// END NEW FOOTNOTE THINGY


const testFunctionFactories = {

  init: (searchState) => {
    // return () => searchState.isInitial()
    return () => { console.log('IS IT INIT?'); searchState.isInitial()}
  },

  and: (searchState, {rules}) => {
    const rulesAsFunctions = rules.map(rule => getTestFunction(searchState, rule));
    return () => rulesAsFunctions.every(f => f());
  },

  or: (searchState, {rules}) => {
    const rulesAsFunctions = rules.map(rule => getTestFunction(searchState, rule));
    return () => rulesAsFunctions.some(f => f());
  },

  matches: (searchState, {fieldId, value}) => {
    const matchRegEx = new RegExp(value);
    return () => {
      console.log('REGEX TEST', 
                  { searchState, fieldId, value, matchRegEx, 
                    matchAgainst: searchState.getFieldValue(fieldId),
                    result: searchState.getFieldValue(fieldId).some(
                      dataValue => matchRegEx.test(dataValue)
                    )
                  });
      return searchState.getFieldValue(fieldId).some(
        dataValue => matchRegEx.test(dataValue)
      );
    };
  },

  equals: (searchState, {fieldId, value}) => {
    return () => {
      console.log('EQUALITY TEST', { 
        searchState, fieldId, value, 
        matchAgainst: searchState.getFieldValue(fieldId),
        result: searchState.getFieldValue(fieldId).some(
          dataValue => dataValue === value
        )
      });
      return searchState.getFieldValue(fieldId).some(
        dataValue => dataValue === value
      );
    };
  },

  isNotEmpty: (searchState, {fieldId}) => {
    return () => {
      console.log('NOT_EMPTY TEST', { 
        searchState, fieldId,
        fieldValue: searchState.getFieldValue(fieldId),
        result: searchState.getFieldValue(fieldId).some(
          dataValue => dataValue !== undefined && dataValue.trim() !== ''
        ) 
      });
      return searchState.getFieldValue(fieldId).some(
        dataValue => dataValue !== undefined && dataValue.trim() !== ''
      );
    };
  }
}

// Given a clause, generate test functions

function getTestFunction(searchState, {ruleType, ...ruleArguments}) {

  try {
    if (testFunctionFactories[ruleType] === undefined) {
      console.error(`'${ruleType}' is not a recognized test type (i.e. and, or, matches, equals -- case matters)`);
      throw('');
    } else {
      return testFunctionFactories[ruleType](searchState, ruleArguments);
    }
  } catch (err) {
    throw new Error('DCF config', { cause: err });
  }
}

// Given a resource, use the <template> element in the HTML file
//  to create snippet of HTML as string

const dcfResourceTemplate = document.getElementById('dcf-resource-template');

function getResourceDisplayHtml(resource) {
  const resourceCard = dcfResourceTemplate.content.cloneNode(true),
        linkToFullResource = resourceCard.querySelector('a.dcf-resource-link');

  // Populate template copy

  // resourceCard.querySelector('span.dcf-number').textContent = resource.id;
  resourceCard.querySelector('span.dcf-resource-title').textContent = resource.title;
  resourceCard.querySelector('span.dcf-resource-text').innerHTML = resource.text;
  linkToFullResource.href = resource.url;
  linkToFullResource.title = `Link to more information about ${resource.title}`;

  // Convert document fragment to HTML string

  const finalHtmlContainer = document.createElement('div');
  finalHtmlContainer.appendChild(resourceCard);
  return finalHtmlContainer.innerHTML.trim();
}

// Given the searchState object & the available resources (in WP), 
//  return a function that can be called to refresh
//  the Decolonizing Framework sidebar

function getDcfUpdateHandler(searchState, dcfContentElem, table) {

  try {

    // With the config array, make an array of functions that each
    // (a) runs the test and (b) returns the HTML snippet if it passes
    // (HTML is generated in advance)

    function getTestAndDisplayFunction({searchRule, resourceSelector}, ruleNumber) {

      const testFunction = getTestFunction(searchState, searchRule),
            resources = getDcfResources(resourceSelector);
            console.log(`START MAPPING FOR RULE #${ruleNumber}`, resources);
            resources.map(r => console.log(`MAPPING FOR RULE #${ruleNumber}`, r));
            const resourceDisplayArr = resources.map(getResourceDisplayHtml);

      console.log(`GOT DISPLAY HTML FOR RULE #${ruleNumber}:`, {searchRule, resourceSelector, resourceDisplayArr});

      return () => {
        console.log(`TESTING RULE #${ruleNumber}`, {resourceSelector, resourceDisplayArr, searchState, searchRule, testFunction});
        console.log(`RESULT: RULE #${ruleNumber} ` + (testFunction() ? 'PASSES' : 'FAILS'));
        return testFunction() ? resourceDisplayArr : []
      };
    }

    const testAndDisplayFunctions = dcfConfig.map(getTestAndDisplayFunction);

    // Generate a function that runs all test/display functions
    //  in the array generated above, then
    //  collects the display HTML (eliminating duplicates)
    //  and returns the compiled HTML

    const getAllDcfDisplayHtml = function () {
      searchState.refreshFilterValues();
      const resourcesDisplayHtml = testAndDisplayFunctions.map(f => f()).flat(),
            uniqueResourcesDisplayHtml = Array.from((new Set(resourcesDisplayHtml)).values());
      return uniqueResourcesDisplayHtml.join('');
    };

    // Updater for table rows -- adds footnotes

    const updateTableRowFootnotes = getVisibleRecordsUpdater(table, dcfConfig);
    
    // Final function: updates all HTML in CF sidebar
    //  and adds footnotes to table rows

    return function () {
      dcfContentElem.innerHTML = getAllDcfDisplayHtml();
      updateTableRowFootnotes();
    }
  } catch (err) {
    throw new Error('Error while initializing DeColonizing Frame');
  }
}

// @todo for testing only
window.testFunctionFactories = testFunctionFactories;
window.getTestFunction = getTestFunction;

export { getDcfUpdateHandler }
