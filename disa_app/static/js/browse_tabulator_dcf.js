
import dcfConfig from './browse_tabulator_dcf-config.js';
import { getDcfResources } from './browse_tabulator_dcf-resources.js';

// Given a clause, generate test functions

const testFunctionFactories = {

  init: () => { // This is probably better tested by seeing if there are any other notes
    return () => false;
    // return data => data.isInitial()
  }, // The rule could always return true -- IF no other rules, THEN init()
     // maybe a better name is 'default'

  matches: ({fieldId, value}) => {
    const matchRegEx = new RegExp(value),
          matchTestFunc = dataValue => matchRegEx.test(dataValue),
          testFunc = data => data.getFieldValue(fieldId).some(matchTestFunc);
    return testFunc;
  },

  equals: ({fieldId, value}) => {
    const equalityTestFunc = dataValue => dataValue === value;
    return data => data.getFieldValue(fieldId).some(equalityTestFunc);
  },

  isNotEmpty: ({fieldId}) => {
    const isNotEmptyTestFunc = dataValue => {
      return dataValue !== undefined && dataValue.trim() !== ''
    }
    return data => data.getFieldValue(fieldId).some(isNotEmptyTestFunc);
  },

  and: ({rules}) => {
    const rulesAsFunctions = rules.map(rule => getTestFunction(rule));
    return data => rulesAsFunctions.every(f => f(data));
  },

  or: ({rules}) => {
    const rulesAsFunctions = rules.map(rule => getTestFunction(rule));
    return data => rulesAsFunctions.some(f => f(data));
  }
}

function getTestFunction({ruleType, ...ruleArguments}) {
  if (testFunctionFactories[ruleType] === undefined) {
    console.error(`'${ruleType}' is not a recognized test type (i.e. ${Object.keys(testFunctionFactories).join(', ')} -- case matters!)`);
  } else {
    return testFunctionFactories[ruleType](ruleArguments);
  }
}

function getFootnoteHtmlElem(resource) {
  const footnoteElem = document.createElement('span');
  footnoteElem.classList.add('cf-footnote', 'badge', 'rounded-pill', 'text-bg-primary');
  footnoteElem.innerText = resource.id;
  footnoteElem.setAttribute('id',resource.id);
  /* footnoteElem.onmouseover = () => {
    //document.getElementById(`dcf-resource-${resource.id}`).classList.add('highlight');
  }
  footnoteElem.onmouseleave = () => {
    //document.getElementById(`dcf-resource-${resource.id}`).classList.remove('highlight');
  }*/
  return footnoteElem;
}

function getDcfUpdateHandler(searchState, dcfContentElem, table) {

  // Map rules array (from config) to an array of objects with
  //  test-functions and resolved resources

  const rules = dcfConfig.map(rule => {

    // Get this rule's corresponding test function
    const testFunction = getTestFunction(rule.searchRule);

    // Create a function for testing an entry
    const entryPassesFunction = entry => {
      return testFunction({
        getFieldValue: (fieldId) => [entry[fieldId.slice(7)]],
        isInitial: () => false // Entries are never init
      })
    };

    // Create a function for testing filter state
    const filterPassesFunction = () => testFunction(searchState);

    // START TEMP
    if (rule.searchRule.ruleType === 'init') {
      /*console.log({
        type: rule.searchRule.ruleType,
        filterPasses: filterPassesFunction,
        entryPasses: entryPassesFunction,
        resources: getDcfResources(rule.resourceSelector),
        resourceSelector: rule.resourceSelector
      });*/
    } // END TEMP
    return {
      type: rule.searchRule.ruleType,
      filterPasses: filterPassesFunction,
      entryPasses: entryPassesFunction,
      resources: getDcfResources(rule.resourceSelector)
    }
  });

  // Pull out the default rule (only the first is used)

  const defaultRule = rules.find(rule => rule.type === 'init');

  // Define a function to deduplicate an array
  //  (used below)

  const filterForUniques = (resource, index, resources) => {
    return resources.findIndex(r => r.id === resource.id) === index
  }
  
  window.srGetTestFunction = getTestFunction;
  window.srRules = rules;

  // Final function: run test functions against filters and records and
  //  update the display accordingly

  return function () {

    // Generate the footnotes in the table

    // For each results entry in the table 
    //  (1) run the tests and get a list of rules that apply
    //  (2) extract the resources into a list
    //  (3) deduplicate the list
    //  (4) convert the list to HTML strings and join

    table.getVisibleData().forEach(entry => {
      const entryFootnoteElemId = `referent-footnote-id-${entry.referent_db_id}`,
            entryFootnoteContainerElem = document.getElementById(entryFootnoteElemId);

      if (entryFootnoteContainerElem.innerHTML.trim() === '') {
        rules.filter(rule => rule.entryPasses(entry)) // 1
            .reduce((resources, rule) => resources.concat(rule.resources), []) // 2
            .filter(filterForUniques) // 3
            .map(r => { //console.log('!!', r);
              return r })
            .map(resource => getFootnoteHtmlElem(resource)) // 4
            .forEach(
              entryFootnoteElem => entryFootnoteContainerElem.appendChild(entryFootnoteElem)
            );
      }
    });

    // Generate the sidebar content

    // For each rule, 
    //  (1) run the tests against the filter state
    //  (2) get a list of resources
    //  (3) deduplicate it
    //  (4) convert to HTML and join
    // (If no rules pass, then use the default rule)

    searchState.refreshFilterValues();

    const cfRulesThatPass = rules.filter(rule => rule.filterPasses()), // (1)
          cfRules = cfRulesThatPass.length ? cfRulesThatPass : [defaultRule];

    const cfHTML = cfRules.reduce((resources, rule) => resources.concat(rule.resources), []) // (2)
        .filter(filterForUniques) // (3)
        .map(resource => resource.cfHtml) // (4)
        .join();

    dcfContentElem.innerHTML = cfHTML;
  }

  // Get a map of resources to rules

}

// @todo for testing only
window.srTestFunctionFactories = testFunctionFactories;

export { getDcfUpdateHandler }
