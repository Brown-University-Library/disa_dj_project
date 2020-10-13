
(function() { // Open IIFE

  // Constants

  const DATA_ENDPOINT_URL = document.getElementById('denormalized_json_url').value,
        NAME_DISPLAY_OVERRIDES = {
          'unrecorded': 'No name is recorded ',
          'Unknown': 'No name is known '
        },
        BIO_THEME_CLASSNAME = 'biographical',
        VIEW_OPTIONS_RADIO_BUTTONS_ID = 'view-options',
        MIN_TIME_BETWEEN_LUNR_INDEXES = 1000;

  // Event handlers

  window.disa = {};

  window.populateTribeFilter = function(tribeName) {
    window.table.setHeaderFilterValue('description.tribe', tribeName);
  }

  window.populateNameFilter = function(nameSearchText) {
    window.table.setHeaderFilterValue('all_name', nameSearchText);
  }

  window.populateLocationFilter = function(locationSearchText) {
    window.table.setHeaderFilterValue('all_locations', locationSearchText);
  }

  // Called when "details" button pressed

  let detailsModal;

  window.showDetails = function(id) {

    const data = window.disa.jsonData.find(x => x.id === id);

    // Initialize modal

    function getModalContentSetter(idOrClass, textOrHTML) {
      const elems = document.querySelectorAll(`#${idOrClass},.${idOrClass}`);
      return function(content) {
        elems.forEach(elem => elem[`inner${textOrHTML}`] = content);
      }
    }

    const setDetailsTable = getModalContentSetter('details-table', 'HTML');

    if (detailsModal === undefined) {
      detailsModal = {
        show: () => $('#details-modal').modal('show'),
        setId: getModalContentSetter('details-id', 'Text'),
        setName: getModalContentSetter('details-title-name', 'Text'),
        setDocTitle: getModalContentSetter('details-doc', 'Text'),
        setTranscription: getModalContentSetter('details-transcription', 'HTML'),
        clearDetailsTable: () => setDetailsTable(''),
        addToDetailsTable: (label, value) => {
          document.getElementById('details-table').innerHTML += 
            `<tr><th>${label}</th><td>${value}</td></tr>`;
        }
      }
    }

    // Populate modal

    if (data) {
      detailsModal.setName(data.all_name);
      detailsModal.setId(id);
      // detailsModal.transcription(data.comments.replace(/http[^\s]+/,''));
      detailsModal.setTranscription(data.comments);
      detailsModal.setDocTitle(data.docTitle.replace(/http[^\s]+/,''));
      detailsModal.clearDetailsTable();
      
      const detailsTableContent = [
        ['Location', data.all_locations],
        ['First name', data.first_name],
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
      ];
      
      detailsTableContent.forEach(
        ([label, value]) => {
          if (value) { detailsModal.addToDetailsTable(label, value) }
        }
      );

      detailsModal.show();
    }
  }

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

  // Lunr index function

  let lunrIndex, currLunrSelection;

  function indexInLunr(data) {

    // Create a list of documents with ID
    //   and text (which combines all the DISA fields to search)

    const docList = data.map(entry => {

      const indexableText = [ 
        entry.first_name, entry.last_name,
        entry.comments, Object.keys(entry.documents).join(' '),
        entry.locations.join(' '),
        Object.values(entry.description).join(' ') 
      ].join(' ');
  
      const indexableText_noHTML = indexableText.replace(/\<[^>]+>/g, '');

      return {
        id: entry.id,
        text: indexableText_noHTML
      }
    });

    // Create lunr index from the documents

    const index = lunr( function () {
      this.ref('id');
      this.field('text');
    
      docList.forEach(function (document) {
        this.add(document)
      }, this);
    });

    return index;
  }

  function checkAgainstGeneralSearch(data) {
    return currLunrSelection.includes(data.id);
  }

  // Main onload routine
  
  window.addEventListener('DOMContentLoaded', () => {

    // General search box listener
    //   When user inputs something, trigger a re-indexing

    document.getElementById('general-search')
            .addEventListener('input', searchAgainstIndex);

    // Run the JSON through this when it comes back from the
    //  server. Save the data.
  
    const jsonProcessor = function(_, __, response) {
  
      console.log('JSON response', response);

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
      searchAgainstIndex(); // Initialize results array for general search

      // Save this data for later & return to Tabulator

      window.disa.jsonData = response; 
      return response;
    }
  
    const getPersonEntryHTML = function(data) {
  
      const nameDisplay = NAME_DISPLAY_OVERRIDES[data.first_name] || data.first_name,
            name_text = data.description.title 
                        + `<a href="#" onclick="populateNameFilter('${nameDisplay}')" title="Show only people named '${nameDisplay}'">${nameDisplay}</a>`
                        + (data.last_name ? ` <a href="#" onclick="populateNameFilter('${data.last_name}')" title="Show only people with last name '${data.last_name}'">${data.last_name}</a>` : ''),
            name_forOrIs = NAME_DISPLAY_OVERRIDES[data.first_name] ? 'for' : 'is',
            statusDisplay = {
              'enslaved': 'enslaved'
            },
            locSearchTerms = data.locations.map((_, i, locArr) => locArr.slice(i).join(', ')),
            locationDisplay = data.locations.map((loc, i) => {
              return `<a  href="#" onclick="populateLocationFilter('${locSearchTerms[i]}')" 
                          title="Show only people located in ${locSearchTerms[i]}">${uncleanString(loc)}</a>`
            }).join(', '),
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
            ageAsNumber = parseInt(data.description.age),
            age_number = (isNaN(ageAsNumber) ? undefined : ageAsNumber),
            ageStatus = (age_number && age_number <= 16 ? 'child' : 'adult'),
            age_text = (data.description.age === 'Not Mentioned' ? undefined : data.description.age),
            race_text = (data.description.race ? `, described as &ldquo;${data.description.race}&rdquo;,` : ''),
            year = data.date.year;
            
      const html = `<a  class="details-button float-right" type="button" onclick="showDetails(${data.id})" 
                        title="Show source document and details for ${data.all_name}">Details</a>` +
                   `<strong class='referent-name'>${name_text}</strong> ${name_forOrIs} an ` + 
                   statusDisplay[data.status] + ' ' + 
                   (data.description.tribe ? ` <a href="#" title="Show only ${data.description.tribe} people" onclick="populateTribeFilter('${data.description.tribe}')">${data.description.tribe}</a> ` : '') +
                   sexDisplay[ageStatus][data.description.sex] +
                   (age_text ? `, age ${age_text}` : '') +
                   race_text +
                   ' who lived' +
                   ` in ${locationDisplay}` + 
                   (year ? ` in ${year}` : '') +
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
      { title:'Status',    field:'status',            sorter:'string', headerFilter: true },
      { title:'Sex',       field:'description.sex',   sorter:'string', 
        headerFilter: 'select', headerFilterParams:{ values: ['Male','Female', 'Other'] } },
      { title:'Tribe',     field:'description.tribe', sorter:'string', headerFilter: true },
      { title:'Race',      field:'description.race',  sorter:'string', headerFilter: true },
      // { title:'Age',       field:'description.age',   sorter:'string', headerFilter: true },
      { title:'Location',  field:'all_locations',     sorter:'string', headerFilter: true },
      { title:'Year',      field:'date.year',         sorter:'string', headerFilter: true }
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

    table.addFilter(data => {
      return currLunrSelection.includes(data.id);
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
        rowFormatter: bioOption ? rowFormatter : undefined
      });

      table.addFilter(data => {
        return currLunrSelection.includes(data.id);
      });
    });

    window.table = table;

    // This is called every time a user changes the content of the
    //   general search box

    let lastSearchTimestamp = 0, timeOutId;
    const generalSearchInput = document.getElementById('general-search');

    function searchAgainstIndex(x) {

      const searchTextChanged = (x !== false);

      // If enough time has passed ...

      if (Date.now() - lastSearchTimestamp > MIN_TIME_BETWEEN_LUNR_INDEXES) {

        // Do a search against index & force Tabulator to reapply filters

        currLunrSelection = lunrIndex.search(generalSearchInput.value).map(x => parseInt(x.ref));
        console.log(`Searching for ${generalSearchInput.value}`, 'Results:', currLunrSelection);
        table.setFilter(table.getFilters());

        // Update times

        lastSearchTimestamp = Date.now();

        // If this update is becuase of a change in the 
        //   search field, then schedule a future
        //   search to catch any changes

        if (searchTextChanged) {
          window.clearTimeout(timeOutId);
          timeOutId = window.setTimeout(
            () => { searchAgainstIndex(false) }, 
            MIN_TIME_BETWEEN_LUNR_INDEXES + 100
          );
        }
      }
    }

    // searchAgainstIndex(); // Initialize results array for general search

  });

})() // Closing IIFE
