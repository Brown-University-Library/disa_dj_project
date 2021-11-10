
import { getBiographyRowFormatter } from './browse_tabulator_biography-formatter.js';


// Given data, initialize the Tabulator-based table

// Clean the cruft (mostly MSOffice markup) out of the transcription
//  before download

function transcriptionDownloadAccessor(value) {
  const noStyle = value.replace(/<style>.*<\/style>/gis, ''),
        noMSOfficeGarbage = noStyle.replace(/<([wmo]:\w+)[^>]*>.*?<\/\1[^>]*>/gis, ''),
        noHTML = noMSOfficeGarbage.replace(/<[^>]+>/g, ''),
        cleanSpaces = noHTML.replace(/(\s\s+|\n)/gs, ' ');
  return cleanSpaces;
}

function getTabulatorOptions(sr, showDetailsFunction, setFilterFunction) {

  // Columns

  const columnDefinitions = [

    { title:'Name',      field:'all_name',          sorter:'string', headerFilter: true }, // mutator: combineNames_mutator },
    { title:'Last name', field:'name_last',         sorter:'string', headerFilter: true, visible: false },
    { title:'Status',    field:'enslavement_status',            sorter:'string', headerFilter: true,
      headerFilter: 'select', headerFilterParams:{ values: ['Enslaved','Enslaver','Neither'] }, download: true },
    // { title:'Roles',    field:'roles',              sorter:'string', headerFilter: true },
    { title:'Sex',       field:'sex',   sorter:'string',
      headerFilter: 'select', headerFilterParams:{ values: ['Male','Female', 'Other'] } },
    { title:'Tribe',     field:'all_tribes', sorter:'string',
      headerFilter: 'select',
      headerFilterParams: {
        values: [ '"daughter of a Spanish Squaw"', "Apalachee", "Blanco", "Blanea", "Bocotora",
                  "Bousora", "Boustora", "Chaliba", "Cherokee", "Codira", "Cookra", "Creek",
                  "Cuol", "Curero", "Eastern Pequot", "Eastern Tribes", "Mashantucket Pequot",
                  "Mohegan", "Naragansett", "Natchez", "Nidwa", "Nipmuc", "Noleva", "Nome Lackee",
                  "Nomi Lackee", "Oquelonex", "Pequot", "Portoback", "Rocotora", "Sambo", "Shaliba",
                  "Shalliba", "Shangina", "Shargana", "Shatyana", "Souix,Sioux", "Spanish", "Talusky",
                  "Tanybec", "Tenebec", "Tenybec", "Terriby", "Thalliba", "Toluskey", "Unspecified",
                  "Valiante", "Valience", "Wackaway", "Wampanoag", "Warao", "Weanoke,Weanock,Powhatan",
                  "Weyanoke", "Woolwa", "de Nacion Caribe Cuchibero" ]
      }
    },
    { title:'Race',      field:'all_races',  sorter:'string',
      headerFilter: 'select',
      headerFilterParams: {
        values: [ "Asiatic", "Black", "Carolina Indian", "Creole", "Creole", "Dark melattress",
                  "Dark mulatto", "East India Negro", "East-India Indian", "East-Indian", "Griffon",
                  "Half Indian", "Half Indian", "Half Negro", "Indian", "Indian Mulatto", "Irish",
                  "Martha's Vineyard Indian", "Mulatto", "Mustee", "Negro", "Sambo", "Spanish Indian",
                  "Surinam Indian", "White" ]
      }
    },
    // { title:'Age',       field:'description.age',   sorter:'string', headerFilter: true },
    { title:'Location',  field:'reference_data.all_locations',     sorter:'string', headerFilter: true },
    { title:'Year',      field:'year',         sorter:'string', headerFilter: true },

    // Some hidden fields just for downloading and general search

    { title:'Source transcription', field:'reference_data.transcription', visible: false, download: true, 
      accessorDownload:transcriptionDownloadAccessor },
    { title:'Referent_ID', field:'referent_db_id', visible: false, download: true },
    { title:'Vocation', field:'vocation', visible: false, download: true },
    { title:'Age', field:'age', visible: false, download: true },
    { title:'Reference_ID', field:'reference_data.reference_db_id', visible: false, download: true },
    { title:'Enslaved_by', field:'enslaved_by', visible: false, download: true },
    { title:'Enslaved', field:'enslaved', visible: false, download: true }
  ];

  // Global options

  const tabulatorOptions_global = {
    data: sr.data,
    height:'611px',
    layout:'fitColumns',
    placeholder: sr.NO_RESULTS_MESSAGE,
    pagination: 'local',
    paginationSize: 20,
    paginationSizeSelector:[20,50,100,10000],
    columns: columnDefinitions,
    downloadRowRange: 'active', /*
    renderComplete: (x) => {
      console.log('EEE', x, this);
      document.querySelectorAll("*[data-filter-function]").forEach(
        setFilterLink => { 
          const onclickFunctionName = x.getAttribute('data-filter-field'),
                onclickFunctionArg = x.getAttribute('data-filter-value'),
                // onclickFunction = () => { console.log('YESS'); window[onclickFunctionName](onclickFunctionArg);}
                onClickFunction = () => setFilterFunction(onclickFunctionName, onclickFunctionArg);
          setFilterLink.addEventListener('click', onClickFunction, true);
        }
      )
    } */
  };

  // Handler for when a user clicks on a row in tabular format

  const rowClick = function(_, row) {
    showDetailsFunction(row.getData().referent_db_id);
  };

  // Complete Tabulator options for two modes: Biographical and Tabular

  const TABULATOR_OPTIONS_BIO = Object.assign(
    {}, tabulatorOptions_global, { rowFormatter: getBiographyRowFormatter(sr) }
  );

  const TABULATOR_OPTIONS_TABLE = Object.assign(
    {}, tabulatorOptions_global, { rowClick }
  );

  return {
    BIOGRAPHICAL: TABULATOR_OPTIONS_BIO,
    TABULAR: TABULATOR_OPTIONS_TABLE
  }
}

function getTableRenderer(sr, showDetailsFunction, generalSearch) {

  const options = getTabulatorOptions(sr, showDetailsFunction);
  let table;

  function createTable(mode = 'BIOGRAPHICAL') { // mode = 'BIOGRAPHICAL' or 'TABULAR'
    if (table) { table.destroy() }
    table = new Tabulator(`#${sr.TABULATOR_CONTAINER_ID}`, options[mode]);
    table.addFilter(data => {
      return generalSearch.currentResults().includes(data.referent_db_id);
    });
  }

  // Download workaround: make the page size a huge number, download, 
  //  then set it back to what it was

  function download() {
    const oldPageSize = table.getPageSize();
    table.setPageSize(sr.MAX_NUMBER_OF_ENTRIES);
    table.download('csv', `disa-data-export_${Date.now()}.csv`);
    table.setPageSize(oldPageSize);
  }

  createTable(); // Initialize table

  return {
    switchMode: createTable,
    download,
    refresh: function () {
      console.log(table);
      table.refreshFilter();
    },
    setHeaderFilterValue: function (headerId, value) { 
      table.setHeaderFilterValue(headerId, value) 
    }
  };
}

export { getTableRenderer }