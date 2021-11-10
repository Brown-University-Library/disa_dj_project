
import srPageSettings from './browse_tabulator_getPageSettings.js'; 
import * as srConstants from './browse_tabulator_constants.js';
import { getStolenRelationsData } from './browse_tabulator_getData.js';
import { processJSON } from './browse_tabulator_json-processor.js';

// Initializes the global sr object
// (contains data, user constants, session settings, global functions, etc.)

const editUrlRoot = srPageSettings.redesign_citations_url,
      dataEndpoint = srPageSettings.browse_json_url,
      data = await getStolenRelationsData(dataEndpoint),
      processedData = processJSON(data, srConstants);

const srGlobalObject = Object.assign({}, { 
    url: {
        editReferent: (sourceId, recordId, referentId) => `${editUrlRoot}${sourceId}/#/${recordId}/${referentId}`,
        editRecord: (sourceId, recordId) => `${editUrlRoot}${sourceId}/#/${recordId}`,
        editSource: (sourceId) => `${editUrlRoot}${sourceId}`
    },
    data: processedData,
    table: undefined, // will hold the tabulator object
    doGeneralSearch: undefined // will hold the general search function
}, srPageSettings, srConstants);

export { srGlobalObject }