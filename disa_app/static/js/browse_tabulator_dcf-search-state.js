
  // @todo - need to initialize searchState object to respond to table
  /*
    Basically a proxy for getting filter values from the Tabulator table.
    Caches the results for efficiency (call refreshFilterValues() to update cache)
    @todo - search the text of the displayed table to look for keywords in results.
  */

function getSearchStateObject(table, generalSearch) {

  let filterValues;

  function refreshFilterValues() {
    filterValues = table.getFilterValues();
  }

  refreshFilterValues();

  // @TODO need to also check general search box to make sure it's empty

  function isInitial() {
    console.log('IS INITIAL', table.getFilterValues(), Object.keys(table.getFilterValues()).length === 0 && generalSearch.input.trim() === '');
    return (Object.keys(table.getFilterValues()).length === 0 && generalSearch.input.trim() === '')
  }

  return {
    refreshFilterValues,
    isInitial,
    getFilterValue(fieldId) {
      if (fieldId === 'general-search') {
        return generalSearch.input.trim() || '';
      } else {
        return filterValues[fieldId] || ''
      }
    }
  };
}

export { getSearchStateObject }

