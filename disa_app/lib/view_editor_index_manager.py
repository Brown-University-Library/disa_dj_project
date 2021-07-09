# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from disa_app.models import MarkedForDeletion


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def query_documents( username: str, old_usr_db_id: int ) -> dict:
    """ Queries and massages data.
        Called by views.editor_index() """
    log.debug( f'username, ``{username}``; old_usr_db_id, ``{old_usr_db_id}``' )
    marked = MarkedForDeletion.objects.all()
    marked_ids = []
    all_cites = []
    session = make_session()
    cites_result_set = session.query( models_alch.Citation ).all()
    if marked:
        for entry in marked:
            marked_ids.append( entry.old_db_id )
        for cite in cites_result_set:
            if cite.id not in marked_ids:
                all_cites.append( cite )
            else:
                log.debug( f'skipping site, ``{cite}``' )
    else:
        all_cites = cites_result_set

    data = {}
    log.debug( f'type(all_cites), ``{type(all_cites)}``')
    no_refs = [ (cite, old_usr_db_id, datetime.datetime.now(), '')
        for cite in all_cites if len(cite.references) == 0 ]
    has_refs = [ cite
        for cite in all_cites if len(cite.references) > 0 ]
    wrapped_refs = make_wrapped_refs( has_refs )
    user_cites = [ wrapped
        for wrapped in wrapped_refs if wrapped[1] == old_usr_db_id ]
    srtd_all = sort_documents( wrapped_refs )  # was ```srtd_all = sort_documents(no_refs + wrapped_refs)```
    srtd_user = sort_documents( user_cites )
    data['user_documents'] = jsonify_entries( srtd_user[0:10] )
    data['documents'] = jsonify_entries( srtd_all )
    log.debug( f'data (first 1K chars), ```{pprint.pformat(data)[0:1000]}...```' )
    return data


def make_wrapped_refs( has_refs ):
    """ Takes list of citation-objects,
        Returns list of tuples, with each tuple comprised of a citation-object, the (last?) editor-id, the (last?) editor-timestamp, and the (last?) editor-email.
        Making this into a function instead of a list comprehension for clarity.
        Called by query_documents() """
    # wrapped_refs = [ (cite, edit.user_id, edit.timestamp, edit.edited_by.email)
    #                     for cite in has_refs
    #                         for ref in cite.references
    #                             for edit in ref.edits ]
    wrapped_refs = []
    for cite in has_refs:
        for ref in cite.references:
            for edit in ref.edits:
                try:
                    email = edit.edited_by.email
                except:
                    log.warning( 'email unavailable' )
                    email = 'not_available'
                wrapped_refs.append( (cite, edit.user_id, edit.timestamp, email) )
    log.debug( f'wrapped_refs (first 5) of `{len(wrapped_refs)}`, ```{pprint.pformat(wrapped_refs[0:5])}...```' )
    return wrapped_refs


def sort_documents( wrappedDocs ) -> list:
    """ Sorts documents.
        Called by query_documents() """
    log.debug( f'before sort (first 5), ```{pprint.pformat(wrappedDocs[0:5])}```...' )
    merge = {}
    for w in wrappedDocs:
        if w[0].id not in merge or merge[w[0].id][0] < w[2]:
            merge[w[0].id] = (w[2], w[3], w[0])
        else:
            continue
    sorted_docs = sorted([ merge[w] for w in merge], reverse=True)
    log.debug( f'after sort (first 5), ```{pprint.pformat(sorted_docs[0:5])}```...' )
    return sorted_docs


def jsonify_entries( doc_list ) -> list:
    """ Converts data elements into json-compatible data-structures.
        Called by query_documents() """
    jsonified_entries = []
    for entry in doc_list:
        ( date, email, citation_obj ) = ( entry[0], entry[1], entry[2] )
        dtstr_date = date.strftime( '%Y-%m-%d')
        dtstr_time = date.strftime( '%I:%M %p' )
        entry_dct = {
            'date': {'dt_date': dtstr_date, 'dt_time': dtstr_time},
            'email': email,
            'doc': {'id': citation_obj.id, 'display': citation_obj.display, 'reference_count': len(citation_obj.references) }
            }
        jsonified_entries.append( entry_dct )
    log.debug( f'jsonified_entries (first 3), ```{pprint.pformat(jsonified_entries[0:3])}```' )
    return jsonified_entries


## for reference -- accessing edits (was in query_documents() above)

    # for ( i, cite ) in enumerate( has_refs):
    #     log.debug( f'cite, `{cite}`' )
    #     log.debug( f'display, ```{cite.display}```' )
    #     log.debug( f'cite.references, ```{cite.references}```' )
    #     for rfrnc in cite.references:
    #         log.debug( f'rfrnc.edits for rfrnc.id `{rfrnc.id}`, ```{rfrnc.edits}```' )
    #     if i > 4:
    #         break
    # 1/0
