
import { openSourceEditPage, initShowOnlyCurrentUserButton } from './redesign_citations_UI-handlers.js';

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
