
import { cleanString } from './browse_tabulator_clean-string.js';

// Given the JSON data loaded from the API, 
// cleans, processes, and prepares that JSON object
// for ingestion into Tabulator

// Run the JSON through this when it comes back from the
//  server. Save the data.

function processJSON(response, sr) {

  // Update count stats
  // @TODO move this elsewhere

  document.getElementById(sr.REF_COUNT_ELEM_ID).innerText = response.meta.referents_count;
  document.getElementById(sr.ITEM_COUNT_ELEM_ID).innerText = response.referent_list.reduce(
    (setOfRefs, currRef) => setOfRefs.add(currRef.reference_data.reference_db_id),
    new Set()
  ).size;

  // Create an 'all_names' field
  // Create an 'all_locations' field
  // Clean up data for apostrophes, ampersands

  let processedResponse = response.referent_list.map(entry => {

    // Copy all properties over to newEntry

    let newEntry = JSON.parse(JSON.stringify(entry));

    // Clean strings

    newEntry.name_first = cleanString(newEntry.name_first);
    newEntry.name_last = cleanString(newEntry.name_last);
    newEntry.tribes = newEntry.tribes.map(cleanString);
    newEntry.citation_data.display = cleanString(newEntry.citation_data.display);
    newEntry.citation_data.comments = cleanString(newEntry.citation_data.comments);
    // newEntry.reference_data.transcription = cleanString(newEntry.reference_data.transcription);
    newEntry.reference_data.locations.forEach(
      loc => loc.location_name = cleanString(loc.location_name)
    );
    newEntry.sex = newEntry.sex === '(not-recorded)' ? '' : newEntry.sex;

    // Additional tabulator/lunr fields

    newEntry.all_name = [newEntry.name_first, newEntry.name_last]
      .filter(name => (name))
      .join(' ');

    newEntry.reference_data.all_locations = newEntry.reference_data.locations
      .reverse()
      .map(loc => loc.location_name)
      .join(', ');

    newEntry.all_tribes = newEntry.tribes.join(', ');
    newEntry.all_races = newEntry.races.join(', ');
    newEntry.year = (new Date(entry.reference_data.date_db)).getFullYear();

    // Add a derivative field for Enslaved/Enslaver/Other filter

    function includesAny(compareArr1, compareArr2) {
      return compareArr1.reduce(
        (acc, role) => acc || compareArr2.includes(role),
        false
      )
    }

    if (includesAny(entry.statuses, sr.ENSLAVED_STATUSES ||
        includesAny(entry.roles, sr.ENSLAVED_ROLES))) {
      newEntry.enslavement_status = sr.ENSLAVEMENT_STATUS.ENSLAVED;
    } else if (includesAny(entry.statuses, sr.ENSLAVER_STATUSES) ||
               includesAny(entry.roles, sr.ENSLAVER_ROLES)) {
      newEntry.enslavement_status = sr.ENSLAVEMENT_STATUS.ENSLAVER;
    } else {
      newEntry.enslavement_status = sr.ENSLAVEMENT_STATUS.DEFAULT;
    }

    // Some additional fields for Maiah's download

    newEntry.vocation = newEntry.vocations.join(',');

    newEntry.enslaved_by = newEntry.relationships.filter(
      rel => (rel.description === 'enslaved by')
    ).map(
      rel => rel.related_referent_info.related_referent_first_name + ' ' +
              rel.related_referent_info.related_referent_last_name
    ).join('; ');

    newEntry.enslaved = newEntry.relationships.filter(
      rel => (rel.description === 'owner of')
    ).map(
      rel => rel.related_referent_info.related_referent_first_name + ' ' +
              rel.related_referent_info.related_referent_last_name
    ).join('; ');

    return newEntry;
  });
  
  return processedResponse;
}

export { processJSON }

