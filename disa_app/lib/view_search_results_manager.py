# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def run_search( srch_text: str ) -> dict:
    """ Queries people, citations, and items for search-text.
        Called by views.search_results() """
    log.debug( f'srch_text, ```{srch_text}```' )
    session = make_session()
    data = {}

    people_results = search_people( srch_text, session )
    citation_results = search_citations( srch_text, session )
    item_results = search_items( srch_text, session )

    data = {
        'people_results': people_results, 'citation_results': citation_results, 'item_results': item_results }

    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


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
        rfrncs = person.references
        log.debug( f'type(rfrncs), ```{type(rfrncs)}```' )
        enslavements = []
        for rfrnc in rfrncs:
            rfrnc_enslavements = [ e.name for e in rfrnc.enslavements ]
            if rfrnc_enslavements:
                # enslavements.append( rfrnc_enslavements )
                enslavements = list( set(enslavements + rfrnc_enslavements) )
        prsn_dct['enslavements'] = enslavements
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
#         people.append( person.dictify() )
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
        citations.append( cite.dictify() )
    citations_info = {
        'count': len(citations), 'citations': citations, 'fields_searched': ['display', 'comments'] }
    log.debug( f'citations_info, ```{pprint.pformat( citations_info )}```' )
    return citations_info


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


# experiment()
