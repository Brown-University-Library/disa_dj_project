# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint, re
# from operator import itemgetter

import django, sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from django.core.cache import cache
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def run_search( srch_text: str, start_time: datetime.datetime ) -> dict:
    """ Queries people, citations, and items for search-text.
        Called by views.search_results() """
    log.debug( f'srch_text, ```{srch_text}```' )
    session = make_session()
    cache_key = srch_text
    query_results: dict = cache.get( cache_key )  # see CACHE envar-settings for timeout
    if query_results is None:
         log.debug( 'query_results were not in cache' )
         query_results = run_query( srch_text, session )
         cache.set( cache_key, query_results )
    data = {
        'people_results': query_results['people_results'],
        'citation_results': query_results['citation_results'],
        'item_results': query_results['item_results'],
        'search_query': srch_text,
        'time_taken': str( datetime.datetime.now() - start_time )
        }
    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


def run_query( srch_text, session ) -> dict:
    """ Caller of individual queries.
        Called by run_search()
        Makes caching easier; TODO: consider async db calls. """
    queried_persons: list = query_persons( srch_text, session )
    queried_persons_via_tribes: list = query_persons_via_tribes( srch_text, session )
    all_persons = list( set(queried_persons + queried_persons_via_tribes) )

    people_results = process_persons( all_persons, session )

    citation_results = search_citations( srch_text, session )

    queried_items_via_transcription: list = query_items_via_transcription( srch_text, session  )
    queried_items_via_location: list = query_items_via_location( srch_text, session  )
    all_items = list( set(queried_items_via_transcription + queried_items_via_location) )

    item_results = process_items( all_items, srch_text )

    query_dct = {
        'people_results': people_results, 'citation_results': citation_results, 'item_results': item_results }
    log.debug( 'returning query_dct' )
    return query_dct


def query_persons( srch_text, session ) -> list:
    """ Searches `Person` table.
        Called by run_query() """
    persons = []
    qset_persons = session.query( models_alch.Person ).filter(
        or_(
            models_alch.Person.first_name.contains( srch_text ),
            models_alch.Person.last_name.contains( srch_text ),
            models_alch.Person.comments.contains( srch_text )
            ) ).all()
    for person in qset_persons:
        persons.append( person )
    log.debug( f'persons, ```{pprint.pformat(persons)}```' )
    return persons


def query_persons_via_tribes( srch_text, session ) -> list:
    """ Searches tribes table.
        Finds all referents for each tribe entry.
        Finds all persons for each referent and returns them.
        Called by run_query() """
    tribes = []
    referents = []
    persons = []
    qset_tribes = session.query( models_alch.Tribe ).filter(
        or_(
            models_alch.Tribe.name.contains( srch_text ),
            ) ).all()
    log.debug( f'qset_tribes, ```{pprint.pformat(qset_tribes)}```' )
    for tribe in qset_tribes:
        log.debug( f'name, ```{tribe.name}```' )
        tribes.append( tribe )
        log.debug( f'tribe_referents, ```{pprint.pformat(tribe.referents)}```' )
        for referent in tribe.referents:
            if referent not in referents:
                referents.append( referent )
    log.debug( f'referents, ```{pprint.pformat(referents)}```' )
    for referent in referents:
        log.debug( f'referent primary_name, ```{referent.primary_name}```' )
        person = referent.person
        log.debug( f'person display_name, ```{person.display_name()}```' )
        if person not in persons:
            persons.append( person )
    log.debug( f'persons, ```{pprint.pformat(persons)}```' )
    return persons


def process_persons( all_persons, session ):
    """ Searches `Person` table.
        Called by run_search() """
    log.debug( f'all_persons before sort, ```{pprint.pformat(all_persons)}```' )
    all_persons.sort( key=lambda prsn: prsn.display_name() )
    log.debug( f'all_persons after sort, ```{pprint.pformat(all_persons)}```' )
    people = []
    for person in all_persons:
        prsn_dct = person.dictify()
        if not prsn_dct['comments']:
            prsn_dct['comments'] = '(None)'
        rfrnts: List[models_alch.Referent] = person.references  # strange-but-true: this yields Referent records
        enslavements = []
        roles = []
        tribes = []
        for rfrnt in rfrnts:
            rfrnt_enslavements = [ e.name for e in rfrnt.enslavements ]
            if rfrnt_enslavements:
                enslavements = list( set(enslavements + rfrnt_enslavements) )
            rfrnt_roles = [ r.name for r in rfrnt.roles ]
            if rfrnt_roles:
                roles = list( set(roles + rfrnt_roles) )
            rfrnt_tribes = [ t.name for t in rfrnt.tribes ]
            if rfrnt_tribes:
                tribes = list( set(tribes + rfrnt_tribes) )
        prsn_dct['enslavements'] = enslavements
        prsn_dct['roles'] = roles
        prsn_dct['tribes'] = tribes
        people.append( prsn_dct )
    people_info = {
        'count': len(people), 'people': people, 'fields_searched': ['first_name', 'last_name', 'comments', 'tribe.name'] }
    log.debug( f'people_info, ```{pprint.pformat( people_info )}```' )
    return people_info


def search_citations( srch_text, session ):
    """ Searches `Citation` table.
        Called by run_search() """
    citations = []
    qset_citations = session.query( models_alch.Citation ).filter(
        or_(
            models_alch.Citation.display.contains( srch_text ),
            models_alch.Citation.comments.contains( srch_text )
            ) ).all()
    for cite in qset_citations:
        cite_dct = cite.dictify()
        if not cite_dct['comments']:
            cite_dct['comments'] = '(None)'
        citations.append( cite_dct )
    citations_info = {
        'count': len(citations), 'citations': citations, 'fields_searched': ['display', 'comments'] }
    log.debug( f'citations_info, ```{pprint.pformat( citations_info )}```' )
    return citations_info


