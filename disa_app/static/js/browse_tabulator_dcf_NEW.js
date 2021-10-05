
import dcfConfig from './browse_tabulator_dcf-config.js';
import { getDcfResources } from './browse_tabulator_dcf-resources.js';

// Given a clause, generate test functions

const testFunctionFactories = {

  init: () => {
    return data => data.isInitial()
  },

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

// Given a resource, use the <template> element in the HTML file
//  to create snippet of HTML as string

const dcfResourceTemplate = document.getElementById('dcf-resource-template');

function getResourceDisplayHtml(resource) {
  const resourceCard = dcfResourceTemplate.content.cloneNode(true),
        linkToFullResource = resourceCard.querySelector('a.dcf-resource-link');

  // Populate template copy

  resourceCard.querySelector('span.dcf-number').textContent = resource.id;
  resourceCard.querySelector('span.dcf-resource-title').textContent = resource.title;
  resourceCard.querySelector('span.dcf-resource-text').innerHTML = resource.text;
  linkToFullResource.href = resource.url;
  linkToFullResource.title = `Link to more information about ${resource.title}`;

  // Convert document fragment to HTML string

  const finalHtmlContainer = document.createElement('div');
  finalHtmlContainer.appendChild(resourceCard);
  return finalHtmlContainer.innerHTML.trim();
}


function getDcfUpdateHandler(searchState, dcfContentElem, table) {

  // Map rules config array to an array of objects with
  //  test-functions and resolved resources

  const rules = dcfConfig.map(rule => {

    const testFunction = getTestFunction(rule.searchRule),
          entryPassesFunction = entry => {
            testFunction({
              getFieldValue: (fieldId) => [entry[fieldId.slice(7)]],
              isInitial: () => false // Entries are never init
            })
          },
          filterPassesFunction = () => testFunction(searchState);
    
    return {
      filterPasses: filterPassesFunction,
      entryPasses: entryPassesFunction,
      resources: getDcfResources(rule.resourceSelector)
    }
  });

  // Define a function to deduplicate an array
  //  (used below)

  const makeUniqueFilter = (resource, index, resources) => {
    return resources.findIndex(r => r.id === resource.id) === index
  }

  // Final function: run test functions against filters and records and
  //  update the display accordingly

  return function () {

    // For each entry, (1) run the tests and get a list of rules that apply,
    //   (2) extract the resources into a list and (3) deduplicate the list,
    //   (4) convert the list to HTML strings and join

    table.getVisibleData().forEach(entry => {
      const notesHTML = rules.filter(rule => rule.entryPasses(entry)) // 1
        .reduce((resources, rule) => resources.concat(rule.resources), []) // 2
        .filter(makeUniqueFilter) // 3
        // .map(resource => getFootnoteHTML(resource)) // 4
        .map(resource => `<span>FN_${resource.id}</span>`) // 4
        .join();
      // ... and append footnotes to table row
      console.log("NOTES:", notesHTML);
    });

    // For each rule, (1) run the tests against the filter state, 
    //   (2) get a list of resources and (3) deduplicate it,
    //   (4) convert to HTML and join

    rules.filter(rule => rule.filterPasses)
        .reduce((resources, rule) => resources.concat(rule.resources), []) 
        .filter(makeUniqueFilter)
        .map(resource => resource.cfHtml)
        .join();
  }

  // Get a map of resources to rules

}

// @todo for testing only
window.testFunctionFactories = testFunctionFactories;
window.getTestFunction = getTestFunction;

export { getDcfUpdateHandler }
