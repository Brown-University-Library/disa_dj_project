
window.addEventListener('DOMContentLoaded', () => {


  //define custom mutator
  const customMutator = function(value, data, type, params, component){
    //value - original value of the cell
    //data - the data for the row
    //type - the type of mutation occurring  (data|edit)
    //params - the mutatorParams object from the column definition
    //component - when the "type" argument is "edit", this contains the cell component for the edited cell, otherwise it is the column component for the column

    return `${data.first_name} ${data.last_name}`; //return the new value for the cell data.
  }

  const dataEndpointUrl = document.getElementById('denormalized_json_url').value,
        columnDefinitions = [
          { title:'Name',   field:'first_name', sorter:'string', mutator: customMutator },
          { title:'Status', field:'status',     sorter:'string', headerFilter: true }
        ];


  const table = new Tabulator('#data-display', {
    height:'311px',
    layout:'fitColumns',
    placeholder:'No Data Set',
    pagination: 'local',
    paginationSize: 20,
    ajaxURL: dataEndpointUrl,
    columns: columnDefinitions,
  });
  
  // trigger AJAX load on 'Load Data via AJAX' button click

  window.tt = table;

});