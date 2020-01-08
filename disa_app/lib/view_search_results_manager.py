# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def run_search( srch_text: str ) -> dict:
    session = make_session()
    data = {}

    log.debug( f'srch_text, ```{srch_text}```' )
    log.debug( f'old_usr_db_id, `{old_usr_db_id}`' )

    all_cites = session.query( models_alch.Citation ).all()
    log.debug( f'all_cites (first 10), ```{pprint.pformat(all_cites[0:10])}...```' )

    # no_refs = [
    #     (cite, current_user.id, datetime.datetime.now(), '') for cite in all_cites if len(cite.references) == 0
    #     ]
    no_refs = [
        (cite, old_usr_db_id, datetime.datetime.now(), '') for cite in all_cites if len(cite.references) == 0
        ]
    log.debug( f'no_refs (first 10), ```{pprint.pformat(no_refs[0:10])}...```' )

    has_refs = [ cite for cite in all_cites if len(cite.references) > 0 ]
    log.debug( f'has_refs (first 10), ```{pprint.pformat(has_refs[0:10])}...```' )




    # for ( i, cite ) in enumerate( has_refs):
    #     log.debug( f'cite, `{cite}`' )
    #     log.debug( f'display, ```{cite.display}```' )
    #     log.debug( f'cite.references, ```{cite.references}```' )
    #     for rfrnc in cite.references:
    #         log.debug( f'rfrnc.edits for rfrnc.id `{rfrnc.id}`, ```{rfrnc.edits}```' )
    #     if i > 4:
    #         break
    # 1/0



    wrapped_refs = [ (cite, edit.user_id, edit.timestamp, edit.edited_by.email)
                        for cite in has_refs
                            for ref in cite.references
                                for edit in ref.edits ]
    log.debug( f'wrapped_refs (first 5), ```{pprint.pformat(wrapped_refs[0:5])}...```' )

    # user_cites = [ wrapped for wrapped in wrapped_refs
    #                 if wrapped[1] == current_user.id ]
    user_cites = [ wrapped for wrapped in wrapped_refs
                    if wrapped[1] == old_usr_db_id ]
    log.debug( f'user_cites (first 5), ```{pprint.pformat(user_cites[0:5])}...```' )

    # srtd_all = sort_documents(no_refs + wrapped_refs)
    srtd_all = sort_documents(wrapped_refs)
    log.debug( f'srtd_all (first 5), ```{pprint.pformat(srtd_all[0:5])}...```' )
    log.debug( f'srtd_all count, `{len(srtd_all)}`' )

    srtd_user = sort_documents(user_cites)
    log.debug( f'srtd_user (first 5), ```{pprint.pformat(srtd_user[0:5])}...```' )
    log.debug( f'srtd_user count, `{len(srtd_user)}`' )

    # return render_template(
    #     'document_index.html',
    #     user_documents=srtd_user,
    #     documents=srtd_all
    #     )

    # data['user_documents'] = srtd_user
    # data['documents'] = srtd_all

    # data['user_documents'] = [
    #     {
    #     'date': {'dt_date': 'the-date', 'dt_time': 'the-time'},
    #     'email': 'the-email',
    #     'doc': {'id': 'the-doc-id', 'display': 'the-doc-display', 'reference_count': 1} },
    #     {
    #     'date': {'dt_date': 'the-date2', 'dt_time': 'the-time2'},
    #     'email': 'the-email2',
    #     'doc': {'id': 'the-doc-id2', 'display': 'the-doc-display2', 'reference_count': 2} }
    #     ]

    data['user_documents'] = jsonify_entries( srtd_user[0:10] )
    data['documents'] = jsonify_entries( srtd_all )

    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


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
    pass
    # jsonified_entries = []
    # for entry in doc_list:






## from DISA
# @app.route('/editor', methods=['GET'])
# @login_required
# def editor_index():
#     log.debug( '\n\nstarting editor_index' )
#     all_cites = models.Citation.query.all()
#     log.debug( f'all_cites (first 10), ```{pprint.pformat(all_cites[0:10])}...```' )
#     no_refs = [
#         (cite, current_user.id, datetime.datetime.now(), '') for cite in all_cites if len(cite.references) == 0
#         ]
#     log.debug( f'no_refs (first 10), ```{pprint.pformat(no_refs[0:10])}...```' )
#     has_refs = [ cite for cite in all_cites if len(cite.references) > 0 ]
#     log.debug( f'has_refs (first 10), ```{pprint.pformat(has_refs[0:10])}...```' )
#     wrapped_refs = [ (cite, edit.user_id, edit.timestamp, edit.edited_by.email)
#                         for cite in has_refs
#                             for ref in cite.references
#                                 for edit in ref.edits ]
#     log.debug( f'wrapped_refs (first 20), ```{pprint.pformat(wrapped_refs[0:20])}...```' )
#     user_cites = [ wrapped for wrapped in wrapped_refs
#                     if wrapped[1] == current_user.id ]
#     log.debug( f'user_cites (first 10), ```{pprint.pformat(user_cites[0:10])}...```' )

#     # srtd_all = sort_documents(no_refs + wrapped_refs)
#     srtd_all = sort_documents(wrapped_refs)
#     log.debug( f'srtd_all (first 10), ```{pprint.pformat(srtd_all[0:10])}...```' )

#     srtd_user = sort_documents(user_cites)
#     log.debug( f'srtd_user (first 10), ```{pprint.pformat(srtd_user[0:10])}...```' )
#     return render_template(
#         'document_index.html',
#         user_documents=srtd_user,
#         documents=srtd_all
#         )
