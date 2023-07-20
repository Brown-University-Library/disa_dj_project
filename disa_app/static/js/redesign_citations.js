
import {initializeTabulator} from './redesign_citations_tabulator-init.js';

// sr.setModalDeleteUrl called by (x)delete buttons

const deleteSourceConfirmButton = document.getElementById('delete-source-confirm');
window.sr.setModalDeleteUrl = function(url) {
    deleteSourceConfirmButton.dataset.deleteUrl = url;
}

// Create a new Source on server

async function createNewSource() {

    const url = `${window.sr.api_url_root}documents/`,
        TOKEN = window.sr.csrf_token,
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
        TOKEN = window.sr.csrf_token,
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

// Main: set up handlers for sidebar documentation and "New Source" button

function main() {

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
}
console.log('fjsk');
window.addEventListener('DOMContentLoaded', main);
