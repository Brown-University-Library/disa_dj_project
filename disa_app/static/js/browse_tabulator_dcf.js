
import dcfConfig from './browse_tabulator_dcf-config.js';
import { getDcfResources } from './browse_tabulator_dcf-resources.js';

const testFunctionFactories = {

  init: (searchState) => {
    return () => searchState.isInitial()
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
    // return () => matchRegEx.test(searchState.getFilterValue(fieldId));
    return () => {
      console.log('REGEX TEST', 
                  { searchState, fieldId, value, matchRegEx, 
                    matchAgainst: searchState.getFilterValue(fieldId),
                    result: matchRegEx.test(searchState.getFilterValue(fieldId))
                  });
      return matchRegEx.test(searchState.getFilterValue(fieldId))
    };
  },

  equals: (searchState, {fieldId, value}) => {
    return () => {
      console.log('EQUALITY TEST', { 
        searchState, fieldId, value, 
        matchAgainst: searchState.getFilterValue(fieldId),
        result: searchState.getFilterValue(fieldId) === value
      });
      return searchState.getFilterValue(fieldId) === value
    };
  },

  isNotEmpty: (searchState, {fieldId}) => {
    return () => {
      console.log('NOT_EMPTY TEST', { 
        searchState, fieldId,
        fieldValue: searchState.getFilterValue(fieldId),
        result: searchState.getFilterValue(fieldId).trim() !== ''
      });
      return searchState.getFilterValue(fieldId).trim() !== ''
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

// Given a selector, returns an array of resource display HTML

const dcfResourceTemplate = document.getElementById('dcf-resource-template');
window.temp = dcfResourceTemplate;


// Proposed version uses <template> element instead of JS templating
// See https://johnpapa.net/render-html-2/#renderingheroeswithtemplates
function getResourceDisplayHtml_PROPOSED(resourceSelector) {
  const dcfResources = getDcfResources(resourceSelector);
  return dcfResources.map(resource => {
    const resourceCard = document.importNode(dcfResourceTemplate.content, true);
    resourceCard.querySelector('.dcf-resource-text').textContent = resource.text;
    resourceCard.querySelector('.dcf-resource-link').href = resource.url;
  });
}

// Given an array of resources (compiled from WP-API),
//  return array of HTML snippets for display

function getResourceDisplayHtml(resource) {
  console.log('GENRATING HTML FROM: ', resource);
  return `
    <div class="dcf-resource card bg-light mb-3">\
      <div class="card-header">
        ${resource.title}
        <a class="dcf-resource-link card-link stretched-link" 
           href="${resource.url}" target="_BLANK"
           style="font-weight: bold; font-size: 80%"
           title="Link to more information about ${resource.title}">More</a>
      </div>
      <div class="card-body">
        ${resource.text}
      </div>
    </div>
  `;
}

// Given the searchState object & the available resources (in WP), 
//  return a function that can be called to refresh
//  the Decolonizing Framework sidebar

function getDcfUpdateHandler(searchState, dcfContentElem) {

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
      console.log('YES', {resourcesDisplayHtml, uniqueResourcesDisplayHtml})
      return uniqueResourcesDisplayHtml.join('');
    };

    return function () {
      dcfContentElem.innerHTML = getAllDcfDisplayHtml()
    }
  } catch (err) {
    throw new Error('Error while initializing DeColonizing Frame');
  }
}

// @todo for testing only
window.testFunctionFactories = testFunctionFactories;
window.getTestFunction = getTestFunction;

export { getDcfUpdateHandler }
