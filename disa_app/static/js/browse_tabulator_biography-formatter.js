

import { uncleanString } from './browse_tabulator_clean-string.js';

// Given an entry, create a biographical sketch in HTML

function getPersonEntryHTML(entry, sr) {

  const nameDisplay = sr.NAME_DISPLAY_OVERRIDES[entry.name_first] || entry.name_first,
        name_forOrIs = sr.NAME_DISPLAY_OVERRIDES[entry.name_first] ? 'for' : 'is';

  let name_text;

  if (nameDisplay || entry.name_last) {
    name_text = `<a href="#" onclick="populateFilter('all_name', '${nameDisplay}')" title="Show only people named '${nameDisplay}'">${uncleanString(nameDisplay)}</a>`
    + (entry.name_last ? ` <a href="#" onclick="populateFilter('all_name', '${entry.name_last}')" title="Show only people with last name '${entry.name_last}'">${uncleanString(entry.name_last)}</a>` : '');
    name_text = `<strong class='referent-name'>${name_text}</strong>`;
  } else {
    name_text = 'There '
  }

  const statusDisplay = { // @todo make a global constant?
          [sr.ENSLAVEMENT_STATUS.ENSLAVED]: 'enslaved',
          [sr.ENSLAVEMENT_STATUS.ENSLAVER]: 'slave-owning',
          [sr.ENSLAVEMENT_STATUS.DEFAULT]: ''
        },
        locSearchTerms = entry.reference_data.locations.map(
          (_, i, locArr) => locArr.slice(i).map(x => x.location_name).join(', ')
        ),
        locationDisplay = entry.reference_data.locations.map((loc, i) => {
          return `<a  href="#" onclick="populateFilter('reference_data.all_locations', '${locSearchTerms[i]}')"
                      title="Show only people located in ${locSearchTerms[i]}">${uncleanString(loc.location_name)}</a>`
        }).join(', '),
        sexDisplay = { // @todo make a global constant?
          'child': {
            'Female' : 'girl',
            'Male': 'boy',
            'Other': 'child',
            '': 'child'
          },
          'adult': {
            'Female': 'woman',
            'Male': 'man',
            'Other': 'individual',
            '': 'individual'
          },
          'pronoun': {
            'Female': { cap: 'She', nocap: 'she', be_conj: 'was'},
            'Male': { cap: 'He', nocap: 'he', be_conj: 'was'},
            'Other': { cap: 'They', nocap: 'they', be_conj: 'were'},
            '': { cap: 'They', nocap: 'they', be_conj: 'were'}
          }
        },
        ageAsNumber = parseInt(entry.age.replaceAll(/[^\d]/g, '')),
        age_number = (isNaN(ageAsNumber) ? undefined : ageAsNumber),
        ageStatus = (age_number && age_number <= sr.ADULT_CHILD_CUTOFF_AGE ? 'child' : 'adult'),
        age_text = (entry.age === '(not-recorded)' ? undefined : entry.age),
        race_text = (entry.all_races ? `, described as &ldquo;${entry.all_races}&rdquo;,` : ''),
        year = entry.year,
        proNounCap = sexDisplay.pronoun[entry.sex].cap,
        toBe_conj = sexDisplay.pronoun[entry.sex].be_conj;

  // GENERATE RELATIONSHIPS DESCRIPTION
  
  const relationshipsArrayHTML = entry.relationships.map(relationship => {
    let html;
    const relRefInfo = relationship.related_referent_info,
          relRefName = [relRefInfo.related_referent_first_name, relRefInfo.related_referent_last_name]
                        .filter(x => x.length)
                        .join(' '),
          relRefNameLink = `<a href='#' onclick='showDetails(${relRefInfo.related_referent_db_id})' 
                                title='Details about ${relRefName}'>${relRefName}</a>`;
    if (relationship.description === 'enslaved by') {
      html = `${toBe_conj} enslaved by ${relRefNameLink}`;
    } else if (relationship.description === 'owner of') {
      html = `enslaved ${relRefNameLink}`;
    } else if (relationship.description === 'escaped from') {
      html = `escaped from ${relRefNameLink}`;
    } else if (relationship.description === 'sold by') {
      html = `${toBe_conj} sold by ${relRefNameLink}`;
    } else if (relationship.description === 'mother of' || relationship.description === 'father of') {
      html = `had a child, ${relRefNameLink}`;
    } else if (relationship.description === 'child of') {
      html = `${toBe_conj} the child of ${relRefNameLink}`;
    } else {
      html = undefined;
    }
    return html;
  }).filter(r => r !== undefined);

  let relationshipsHTML;

  if (relationshipsArrayHTML.length) {
    const lastRel = relationshipsArrayHTML.pop();
    relationshipsHTML = ' ' + proNounCap + ' ' +
                        (relationshipsArrayHTML.length 
                          ? `${relationshipsArrayHTML.join(', ')}, and ` 
                          : '') +
                        lastRel + '.';
  } else {
    relationshipsHTML = ''
  }
  
  // COMPILE FINAL HTML

  const html = `<a  class="details-button float-right" onclick="showDetails(${entry.referent_db_id})"
                    title="Show source document and details for ${entry.all_name}">Details</a>` +
                (sr.user_is_authenticated
                  ? `<a class="details-button float-right" style="margin-right: 1em;" 
                        href="${sr.url.editReferent(entry.citation_data.citation_db_id, entry.reference_data.reference_db_id, entry.referent_db_id)}"
                        title="Edit entry for ${entry.all_name}">Edit</a>` 
                  : '') +
                `${name_text} ${name_forOrIs} ` +
                (statusDisplay[entry.enslavement_status][0] === 'e' ? 'an ' : 'a ') +
                statusDisplay[entry.enslavement_status] + ' ' +
                // (entry.description.tribe ? ` <a href="#" title="Show only ${entry.description.tribe} people" data-filter-function='populateTribeFilter' data-filter-arg="${entry.description.tribe}" onclick="populateTribeFilter('${entry.description.tribe}')">${entry.description.tribe}</a> ` : '') +
                // (entry.tribes[0] ? ` <a href="#" title="Show only ${entry.tribes[0]} people" data-filter-field='all_tribes' data-filter-value="${entry.tribes[0]}">${entry.tribes[0]}</a> ` : '') +
                (entry.tribes[0] ? ` <a href="#" title="Show only ${entry.tribes[0]} people" onclick="populateFilter('all_tribes', '${entry.tribes[0]}')">${entry.tribes[0]}</a> ` : '') +
                
                sexDisplay[ageStatus][entry.sex] +
                // `:: ${ageStatus}  / ${entry.sex} ::` +
                (age_text ? `, age ${age_text}` : '') +
                race_text +
                ' who lived' +
                ` in ${locationDisplay}` +
                (year ? ` in ${year}` : '') +
                '.' + 
                relationshipsHTML;

  return html;
}

function getBiographyRowFormatter(sr) {
  return function(row) {
    let entry = row.getData();
    row.getElement().innerHTML = getPersonEntryHTML(entry, sr);
  };
}


export { getBiographyRowFormatter }