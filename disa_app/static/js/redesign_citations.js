
// Global SR object

window.sr = {};

// sr.setModalDeleteUrl called by (x)delete buttons

const deleteSourceConfirmButton = document.getElementById('delete-source-confirm');
window.sr.setModalDeleteUrl = function(url) {
    deleteSourceConfirmButton.dataset.deleteUrl = url;
}

// Create a new Source on server

async function createNewSource() {

    const url = "{{ API_URL_ROOT }}documents/",
        TOKEN = '{{ csrf_token }}',
        requestBody = {
            'acknowledgements': '',
            'citation_type_id': 20, // means the fields below will be 'Book' fields
            'comments': '',
            'fields': {
                'ISBN': '',
                'abstractNote': '',
                'accessDate': '',
                'archive': '',
                'archiveLocation': '',
                'author': '',
                'callNumber': '',
                'date': '',
                'edition': '',
                'extra': '',
                'language': '',
                'libraryCatalog': '',
                'numPages': '',
                'numberOfVolumes': '',
                'pages': '',
                'place': '',
                'publisher': '',
                'rights': '',
                'series': '',
                'seriesNumber': '',
                'shortTitle': '',
                'title': '',
                'url': '',
                'volume': ''
            }
        },
        fetchOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': TOKEN
            },
            body: JSON.stringify(requestBody)
        };

    const response = await fetch(url, fetchOptions);

    if (response.ok) {

        const dataJSON = await response.json(),
            sourceIdMatch = dataJSON.redirect.match('/redesign_citations/([^/]+)/');

        if (sourceIdMatch && sourceIdMatch[1]) {
            window.location.href = `${sourceIdMatch[1]}/`;
        } else {
            console.error(`Can't create new source: redirect URL format error`, dataJSON);
        }
    } else {
        console.error("Error on server creating new Source", { fetchOptions, response });
    }
}

async function deleteSource({ target }) {

    const deleteSourceConfirmButton = target;

    console.log('DELETE SOURCE ' + deleteSourceConfirmButton.dataset.deleteUrl, deleteSourceConfirmButton);

    const url = deleteSourceConfirmButton.dataset.deleteUrl,
        TOKEN = '{{ csrf_token }}',
        fetchOptions = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': TOKEN
            }
        };

    console.log('DELETING SOURCE', {
        url,
        fetchOptions
    });

    const response = await fetch(url, fetchOptions);

    if (response.ok) {
        console.log(response);
        location.reload();
    } else {
        console.log('FAILED', response);
        // What?? Error handling
    }
}

// Go to Source's edit form

function openSourceEditPage(sourceId) {
    window.location.href = `./${sourceId}`;
}

// Set up handler for "show details"

function initToggleTableDetailsButton(table) {
    const showDetailsSwitch = document.getElementById('show-details'),
        showOnlyCurrentUserSwitch = document.getElementById('current-user-only');
    showDetailsSwitch.addEventListener('change', function() {
        const colOp = showDetailsSwitch.checked ? 'showColumn' : 'hideColumn';
        table[colOp]('id');
        table[colOp]('date');
        if (!showOnlyCurrentUserSwitch.checked) {
            table[colOp]('editor');
        }
    });
    showDetailsSwitch.dispatchEvent(new Event('change'));
}

// Set up handler for "show current user" --
//  sets "editor" filter field & hides editor column

function initShowOnlyCurrentUserButton(table, editorFilterElem) {
    const userEmail = window.sr.userEmail;
    const showOnlyCurrentUserButton = document.getElementById('current-user-only');
    showOnlyCurrentUserButton.addEventListener('change', function() {
        if (showOnlyCurrentUserButton.checked) {
            editorFilterElem.value = userEmail;
            editorFilterElem.parentNode.hidden = true;
            table.hideColumn('editor');
            editorFilterElem.dispatchEvent(new Event('input'));
        } else {
            editorFilterElem.value = '';
            editorFilterElem.parentNode.hidden = false;
            table.showColumn('editor');
            editorFilterElem.dispatchEvent(new Event('input'));
        }
    });
    showOnlyCurrentUserButton.checked = true;
    showOnlyCurrentUserButton.dispatchEvent(new Event('change'));
}

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
                data-delete-url="{{ API_URL_ROOT }}documents/${recordId}"
                data-bs-toggle="modal" data-bs-target="#delete-source-modal"
                onclick="window.sr.setModalDeleteUrl('{{ API_URL_ROOT }}documents/${recordId}')">
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

// Main: set up handlers for sidebar documentation and "New Source" button

window.addEventListener('DOMContentLoaded', () => {

    // Initialize new-source button

    document.getElementById('createNewSourceButton')
        .addEventListener('click', createNewSource);

    // Initialize confirm button in delete-source modal

    const deleteSourceConfirmButton = document.getElementById('delete-source-confirm');
    deleteSourceConfirmButton.addEventListener('click', deleteSource);

    // Initialize interactive (Tabulator-based) table

    const TABLE_SELECTOR = '#all-sources',
        TABLE_DATA_URL = './?format=json';

    const table = initializeTabulator(TABLE_SELECTOR, TABLE_DATA_URL);
});