def query_items_via_transcription( srch_text, session  ) -> list:
    """ Searches `Reference` table on transcription.
        Called by run_search() """
    rfrncs = []
    qset_rfrncs = session.query( models_alch.Reference ).filter(
        or_(
            models_alch.Reference.transcription.contains( srch_text ),
            ) ).all()
    for rfrnc in qset_rfrncs:
        rfrncs.append( rfrnc )
    log.debug( f'transcription-references count, ```{len(rfrncs)}```' )
    return rfrncs


def query_items_via_location( srch_text, session  ) -> list:
    """ Searches `ReferenceLocation` table.
        Called by run_search() """
    rfrncs = []
    qset_ref_locations = session.query( models_alch.ReferenceLocation ).all()
    log.debug( f'len(qset_ref_locations), ```{len(qset_ref_locations)}```' )
    for qset_ref_location in qset_ref_locations:
        # log.debug( f'qset_ref_location.__dict__, ```{qset_ref_location.__dict__}```' )
        # log.debug( f'qset_ref_location.location.name, ```{qset_ref_location.location.name}```' )
        # log.debug( f'qset_ref_location.reference, ```{qset_ref_location.reference}```' )
        location_name_lowercase = qset_ref_location.location.name.lower()
        location_type_name = None
        try:
            log.debug( f'qset_ref_location.location_type.name, ```{qset_ref_location.location_type.name}```' )
            location_type_name = qset_ref_location.location_type.name
        except:
            log.exception( 'non-stopping problem with qset_ref_location.location.name, traceback follows, followed by __dict__...' )
            log.debug( f'qset_ref_location.__dict__, ```{qset_ref_location.__dict__}```' )
            pass
        log.debug( f'srch_text, ```{srch_text}```' )
        log.debug( f'location_name_lowercase, ```{location_name_lowercase}```' )
        if srch_text in location_name_lowercase:
            rfrncs.append( qset_ref_location.reference )
    log.debug( f'len(rfrncs), ```{len(rfrncs)}```' )
    return rfrncs


def process_items( all_items, srch_text ) -> list:
    """ Prepares item-display data.
        Called by run_query() """
    # log.debug( f'all_items before sort, ```{pprint.pformat(all_items)}```' )
    rfrncs = []
    for rfrnc in all_items:
        try:
            rfrnc_dct = rfrnc.dictify()
            rfrnc_dct['transcription'] = update_transcription( rfrnc_dct.get('transcription', ''), srch_text )
            rfrncs.append( rfrnc_dct )
        except:
            log.exception( f'problem with reference, ```{rfrnc}```; traceback follows but processing will continue' )  # occasionally a reference in the list is None; TODO- determine why that is.
    rfrncs.sort( key=lambda entry: entry['id'] )
    # log.debug( f'rfrncs after sort, ```{pprint.pformat(rfrncs)}```' )
    rfrncs_info = {
        'count': len(rfrncs), 'references': rfrncs, 'fields_searched': ['transcription (display truncated)', 'location-fields'] }
    log.debug( f'rfrncs_info (first 1000 characters), ```{pprint.pformat( rfrncs_info )[0:1000]}```...' )
    return rfrncs_info


def update_transcription( transcription, srch_text ) -> list:
    """ Replaces transcription with transcription segments.
        Called by process_items() """
    transcription_lowercase = transcription.lower()
    srch_text_lowercase = srch_text.lower()
    extra_characters = 40
    finds = []
    for match in re.finditer( srch_text_lowercase, transcription_lowercase ):
        # log.debug( f'match found: start, ``{match.start()}``; end, ``{match.end()}``' )
        start_slice = (match.start() - extra_characters) if (match.start() - extra_characters) >= 0 else 0
        end_slice = (match.end() + extra_characters) if (match.end() + extra_characters) <= len(transcription) else len(transcription)
        big_slice = f'…{transcription[start_slice: end_slice].strip()}…'
        finds.append( big_slice )
    log.debug( f'finds, ```{pprint.pformat(finds)}```' )
    return finds


# def search_items_by_location( srch_text, session ):
#     """ Searches `Reference` table on location.
#         Called by run_search() """
#     rfrncs = []
#     qset_location_types = session.query( models_alch.LocationType ).all()
#     for qset_location_type in qset_location_types:
#         log.debug( f'qset_location_type.name, ```{qset_location_type.name}```' )
#         """
#         This yields a list of all the collection-type names
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Colony/State```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Location```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Locale```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```City```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Colony```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```State```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Town```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```County```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Region```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Church```
#         [30/Mar/2020 10:18:32] DEBUG [view_search_results_manager-search_items_by_location()::190] qset_location_type.name, ```Ship```
#         """
#     1/0
#     return


# ====================


def experiment():
    session = make_session()

    qset_people = session.query( models_alch.Person ).filter(
        or_(
            models_alch.Person.first_name.contains('Ming'),
            models_alch.Person.last_name.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nPeople...' )
    for x in qset_people:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )

    qset_citations = session.query( models_alch.Citation ).filter(
        or_(
            models_alch.Citation.display.contains('Ming'),
            models_alch.Citation.comments.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nCitations...' )
    for x in qset_citations:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )

    qset_items = session.query( models_alch.Reference ).filter(
        or_(
            models_alch.Reference.transcription.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nItems...' )
    for x in qset_items:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )
