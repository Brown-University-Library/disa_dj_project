
import srPageSettings from './browse_tabulator_getPageSettings.js'; 
import * as srConstants from './browse_tabulator_constants.js';

const editUrlRoot = srPageSettings.redesign_citations_url;

const srGlobalObject = Object.assign({}, { 
    url: {
        editReferent: (sourceId, recordId, referentId) => `${editUrlRoot}${sourceId}/#/${recordId}/${referentId}`,
        editRecord: (sourceId, recordId) => `${editUrlRoot}${sourceId}/#/${recordId}`,
        editSource: (sourceId) => `${editUrlRoot}${sourceId}`
    },
    DATA_ENDPOINT_URL: srPageSettings.browse_json_url,
}, srPageSettings, srConstants);

export { srGlobalObject }