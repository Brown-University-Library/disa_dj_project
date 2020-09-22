
(function() { // Open IIFE

  // Constants

  const DATA_ENDPOINT_URL = document.getElementById('denormalized_json_url').value,
        NAME_DISPLAY_OVERRIDES = {
          'unrecorded': 'No name is recorded ',
          'Unknown': 'No name is known '
        },
        BIO_THEME_CLASSNAME = 'biographical';

  // Event handlers

  window.disa = {};

  window.populateTribeFilter = function(tribeName) {
    console.log(tribeName);
    window.table.setHeaderFilterValue('description.tribe', tribeName);
  }

  window.populateNameFilter = function(nameSearchText) {
    console.log(nameSearchText);
    window.table.setHeaderFilterValue('all_name', nameSearchText);
  }

  window.populateLocationFilter = function(locationSearchText) {
    console.log(locationSearchText);
    window.table.setHeaderFilterValue('all_locations', locationSearchText);
  }

  // Called when "details" button pressed

  let detailsModal;

  window.showDetails = function(id) {

    const data = window.disa.jsonData.find(x => x.id === id);

    if (detailsModal === undefined) {
      detailsModal = {
        show: () => $('#details-modal').modal('show'),
        id: x => this.document.getElementById('details-id').innerText = x,
        name: x => document.getElementById('details-name').innerText = x,
        titleName: x => document.getElementById('details-title-name').innerText = x,
        docTitle: x => document.getElementById('details-doc').innerText = x,
        transcription: x => document.getElementById('details-transcription').innerHTML = x
      }
    }

    if (data) {
      detailsModal.titleName(data.all_name);
      // detailsModal.name(data.all_name);
      // detailsModal.id(data.id);
      //detailsModal.transcription(data.comments.replace(/http[^\s]+/,''));
      detailsModal.transcription(data.comments);
      detailsModal.docTitle(data.docTitle.replace(/http[^\s]+/,''));
      detailsModal.show();
    }
  }

  // Main onload routine
  
  window.addEventListener('DOMContentLoaded', () => {
  
    // Combine first name and last name
  
    const combineNames_mutator = function(value, data, type, params, component) {
  
      // value - original value of the cell
      // data - the data for the row
      // type - the type of mutation occurring  (data|edit)
      // params - the mutatorParams object from the column definition
      // component - when the "type" argument is "edit", this contains the cell component for the edited cell, otherwise it is the column component for the column
  
      return [data.first_name, data.last_name]
              .filter(name => (name))
              .join(' ');
    }
  
    // Run the JSON through this when it comes back from the
    //  server. Save the data.
  
    let jsonData;
  
    const jsonProcessor = function(_, __, response) {
  
      console.log(response);
  
      // Create an 'all_names' field
      // Create an 'all_locations' field
      // Clean up data for apostrophes, ampersands

      response.forEach(entry => {

        entry.all_name = [entry.first_name, entry.last_name]
                          .filter(name => (name))
                          .join(' ');

        const docWithLocation = Object.values(entry.documents)[0]
          .find(doc => doc.locations && doc.locations.length);

        entry.locations = docWithLocation ? docWithLocation.locations : [];
        entry.all_locations = entry.locations.join(', ');
      });

      // Save this data for later & return to Tabulator

      jsonData = response; 
      return response;
    }
  
    const getPersonEntryHTML = function(data) {
  
      const nameDisplay = NAME_DISPLAY_OVERRIDES[data.first_name] || data.first_name,
            name_text = data.description.title 
                        + `<a href="#" onclick="populateNameFilter('${nameDisplay}')">${nameDisplay}</a>`
                        + (data.last_name ? ` <a href="#" onclick="populateNameFilter('${data.last_name}')">${data.last_name}</a>` : ''),
            name_forOrIs = NAME_DISPLAY_OVERRIDES[data.first_name] ? 'for' : 'is',
            statusDisplay = {
              'enslaved': 'enslaved'
            },
            locSearchTerms = data.locations.map((_, i, locArr) => locArr.slice(i).join(', ')),
            locationDisplay = data.locations.map((loc, i) => 
              `<a href="#" onclick="populateLocationFilter('${locSearchTerms[i]}')">${loc}</a>`
            ).join(', '),
            sexDisplay = {
              'child': {
                'Female' : 'girl',
                'Male': 'boy',
                '': 'child'
              },
              'adult': {
                'Female': 'woman',
                'Male': 'man',
                '': 'person'
              }
            },
            n = parseInt(data.description.age),
            age_number = (isNaN(n) ? undefined : n),
            ageStatus = (age_number && age_number <= 16 ? 'child' : 'adult'),
            age_text = (data.description.age === 'Not Mentioned' ? undefined : data.description.age)
            year = data.date.year;
            
      const html = `<a  class="details-button float-right" 
      type="button" onclick="showDetails(${data.id})">Details</a>` +
                   `<strong class='referent-name'>${name_text}</strong> ${name_forOrIs} an ` + 
                   statusDisplay[data.status] + ' ' + 
                   (data.description.tribe ? ` <a href="#" onclick="populateTribeFilter('${data.description.tribe}')">${data.description.tribe}</a> ` : '') +
                   sexDisplay[ageStatus][data.description.sex] +
                   (age_text ? `, age ${age_text}` : '') +
                   ` in ${locationDisplay}` + 
                   (year ? ` who lived in ${year}` : '') +
                   '.';
  
      return html;
    }
  
    const rowFormatter = function(row) {
      var data = row.getData();
      row.getElement().innerHTML = getPersonEntryHTML(data);
    };
  
    const columnDefinitions = [
      { title:'Name',      field:'all_name',          sorter:'string', headerFilter: true }, // mutator: combineNames_mutator },
      { title:'Last name', field:'last_name',         sorter:'string', headerFilter: true, visible: false },
      { title:'Sex',       field:'description.sex',   sorter:'string', headerFilter: 'select', headerFilterParams:{ values: ['Male','Female'] } },
      { title:'Tribe',     field:'description.tribe', sorter:'string', headerFilter: true },
      { title:'Age',       field:'description.age',   sorter:'string', headerFilter: true },
      { title:'Location',  field:'all_locations',     sorter:'string', headerFilter: true }
    ];
  
    let table = new Tabulator('#data-display', {
      height:'611px',
      layout:'fitColumns',
      placeholder:'No Data Set',
      pagination: 'local',
      paginationSize: 20,
      paginationSizeSelector:[20,50,100],
      ajaxURL: DATA_ENDPOINT_URL,
      columns: columnDefinitions,
      rowFormatter: rowFormatter,
      ajaxResponse: jsonProcessor
    });
    
    const bioOption = document.getElementById('biographical-view'),
          tableContainer = document.getElementById('data-display');
  
    bioOption.addEventListener('change', (elem, p) => {
      table.destroy();
      tableContainer.classList.toggle(BIO_THEME_CLASSNAME, !bioOption.checked);
      table = new Tabulator('#data-display', {
        height:'611px',
        layout:'fitColumns',
        placeholder:'No Data Set',
        pagination: 'local',
        paginationSize: 20,
        paginationSizeSelector:[20,50,100],
        data: jsonData,
        columns: columnDefinitions,
        rowFormatter: !bioOption.checked ? rowFormatter : undefined
      });
    });
  
    // trigger AJAX load on 'Load Data via AJAX' button click
  
    window.table = table;
  
  });



})() // Closing IIFE

