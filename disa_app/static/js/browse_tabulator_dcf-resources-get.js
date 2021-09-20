import * as sr from './browse_tabulator_constants.js';

// Get resources from WordPress API

let dcfResourceData;

const response = await fetch(sr.WP_API_BASE);

if (response.ok) {
  dcfResourceData = (await response.json()).map(resource => { 
    return { 
      title: resource.title.rendered,  
      text: resource.excerpt.rendered, 
      url: resource.link,
      id: resource.id,
      tags: resource.tags,
      categories: resource.categories 
    } 
  });
} else {
  dcfResourceData = [];
} // @todo add better error handling

export default await dcfResourceData;

/*

const colors = fetch('../data/colors.json')
	.then(response => response.json());

export default await colors;

*/