
// Lunr index function

function getGeneralSearchIndex(data) {

  // Create a list of documents with ID
  //   and text (which combines all the DISA fields to search)

  const docList = data.map(entry => {

    const indexableText = [
      entry.all_name,
      entry.reference_data.all_locations,
      entry.citation_data.display,
      entry.reference_data.transcription,
      entry.enslavement_status
    ].join(' ');

    const indexableText_noHTML = indexableText.replace(/\<[^>]+>/g, '');

    return {
      id: entry.referent_db_id,
      text: indexableText_noHTML
    }
  });

  // Create lunr index from the documents

  const index = lunr( function () {
    this.ref('id');
    this.field('text');

    docList.forEach(function (document) {
      this.add(document)
    }, this);
  });

  return index;
}


function getSearchFunction(sr) {

  const lunrIndex = getGeneralSearchIndex(sr.data);

  return function(searchString) {
    const results = lunrIndex.search(searchString)
                             .map(hit => parseInt(hit.ref));
    return results;
  }
}


function getGeneralSearch(sr) {

  const lunrIndex = getGeneralSearchIndex(sr.data);
  let currentResults;

  const searchFor = function(searchString) {
    currentResults = lunrIndex.search(searchString)
                              .map(hit => parseInt(hit.ref));
    return currentResults;
  }

  searchFor(''); // Initially has full set

  return {
    searchFor,
    currentResults: () => currentResults
  }
}


// Get a function that is called every time a user changes
//  the content of the general search box

function getGeneralSearchFunction_OLD(sr) {

  const lunrIndex = getGeneralSearchIndex(sr.data),
        generalSearchInput = document.getElementById(sr.GENERAL_SEARCH_INPUT_ID);

  let lastSearchTimestamp = 0, 
      timeOutId;

  return function(x) {

    const searchTextChanged = (x !== false); // i.e. if x == false then it indicates a post-change check-in
  
    // If enough time has passed ...
  
    if (Date.now() - lastSearchTimestamp > sr.MIN_TIME_BETWEEN_LUNR_INDEXES) {
  
      // Do a search against index & force Tabulator to reapply filters
  
      const currLunrSelection = lunrIndex.search(generalSearchInput.value).map(hit => parseInt(hit.ref));
      // console.log(`Searching for ${generalSearchInput.value}`, 'Results:', currLunrSelection);
      // sr.table.setFilter(sr.table.getFilters());
  
      // Update times
  
      lastSearchTimestamp = Date.now();
  
      // If this update is because of a change in the
      //   search field, then schedule a future
      //   search to catch any changes
  
      if (searchTextChanged) {
        window.clearTimeout(timeOutId);
        timeOutId = window.setTimeout(
          () => { searchAgainstIndex(false) },
          sr.MIN_TIME_BETWEEN_LUNR_INDEXES + 100
        );
      }

      return currLunrSelection;
    }
  }
}

export { getGeneralSearch };



