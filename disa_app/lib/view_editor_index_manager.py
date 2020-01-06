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


def query_documents( username: str ) -> dict:
    session = make_session()
    data = {}

    log.debug( f'username, ```{username}```' )

    all_cites = session.query( models_alch.Citation ).all()
    log.debug( f'all_cites (first 10), ```{pprint.pformat(all_cites[0:10])}...```' )

    no_refs = [
        (cite, current_user.id, datetime.datetime.now(), '') for cite in all_cites if len(cite.references) == 0
        ]
    log.debug( f'no_refs (first 10), ```{pprint.pformat(no_refs[0:10])}...```' )

    has_refs = [ cite for cite in all_cites if len(cite.references) > 0 ]
    log.debug( f'has_refs (first 10), ```{pprint.pformat(has_refs[0:10])}...```' )

    wrapped_refs = [ (cite, edit.user_id, edit.timestamp, edit.edited_by.email)
                        for cite in has_refs
                            for ref in cite.references
                                for edit in ref.edits ]
    log.debug( f'wrapped_refs (first 20), ```{pprint.pformat(wrapped_refs[0:20])}...```' )

    user_cites = [ wrapped for wrapped in wrapped_refs
                    if wrapped[1] == current_user.id ]
    log.debug( f'user_cites (first 10), ```{pprint.pformat(user_cites[0:10])}...```' )

    # srtd_all = sort_documents(no_refs + wrapped_refs)
    srtd_all = sort_documents(wrapped_refs)
    log.debug( f'srtd_all (first 10), ```{pprint.pformat(srtd_all[0:10])}...```' )

    srtd_user = sort_documents(user_cites)
    log.debug( f'srtd_user (first 10), ```{pprint.pformat(srtd_user[0:10])}...```' )

    # return render_template(
    #     'document_index.html',
    #     user_documents=srtd_user,
    #     documents=srtd_all
    #     )

    data['user_documents'] = srtd_user

    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data



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
