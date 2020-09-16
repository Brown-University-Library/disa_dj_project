


window.addEventListener('DOMContentLoaded', () => {

  // define custom mutator

  const customMutator = function(value, data, type, params, component){

    // value - original value of the cell
    // data - the data for the row
    // type - the type of mutation occurring  (data|edit)
    // params - the mutatorParams object from the column definition
    // component - when the "type" argument is "edit", this contains the cell component for the edited cell, otherwise it is the column component for the column

    return `${data.first_name} ${data.last_name}`; //return the new value for the cell data.
  }

  const dataEndpointUrl = document.getElementById('denormalized_json_url').value,
        columnDefinitions = [
          { title:'Name',   field:'first_name', sorter:'string', mutator: customMutator },
          { title:'Status', field:'status',     sorter:'string', headerFilter: true }
        ];

  const getPersonEntryHTML = function(data) {
    //console.log(data);
    const name_text = data.description.title + data.first_name + (data.last_name ? ' ' + data.last_name : ''),
          statusDisplay = {
            'enslaved': 'enslaved'
          },
          docWithLocationId = Object.keys(data.documents).find(docId => {
            return data.documents[docId][0] && 
                   data.documents[docId][0].locations &&
                   data.documents[docId][0].locations.length
          }),
          location = (
            docWithLocationId 
            ? data.documents[docWithLocationId][0].locations.join(', ')
            : ''),
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

    window.ddd = data;

    const html = `<strong class='referent-name'>${name_text}</strong> is an ` + 
                 statusDisplay[data.status] + ' ' + 
                 sexDisplay[ageStatus][data.description.sex] +
                 (data.description.tribe ? ` of the <a>${data.description.tribe}</a>` : '') +
                 (age_text ? `, age ${age_text}` : '') +
                 (location ? ` from <a>${location}</a>` : '') + 
                 (year ? ` who lived in ${year}` : '') +
                 '.';

    return html;
  }

  const rowFormatter = function(row) {
    var data = row.getData();
    row.getElement().innerHTML = getPersonEntryHTML(data);
  };

  const table = new Tabulator('#data-display', {
    height:'611px',
    layout:'fitColumns',
    placeholder:'No Data Set',
    pagination: 'local',
    paginationSize: 20,
    paginationSizeSelector:[20,50,100],
    ajaxURL: dataEndpointUrl,
    columns: columnDefinitions,
    rowFormatter: rowFormatter
  });
  


  // trigger AJAX load on 'Load Data via AJAX' button click

  window.tt = table;

});