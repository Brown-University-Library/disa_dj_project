
(function() { // Open IIFE

  // Constants

  const DATA_ENDPOINT_URL = document.getElementById('denormalized_json_url').value,
        NAME_DISPLAY_OVERRIDES = {
          'unrecorded': 'No name is recorded ',
          'Unknown': 'No name is known '
        },
        BIO_THEME_CLASSNAME = 'biographical',
        VIEW_OPTIONS_RADIO_BUTTONS_ID = 'view-options';

  // Event handlers

  window.disa = {};

  window.populateTribeFilter = function(tribeName) {
    // console.log(tribeName);
    window.table.setHeaderFilterValue('description.tribe', tribeName);
  }

  window.populateNameFilter = function(nameSearchText) {
    // console.log(nameSearchText);
    window.table.setHeaderFilterValue('all_name', nameSearchText);
  }

  window.populateLocationFilter = function(locationSearchText) {
    // console.log(locationSearchText);
    window.table.setHeaderFilterValue('all_locations', locationSearchText);
  }

  // Called when "details" button pressed

  let detailsModal;

  window.showDetails = function(id) {

    const data = window.disa.jsonData.find(x => x.id === id);

    // Initialize modal

    if (detailsModal === undefined) {
      detailsModal = {
        show: () => $('#details-modal').modal('show'),
        setId: x => this.document.getElementById('details-id').innerText = x,
        name: x => document.getElementById('details-name').innerText = uncleanString(x),
        setTitleName: x => document.getElementById('details-title-name').innerHTML = uncleanString(x),
        setDocTitle: x => document.getElementById('details-doc').innerText = uncleanString(x),
        setTranscription: x => document.getElementById('details-transcription').innerHTML = x,
        clearDetailsTable: () => document.getElementById('details-table').innerHTML = '',
        addToDetailsTable: (label, value) => {
          document.getElementById('details-table').innerHTML = 
            document.getElementById('details-table').innerHTML +
            `<tr><th>${label}</th><td>${value}</td></tr>`;
        }
      }
    }

    // Populate modal

    if (data) {
      detailsModal.setTitleName(data.all_name);
      // detailsModal.name(data.all_name);
      detailsModal.setId(id);
      // detailsModal.transcription(data.comments.replace(/http[^\s]+/,''));
      detailsModal.setTranscription(data.comments);
      detailsModal.setDocTitle(data.docTitle.replace(/http[^\s]+/,''));
      detailsModal.show();
      detailsModal.clearDetailsTable();
      [
        ['Location', data.all_locations],
        ['First name', data.first_name],,
        ['Last name', data.last_name],
        ['Status', data.status],
        ['Date', new Date(data.date.year, data.date.month, data.date.day).toDateString()],
        ['Tribe', data.description.tribe],
        ['Sex', data.description.sex],
        ['Origin', data.description.origin],
        ['Vocation', data.description.vocation],
        ['Age', data.age],
        ['Has a father?', data.has_father],
        ['Has a mother?', data.has_mother],
        ['Owner', data.owner],
        ['Spouse', data.spouse]
      ].forEach(
        ([label, value]) => {
          if (value) { detailsModal.addToDetailsTable(label, value) }
        }
      );
    }
  }

  /*

    all_locations: "Mosquito Coast, British Honduras"
    all_name: "Margaritta"
    comments: "Same Owner as Dublin, Simon, Cillia, Juana, & Cillia"
    date: {year: 1777, month: 2, day: 26}
    description: {tribe: "", sex: "Female", origin: "", vocation: "", age: "Not Mentioned", …}
    docTitle: "“Return of the Registry of Indians on the Mosquito Shore in the year 1777.” TNA, CO 123/31/123-132."
    documents: {“Return of the Registry of Indians on the Mosquito Shore in the year 1777.” TNA, CO 123/31/123-132.: Array(1)}
    first_name: "Margaritta"
    has_father: ""
    has_mother: ""
    id: 309
    last_name: ""
    locations: (2) ["Mosquito Coast", "British Honduras"]
    owner: ""
    spouse: ""
    status: "enslaved"
    transcription: ""

  */

  // Global functions

  // Toggle special characters (single/double quotes; ampersand)
  //  with special codes
  // WARNING: don't use with transcription

  const ampersandRegex = /&(?!\w+;)/,
        aposRegEx = /'/g,
        quotRegEx = /"/g,
        aposRegEx_reverse = /\[APOS]/g,
        quotRegEx_reverse = /\[QUOT]/g,
        ampersandRegex_reverse = /\[AMP]/g;
        
  function cleanString(str) {
    return str.replace(aposRegEx, '[APOS]')
              .replace(quotRegEx, '[QUOT]')
              .replace(ampersandRegex, '[AMP]');
  }

  function uncleanString(str) {
    return str.replace(aposRegEx_reverse, "'")
              .replace(quotRegEx_reverse, '"')
              .replace(ampersandRegex_reverse, '&amp;');
  }

  // Main onload routine
  
  window.addEventListener('DOMContentLoaded', () => {
  
    // Lunr index function

    function indexInLunr(data) {
      return lunr(function () {

        this.ref('id');
        this.field('comments');
      
        data.forEach(function (entry) {
          this.add(entry)
        }, this);
      })
    }

    // Run the JSON through this when it comes back from the
    //  server. Save the data.
  
    const jsonProcessor = function(_, __, response) {
  
      console.log(response);

      // Create an 'all_names' field
      // Create an 'all_locations' field
      // Clean up data for apostrophes, ampersands

      response.forEach(entry => {

        // Name

        entry.first_name = cleanString(entry.first_name);
        entry.last_name = cleanString(entry.last_name);

        entry.all_name = [entry.first_name, entry.last_name]
                          .filter(name => (name))
                          .join(' ');
        // Location

        const docWithLocation = Object.values(entry.documents)[0]
          .find(doc => doc.locations && doc.locations.length);

        entry.locations = docWithLocation 
          ? docWithLocation.locations.map(loc => cleanString(loc))
          : [];
        // console.log('AFTER', entry.locations);
        entry.all_locations = entry.locations.join(', ');

        // Doc

        entry.docTitle = Object.keys(entry.documents)[0];
        entry.docTitle = cleanString(entry.docTitle);
        entry.comments = entry.comments.replace(/ style="[^"]*"/g,'');
      });

      // Index this in Lunr

      lunrIndex = indexInLunr(response);
      window.disa.lunrIndex = lunrIndex; // For testing

      // Save this data for later & return to Tabulator

      window.disa.jsonData = response; 
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
                'Other': 'child',
                '': 'child'
              },
              'adult': {
                'Female': 'woman',
                'Male': 'man',
                'Other': 'person',
                '': 'person'
              }
            },
            n = parseInt(data.description.age),
            age_number = (isNaN(n) ? undefined : n),
            ageStatus = (age_number && age_number <= 16 ? 'child' : 'adult'),
            age_text = (data.description.age === 'Not Mentioned' ? undefined : data.description.age)
            year = data.date.year;
            
      const html = `<a  class="details-button float-right" type="button" onclick="showDetails(${data.id})">Details</a>` +
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
  
    const bioViewOptionInputElem = document.getElementById('biographical-view-option'),
          tableContainer = document.getElementById('data-display');

    document.getElementById(VIEW_OPTIONS_RADIO_BUTTONS_ID).addEventListener('click', () => {
      const bioOption = bioViewOptionInputElem.checked;
      table.destroy();
      tableContainer.classList.toggle(BIO_THEME_CLASSNAME, bioOption);
      table = new Tabulator('#data-display', {
        height:'611px',
        layout:'fitColumns',
        placeholder:'No Data Set',
        pagination: 'local',
        paginationSize: 20,
        paginationSizeSelector:[20,50,100],
        data: window.disa.jsonData,
        columns: columnDefinitions,
        rowFormatter: !bioOption.checked ? rowFormatter : undefined
      });
    });
  
    // trigger AJAX load on 'Load Data via AJAX' button click
  
    window.table = table;
  
  });



})() // Closing IIFE

