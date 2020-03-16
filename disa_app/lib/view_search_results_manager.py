# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

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


# def run_search( srch_text: str, start_time: datetime.datetime ) -> dict:
#     """ Queries people, citations, and items for search-text.
#         Called by views.search_results() """
#     log.debug( f'srch_text, ```{srch_text}```' )
#     session = make_session()
#     data = {}
#     people_results = search_people( srch_text, session )
#     citation_results = search_citations( srch_text, session )
#     item_results = search_items( srch_text, session )
#     data = {
#         'people_results': people_results,
#         'citation_results': citation_results,
#         'item_results': item_results,
#         'search_query': srch_text,
#         'time_taken': str( datetime.datetime.now() - start_time )
#         }
#     log.debug( f'data, ```{pprint.pformat(data)}```' )
#     return data


def run_search( srch_text: str, start_time: datetime.datetime ) -> dict:
    """ Queries people, citations, and items for search-text.
        Called by views.search_results() """
    log.debug( f'srch_text, ```{srch_text}```' )
    session = make_session()

    cache_key = srch_text
    query_results: dict = cache.get( cache_key )
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
    people_results = search_people( srch_text, session )
    citation_results = search_citations( srch_text, session )
    item_results = search_items( srch_text, session )
    query_dct = {
        'people_results': people_results, 'citation_results': citation_results, 'item_results': item_results }
    log.debug( 'returning query_dct' )
    return query_dct


## caching example
# def grab_z3950_data( self, key, value, show_marc_param ):
#     """ Returns data from cache if available; otherwise calls sierra.
#         Called by build_data_dct() """
#     cache_key = '%s_%s' % (key, value)
#     pickled_data = cache.get( cache_key )
#     if pickled_data is None:
#         log.debug( 'pickled_data was not in cache' )
#         pickled_data = self.query_josiah( key, value, show_marc_param )
#         cache.set( cache_key, pickled_data )  # time could be last argument; defaults to settings.py entry
#     else:
#         log.debug( 'pickled_data was in cache' )
#     return pickled_data


def search_people( srch_text, session ):
    """ Searches `Person` table.
        Called by run_search() """
    people = []
    qset_people = session.query( models_alch.Person ).filter(
        or_(
            models_alch.Person.first_name.contains( srch_text ),
            models_alch.Person.last_name.contains( srch_text ),
            models_alch.Person.comments.contains( srch_text )
            ) ).all()
    for person in qset_people:
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
        'count': len(people), 'people': people, 'fields_searched': ['first_name', 'last_name', 'comments'] }
    log.debug( f'people_info, ```{pprint.pformat( people_info )}```' )
    return people_info


# def search_people( srch_text, session ):
#     """ Searches `Person` table.
#         Called by run_search() """
#     people = []
#     qset_people = session.query( models_alch.Person ).filter(
#         or_(
#             models_alch.Person.first_name.contains( srch_text ),
#             models_alch.Person.last_name.contains( srch_text ),
#             models_alch.Person.comments.contains( srch_text )
#             ) ).all()
#     for person in qset_people:
#         prsn_dct = person.dictify()
#         if not prsn_dct['comments']:
#             prsn_dct['comments'] = '(None)'
#         rfrnts: List[models_alch.Referent] = person.references  # strange-but-true: this yields Referent records
#         enslavements = []
#         roles = []
#         for rfrnt in rfrnts:
#             rfrnt_enslavements = [ e.name for e in rfrnt.enslavements ]
#             if rfrnt_enslavements:
#                 enslavements = list( set(enslavements + rfrnt_enslavements) )
#             rfrnt_roles = [ r.name for r in rfrnt.roles ]
#             if rfrnt_roles:
#                 roles = list( set(roles + rfrnt_roles) )
#         prsn_dct['enslavements'] = enslavements
#         prsn_dct['roles'] = roles
#         people.append( prsn_dct )
#     people_info = {
#         'count': len(people), 'people': people, 'fields_searched': ['first_name', 'last_name', 'comments'] }
#     log.debug( f'people_info, ```{pprint.pformat( people_info )}```' )
#     return people_info


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

# def search_citations( srch_text, session ):
#     """ Searches `Citation` table.
#         Called by run_search() """
#     citations = []
#     qset_citations = session.query( models_alch.Citation ).filter(
#         or_(
#             models_alch.Citation.display.contains( srch_text ),
#             models_alch.Citation.comments.contains( srch_text )
#             ) ).all()
#     for cite in qset_citations:
#         citations.append( cite.dictify() )
#     citations_info = {
#         'count': len(citations), 'citations': citations, 'fields_searched': ['display', 'comments'] }
#     log.debug( f'citations_info, ```{pprint.pformat( citations_info )}```' )
#     return citations_info


def search_items( srch_text, session ):
    """ Searches `Reference` table.
        Called by run_search() """
    rfrncs = []
    qset_rfrncs = session.query( models_alch.Reference ).filter(
        or_(
            models_alch.Reference.transcription.contains( srch_text ),
            ) ).all()
    for rfrnc in qset_rfrncs:
        rfrncs.append( rfrnc.dictify() )
    rfrncs_info = {
        'count': len(rfrncs), 'references': rfrncs, 'fields_searched': ['transcription'] }
    log.debug( f'rfrncs_info, ```{pprint.pformat( rfrncs_info )}```' )
    return rfrncs_info



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
