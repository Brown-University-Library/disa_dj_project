
import { srGlobalObject as sr }     from './browse_tabulator_global-object.js';
import { getShowDetailsFunction }   from './browse_tabulator_details-modal.js';
import { getGeneralSearch }         from './browse_tabulator_lunr.js';
import { getTableRenderer }         from './browse_tabulator_init-table.js';

function main() {

  // MAIN ARCHITECTURAL COMPONENTS

  const showDetailsFunction = getShowDetailsFunction(sr),
        generalSearch = getGeneralSearch(sr),
        table = getTableRenderer(sr, showDetailsFunction, generalSearch),

  // EVENT HANDLERS

  // Get DOM elements

  const bioViewOption = document.getElementById(sr.BIO_VIEW_SELECTOR_ID),
        viewSelector = document.getElementById(sr.VIEW_OPTIONS_RADIO_BUTTONS_ID),
        downloadButton = document.getElementById(sr.DOWNLOAD_BUTTON_ID),
        generalSearchInput = document.getElementById(sr.GENERAL_SEARCH_INPUT_ID);
        tableMode = bioViewOption.classList;

  // Toggle cards vs table
  bioViewOption.addEventListener("click", () => {
    const result = tableMode.toggle("biographical");
  });

  // Handle download button click

  downloadButton.addEventListener('click', table.download);

  // Handle change in general search field

  generalSearchInput.addEventListener('change', () => {
    generalSearch.searchFor(generalSearchInput.value);
    table.refresh();
  });

  // GLOBAL FUNCTIONS - referred to in generated markup

  // Functions called by linked entries in Biographical listing
  // (e.g. click on "Elizabeth" to populate the name field with "Elizabeth")

  window.populateFilter = function(filterId, value) {
    table.setHeaderFilterValue(filterId, value);
  }
  // Show details as a global function
  // (referenced in generated markup)

  window.showDetails = showDetailsFunction;

  // reset filters with button, why is table.clearFilter not a function???

let resetFilters = document.getElementById('reset-filters');
 resetFilters.addEventListener("click", function(){
    table.clearFilter();
  });

}


main();
















/* DATA STRUCTURE FOR REFERENCE

{
  "referent_db_id": 317,
  "referent_uuid": "(not-recorded)",
  "name_first": "Nelly",
  "name_last": "",
  "tribes": ['abc'],
  "all_tribes": "abc",
  "sex": "Female",
  "origins": [],
  "vocations": [],
  "age": "13",
  "races": ["Indian"],
  "all_races": "Indian",
  "roles": [
    "Enslaved"
  ],
  "titles": [],
  "statuses": [
    "Slave"
  ],
  "citation_data": {
    "citation_db_id": 97,
    "citation_uuid": "(not-recorded)",
    "citation_type": "Document",
    "display": "“Return of the Registry of Indians on the Mosquito Shore in the year 1777.” TNA, CO 123/31/123-132.",
    "comments": ""
  },
  "reference_data": {
    "reference_db_id": 146,
    "reference_uuid": "(not-recorded)",
    "reference_type": "Inventory",
    "national_context": "British",
    "date_db": "1777-02-26 00:00:00",
    "date_display": "1777 February 26",
    "transcription": "[QUOT]At the Corn Islands at Cape Gracias a Dios at Black River[QUOT]; Same owner as Hemimo, Loraina, [AMP] Alinaes",
    "locations": [
      {
        "location_name": "Mosquito Coast",
        "location_type": null
      },
      {
        "location_name": "British Honduras",
        "location_type": "Colony/State"
      }
    ],
    "all_locations": "Mosquito Coast, British Honduras"
  },
  "relationships": [
    {
      "description": "enslaved by",
      "related_referent_info": {
        "related_referent_db_id": 318,
        "related_referent_first_name": "Robert",
        "related_referent_last_name": "Hodgson"
      }
    }
  ],
  "all_name": "Nelly",
  "enslavement_status": "Enslaved",
  "all_origins": "",
  "year": 1777
}

*/

