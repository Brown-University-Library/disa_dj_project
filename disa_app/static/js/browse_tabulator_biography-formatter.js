
import { uncleanString } from './browse_tabulator_clean-string.js';

// Given an entry, create a biographical sketch in HTML

function getPersonEntryHTML(entry, sr) {

  // BIO_NAME_DISPLAY_OVERRIDES maps things like 'unrecorded' to 'no name is recorded' (for ...)

  const nameDisplay = sr.BIO_NAME_DISPLAY_OVERRIDES[entry.name_first] || entry.name_first,
        name_forOrIs = sr.BIO_NAME_DISPLAY_OVERRIDES[entry.name_first] ? 'for' : 'was';

  // Set name text, including clickable anchor

  let name_text;

  if (nameDisplay || entry.name_last) {
    name_text = `<a href="#" onclick="populateFilter('all_name', '${nameDisplay}')" title="Show only people named '${nameDisplay}'">${uncleanString(nameDisplay)}</a>`
    + (entry.name_last ? ` <a href="#" onclick="populateFilter('all_name', '${entry.name_last}')" title="Show only people with last name '${entry.name_last}'">${uncleanString(entry.name_last)}</a>` : '');
    name_text = `<strong class='referent-name'>${name_text}</strong>`;
  } else {
    name_text = 'There '
  }

  // Enslavement status

  const statusDisplay = { // @todo make a global constant?
    [sr.ENSLAVEMENT_STATUS.ENSLAVED]: 'enslaved',
    [sr.ENSLAVEMENT_STATUS.ENSLAVER]: 'slave-owning',
    [sr.ENSLAVEMENT_STATUS.DEFAULT]: ''
  };

  // Location

  const locSearchTerms = entry.reference_data.locations.map(
    (_, i, locArr) => locArr.slice(i).map(x => x.location_name).join(', ')
  );
  
  const locationDisplay = entry.reference_data.locations.map((loc, i) => {
    return `<a  href="#" onclick="populateFilter('reference_data.all_locations', '${locSearchTerms[i]}')"
                title="Show only people located in ${locSearchTerms[i]}">${uncleanString(loc.location_name)}</a>`
  }).join(', ');

  // Age-related terms

  const ageAsNumber = parseInt(entry.age.replaceAll(/[^\d]/g, '')),
        age_number = (isNaN(ageAsNumber) ? undefined : ageAsNumber),
        ageStatus = (age_number && age_number <= sr.ADULT_CHILD_CUTOFF_AGE ? 'child' : 'adult'),
        age_text = (entry.age === '(not-recorded)' ? undefined : entry.age);

  // Sex-related terms

  const proNounCap = sr.BIO_SEX_DISPLAY_TERMS.pronoun[entry.sex].cap,
        toBe_conj = sr.BIO_SEX_DISPLAY_TERMS.pronoun[entry.sex].be_conj;

  const personNoun = sr.BIO_SEX_DISPLAY_TERMS[ageStatus][entry.sex],
        personArticle = 'aeiouAEIOU'.includes(personNoun[0]) ? 'an ' : 'a ';

  // Relationships
  
  let hasImpliedEnslavement;

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
      hasImpliedEnslavement = true;
    } else if (relationship.description === 'owner of') {
      if (relRefName != '') {
        html = `enslaved ${relRefNameLink}`;
      } else {
        html = `were an enslaver`;
      }
    } else if (relationship.description === 'escaped from') {
      html = `escaped from ${relRefNameLink}`;
      hasImpliedEnslavement = true;
    } else if (relationship.description === 'sold by') {
      html = `${toBe_conj} sold by ${relRefNameLink}`;
      hasImpliedEnslavement = true;
    } else if (relationship.description === 'mother of' || relationship.description === 'father of') {
      html = `had a child, ${relRefNameLink}`;
    } else if (relationship.description === 'child of') {
      html = `${toBe_conj} the child of ${relRefNameLink}`;
    } else {
      html = undefined;
    }
    return html;
  }).filter(r => r !== undefined);

  // If enslavement isn't implied in relationship, then
  //  explicitly name it

  if (hasImpliedEnslavement !== true && entry.enslavement_status === sr.ENSLAVEMENT_STATUS.ENSLAVED) {
    relationshipsArrayHTML.unshift(`was enslaved`);
  }

  // Put all the relationships together into a single HTML snippet

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

  // Tribal nation (link to filter)

  const nationLink = entry.tribes[0] 
    ? ` <a href="#" title="Show only ${entry.tribes[0]} people" onclick="populateFilter('all_tribes', '${entry.tribes[0]}')">${entry.tribes[0]}</a> ` 
    : '';

  // Buttons: details, edit

  const detailsButton = `<a  class="details-button float-right" onclick="showDetails(${entry.referent_db_id})"
                         title="Show source document and details for ${entry.all_name}">Details</a>`;

  const editButton = `<a class="details-button float-right" style="margin-right: 1em;" 
                         href="${sr.url.editReferent(entry.citation_data.citation_db_id, entry.reference_data.reference_db_id, entry.referent_db_id)}"
                         title="Edit entry for ${entry.all_name}">Edit</a>`;

  // Misc

  const racialDescriptor = (entry.all_races ? `, described as &ldquo;${entry.raceDescriptor}&rdquo;,` : ''),
        year = entry.year;

  // COMPILE FINAL NARRATIVE HTML

  const html =  detailsButton +
                (sr.user_is_authenticated ? editButton : '') +
                `${name_text} ${name_forOrIs} ` +
                personArticle +
                nationLink +
                personNoun +
                (age_text ? `, age ${age_text}` : '') +
                racialDescriptor +
                ` who lived in ${locationDisplay}` +
                (year ? ` in ${year}` : '') +
                '.' + 
                relationshipsHTML + 
                `<span id="referent-footnote-id-${entry.referent_db_id}" class="cf-footnotes"></span>`;

  return html;
}

// Row formatter function for Tabulator

function getBiographyRowFormatter(sr) {
  return function(row) {
    let entry = row.getData();
    row.getElement().innerHTML = getPersonEntryHTML(entry, sr);
  };
}

export { getBiographyRowFormatter }
