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

import * as dataSource from ajaxURL;

const ITEMS_PER_PAGE = 10;

const UNFREE_STATUS_FACETS = [
    "Enslaved Person",
    "Slave",
    "Servant",
    "Indentured Servant",
    "Captive",
  ],
  ALL_STATUS_FACETS = [],
  ENSLAVER_STATUS_FACETS = ["free person ▸ enslaver or owner", "Free > Enslaver"];

function setFacetSet(facetValuesToBeChecked, facetContainerClassname) {
  const facetContainer = document
    .getElementsByClassName(facetContainerClassname)
    .item(0);

  const checkboxesValues = Array.from(
    facetContainer.querySelectorAll("input")
  ).map((x) => x.value);

  checkboxesValues.forEach((checkboxValue) => {
    const checkbox = facetContainer.querySelector(
      `input[value="${checkboxValue}"]`
    );
    const isChecked = checkbox.checked,
      shouldBeChecked = facetValuesToBeChecked.includes(checkbox.value);
    if (isChecked !== shouldBeChecked) {
      checkbox.click();
    }
  });
}

async function main() {
  const searchEngine = await dataSource.getSearch();

  console.log("SR Data API object", searchEngine);

  // Initialize Vue object

  let vm = new Vue({
    el: "#el",
    data: function () {
      // making it more generic
      let filters = {};
      Object.keys(searchEngine.definitions.filters).map(
        (v) => (filters[v] = [])
      );

      return {
        query: "",
        // initializing filters with empty arrays
        filters: filters,
        selected_filters: [],
        sort_keys: Object.keys(searchEngine.definitions.sortings),
        sort: "",
        per_page: ITEMS_PER_PAGE,
      };
    },
    methods: {
      remove_filter: function (facet, name) {
        this.filters[facet] = this.filters[facet].filter((v) => v !== name);
      },

      reset: function () {
        let filters = {};
        Object.keys(searchEngine.definitions.filters).map(
          (v) => (filters[v] = [])
        );

        this.filters = filters;
        this.query = "";
      },

      setEnslavedFacets: function () {
        setFacetSet(UNFREE_STATUS_FACETS, "sr-facet-statuses");
      },

      setEnslaverFacets: function () {
        setFacetSet(ENSLAVER_STATUS_FACETS, "sr-facet-statuses");
      },

      unsetStatusFacet: function () {
        setFacetSet(ALL_STATUS_FACETS, "sr-facet-statuses");
      },

      setEnslavedFacets_OLD: function () {
        const statusFacetContainer = document
          .getElementsByClassName("sr-facet-statuses")
          .item(0);

        const statusCheckboxesValues = Array.from(
          statusFacetContainer.querySelectorAll("input")
        ).map((x) => x.value);

        statusCheckboxesValues.forEach((statusCheckboxValue) => {
          const statusCheckbox = statusFacetContainer.querySelector(
            `input[value="${statusCheckboxValue}"]`
          );
          const isChecked = statusCheckbox.checked,
            shouldBeChecked = UNFREE_STATUS_FACETS.includes(
              statusCheckbox.value
            );
          if (isChecked !== shouldBeChecked) {
            statusCheckbox.click();
          }
        });
      },
    },
    computed: {
      searchResult: function () {
        const result = searchEngine.search({
          query: this.query,
          filters: this.filters,
          per_page: this.per_page,
          sort: this.sort,
        });

        // creating selected filters flat array
        this.selected_filters = [];
        for (const [key, value] of Object.entries(this.filters)) {
          for (const name in value) {
            this.selected_filters.push({
              name: value[name],
              facet: key,
            });
          }
        }

        return result;
      },
    },
  });
}

main();
