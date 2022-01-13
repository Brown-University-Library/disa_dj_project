import * as sr from './browse_tabulator_constants.js';

/*

  This module is responsible for accessing the Wordpress API
  and returning the complete list of resources

*/

// Given a resource, get the URL of the featured image

async function getFeaturedImageUrl(resource) {

  let featuredMediaUrl;

  if (resource.featured_media) {

    const featuredMediaInfoUrl = resource._links['wp:featuredmedia'][0].href,
          featuredMediaInfoResponse = await fetch(featuredMediaInfoUrl);

    if (featuredMediaInfoResponse.ok) {
      const featuredMediaInfoJson = await featuredMediaInfoResponse.json();
      featuredMediaUrl = featuredMediaInfoJson.media_details.sizes.thumbnail.source_url;
    } else {
      featuredMediaUrl = null;
    }
  } else {
    featuredMediaUrl = null;
  }

  return featuredMediaUrl;
}


// Get resources from WordPress API

let dcfResourceData;

const response = await fetch(sr.WP_API_BASE);

if (response.ok) {
  dcfResourceData = (await response.json()).map(resource => { 
    return { 
      title: resource.title.rendered,  
      text: resource.excerpt.rendered, 
      // image: getFeaturedImageUrl(resource),
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
