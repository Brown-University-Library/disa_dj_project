import dcfResourceData from './browse_tabulator_dcf-resources-get.js';


// Given a selector, return all the associated resources

function getDcfResources(resourceSelector) {

  // Convert selectors into arrays, if they're not already

  const { tag, category, id } = resourceSelector,
        [tagArray, categoryArray, idArray] = [tag, category, id].map(
          x => Array.isArray(x) ? x : [x]
        );

  let resourceList = [];

  // Match and collect resources

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

  return resourceList.flat(10);
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
