
import { openSourceEditPage, initShowOnlyCurrentUserButton } from './redesign_citations_UI-handlers.js';

const CACHE_EXPIRY_DAYS = 1,
      CACHE_EXPIRY_MS = CACHE_EXPIRY_DAYS * 86400000;

const DATA_CACHE_ID = 'sr-data-cache',
      DATA_TIME_ID = 'sr-data-cache-timestamp';

function fetchDataAndSetCache(url, resolve, reject) {
  fetch(url)
  .then(response => response.json())
  .then(data => {
    localStorage.setItem(DATA_CACHE_ID, JSON.stringify(data));
    localStorage.setItem(DATA_TIME_ID, (new Date()).valueOf())
    resolve(data);
  })
  .catch(error => reject(error));
}

// Overrides Tabulator's built-in Request routine
//  (implements a simple cache using localStorage)

function ajaxRequestFunc(url) {

  return new Promise(function(resolve, reject) {

    // Check if data already cached

    const dataCache = localStorage.getItem(DATA_CACHE_ID),
          dataCacheTimestamp_stored = localStorage.getItem(DATA_TIME_ID),
          dataCacheTimestamp = Number.parseInt(dataCacheTimestamp_stored),
          now = (new Date()).valueOf();

    const haveCachedData = (dataCache !== null),
          cacheIsFresh = (Number.isInteger(dataCacheTimestamp) && (now - dataCacheTimestamp < CACHE_EXPIRY_MS));

    console.log('DATE', {dataCacheTimestamp, now, CACHE_EXPIRY_MS, interval: now - dataCacheTimestamp, cacheIsFresh})

    if (haveCachedData && cacheIsFresh) {
      console.log("Pulling from cached data");
      const data = JSON.parse(dataCache);
      resolve(data);
    // } else if (haveCachedData && !cacheIsFresh) { 
    // TODO if cached data exists, but it's old, then give Tabulator the old data
    //   but fetch the new data and refresh Tabulator when the new data arrives
    } else {
      console.log("Loading data & initializing cache");
      fetchDataAndSetCache(url, resolve, reject);
    }
  });
};


// Main Tabulator setup

function initializeTabulator(tableSelector, ajaxURL) {

  // Formatter for incoming JSON

  const ajaxResponse = function(url, params, response) {

      window.sr.userEmail = (response.user_documents.length) ?
          response.user_documents[0].email :
          undefined;

      const rows = response.documents.map(docData => {
          return {
              title: docData.doc.display,
              id: docData.doc.id,
              date: docData.date.dt_date,
              editor: docData.email
          }
      });

      return rows;
  }

  const titleColumnFormatter = function(cell, formatterParams, onRendered) {
      const recordId = cell._cell.row.data.id;
      return `
      <a href="./${recordId}">${cell.getValue()}</a>
      <button type="button" class="btn btn-outline-danger btn-sm float-end delete-source"
              data-delete-url="${window.sr.api_url_root}documents/${recordId}"
              data-bs-toggle="modal" data-bs-target="#delete-source-modal"
              onclick="window.sr.setModalDeleteUrl('${window.sr.api_url_root}documents/${recordId}')">
        delete
      </button>`;
  }

  const columns = [
      { title: 'Title', field: 'title', formatter: titleColumnFormatter },
      { title: 'ID', field: 'id' },
      {
          title: 'Source created',
          field: 'date',
          formatter: 'datetime',
          formatterParams: {
              inputFormat: "iso",
              outputFormat: "DDD",
              invalidPlaceholder: true,
          },
          headerSort: true,
          sorter: 'date',
          sorterParams: {
              format: 'iso',
              alignEmptyValues: 'top',
          }
      },
      { title: 'Editor', field: 'editor' }
  ];

  // Row click handler: go to Source edit page (unless user
  //  was clicking the 'delete' button)

  const rowClick = function(e, row) {
      const isFromDeleteButton = e.target.classList.contains('delete-source');
      if (!isFromDeleteButton) {
          openSourceEditPage(row._row.data.id);
      }
  };

  const tabulatorSettings = {
      ajaxURL,
      ajaxRequestFunc,
      ajaxResponse,
      columns,
      //dataProcessed: initTableFilterFields,
      pagination: true,
      paginationSize: 20,
      paginationSizeSelector: [20, 50, 100],
  };


  const table = new Tabulator(tableSelector, tabulatorSettings);
  table.on("dataProcessed", initTableFilterFields);

  return table;
}

// Initialize onChange handlers for filters

function initTableFilterFields() {

  const table = this,
      [titleFilterElem, idFilterElem, editorFilterElem] = ['title-filter', 'id-filter', 'editor-filter'].map(
          id => document.getElementById(id)
      );

  function setAllFilters() {
      table.setFilter([
          { field: 'title', type: 'like', value: titleFilterElem.value },
          { field: 'id', type: 'like', value: idFilterElem.value },
          { field: 'editor', type: 'like', value: editorFilterElem.value },
      ]);
  }

  [titleFilterElem, idFilterElem, editorFilterElem].forEach(
      filterElem => filterElem.oninput = setAllFilters
  );

  initShowOnlyCurrentUserButton(table, editorFilterElem);
}

export { initializeTabulator };
