import dcfResourceData from './browse_tabulator_dcf-resources-get.js';

/*

  This module is responsible for returning resources that match a 
  resource selector (as stored in the browse_tabulator_dcf-config.js)

*/



function filterForUniques(resource, index, resources) {
  return resources.findIndex(r => r.id === resource.id) === index
}

// Given a resource, use the <template> element in the HTML file
//  to create snippet of HTML as string

const dcfResourceTemplate = document.getElementById('dcf-resource-template');

// async function getResourceDisplayHtml(resource) {
function getResourceDisplayHtml(resource) {

  const resourceCard = dcfResourceTemplate.content.cloneNode(true),
        linkToFullResource = resourceCard.querySelector('a.dcf-resource-link'),
        imageUrl = null;
        //imageUrl = await resource.image;

  // Populate template copy

  resourceCard.firstElementChild.id = `dcf-resource-${resource.id}`;
  resourceCard.querySelector('span.dcf-number').textContent = resource.id;
  resourceCard.querySelector('span.dcf-resource-title').textContent = resource.title;
  resourceCard.querySelector('span.dcf-resource-text').innerHTML = resource.text;
  // resourceCard.querySelector('img.dcf-featured-image').src = imageUrl || '';
  linkToFullResource.href = resource.url;
  linkToFullResource.title = `Link to more information about ${resource.title}`;

  // Convert document fragment to HTML string

  const finalHtmlContainer = document.createElement('div');
  finalHtmlContainer.appendChild(resourceCard);
  return finalHtmlContainer.innerHTML.trim();
}

// Given a selector, return all the associated resources

// async function getDcfResources(resourceSelector) {
function getDcfResources(resourceSelector) {

  // Convert selectors into arrays, if they're not already

  const { tag, category, id } = resourceSelector,
        [tagArray, categoryArray, idArray] = [tag, category, id].map(
          x => Array.isArray(x) ? x : [x]
        );

  // Match and collect DCF resources

  let resourceList = [];

  if (id) {
    const matchingResources = idArray.map(
      postId => dcfResourceData.find(r => r.id === postId)
    );
    resourceList = resourceList.concat(matchingResources);
  }

  if (category) {
    const matchingResources = categoryArray.map(
      catId => dcfResourceData.filter(r => r.categories.includes(catId))
    );
    resourceList = resourceList.concat(matchingResources);
  }

  if (tag) {
    const matchingResources = tagArray.map(
      tagId => dcfResourceData.filter(r => r.tags.includes(tagId))
    );
    resourceList = resourceList.concat(matchingResources);
  }

  // Flatten & deduplicate the DCF matching resourceList

  /*
  const uniqueResourceListWithHTML_promises = resourceList.flat(10).filter(filterForUniques).map(async function (resource) {
    const cfHtml = await getResourceDisplayHtml(resource);
    console.log('CATCAT', cfHtml);
    return Object.assign({}, resource, { cfHtml });
  });

  const uniqueResourceListWithHTML = await Promise.all(uniqueResourceListWithHTML_promises);
  */

  // Deduplicate matching resources, then
  //  generate HTML for each resource and add it

  let uniqueResourceListWithHTML = resourceList.flat(10).filter(filterForUniques).map(function (resource) {
    const cfHtml = getResourceDisplayHtml(resource);
    return Object.assign({}, resource, { cfHtml });
  });

  // TEMP WORKAROUND - START
  // The problem is that the init resource is referenced right away, before the
  //  resources are finished loading (yes, this is an async issue)
  // The kludge is to jam in some hand-coded content

  if (tag === 9) {
    uniqueResourceListWithHTML = [{
      "url": "https://www.api-test.cody.digitalscholarship.brown.edu/blog/eastern-pequot/",
      "tags": [
          9
      ],
      "cfHtml": `
        <div class=\"dcf-resource card bg-light mb-3\" id=\"dcf-resource-80\">
          <div class=\"card-header\">
            <!-- <span class=\"dcf-number badge bg-primary text-light\">80</span> -->
            <span class=\"dcf-resource-title\">About the data</span>
              <a class=\"dcf-resource-link card-link stretched-link\" href=\"https://indigenousslavery.org/about/\" target=\"_BLANK\" style=\"font-weight: bold; font-size: 80%\" title=\"Link to more information about Stolen Relations\">&nbsp;</a>\n                    </div>\n                    
              <div class=\"card-body\">\n
              <span class=\"dcf-resource-text\">
              <p>
                [These will be notes about the project that provide a baseline context for the 
                data]
              </p>\n</span>\n                    </div>\n                </div>`
    }]
  }

  // TEMP WORKAROUND - END

  console.log('RESOURCES COLLECTED FOR RULE', uniqueResourceListWithHTML);
  window.ttt = uniqueResourceListWithHTML;
  return uniqueResourceListWithHTML;
}

/* Return structure - array of:

{ 
  text: resource.excerpt.rendered, 
  url: resource.link,
  tags: resource.tags,
  categories: resource.categories 
}

*/

export { getDcfResources }
