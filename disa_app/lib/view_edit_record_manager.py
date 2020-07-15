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


def prep_doc_id_context( doc_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
    """ Preps context for record_edit.html template when a doc_id (meaning a `Citation` id) is included.
        Called by views.edit_record() """
    log.debug( 'starting prep_doc_id_context()' )
    log.debug( f'doc_id, ``{doc_id}``' )
    context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
    session = make_session()
    common_data: dict = prepare_common_data( session )
    context.update( common_data )  # merges common_data key-vals into context
    doc = session.query( models_alch.Citation ).get( doc_id )
    log.debug( f'doc, ``{pprint.pformat(doc.__dict__)}``' )
    context['rec_id'] = None
    try:
        context['doc_display'] = doc.display
    except:
        log.exception( 'doc.display not available; traceback follows; processing will continue' )
        context['doc_display'] = 'display not available'
    context['doc_id'] = doc.id
    log.debug( f'context (first 1000 characters), ``{pprint.pformat(context)[0:1000]}``' )
    return context


# def prep_doc_id_context( doc_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
#     """ Preps context for template when a doc_id (meaning a `Citation` id) is included.
#         Called by views.edit_record() """
#     context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
#     session = make_session()
#     common_data: dict = prepare_common_data( session )
#     context.update( common_data )  # merges common_data key-vals into context
#     doc = session.query( models_alch.Citation ).get( doc_id )
#     context['rec_id'] = None
#     context['doc_display'] = doc.display
#     context['doc_id'] = doc.id
#     log.debug( 'context prepared' )
#     return context


def prep_rec_id_context( rec_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
    """ Preps context for record_edit.html template when a rec_id (meaning a `Reference` id) is included.
        Called by views.edit_record() """
    log.debug( 'starting prep_rec_id_context()' )
    context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
    session = make_session()
    common_data: dict = prepare_common_data( session )
    context.update( common_data )  # merges common_data key-vals into context
    rec = session.query( models_alch.Reference ).get( rec_id )
    context['rec_id'] = rec.id
    context['doc_display'] = rec.citation.display
    context['doc_id'] = rec.citation.id
    log.debug( f'context (first 1000 characters), ``{pprint.pformat(context)[0:1000]}``' )
    return context


def prepare_common_data( session: sqlalchemy.orm.session.Session ):
    """ Prepares data used for both the rec_id and doc_id calls.
        Called by prep_rec_id_context() and prep_doc_id_context() """
    log.debug( 'starting prepare_common_data()' )

    locs = session.query( models_alch.ReferenceLocation ).all()

    ref_types = session.query( models_alch.ReferenceType ).all()
    rec_types_list = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name } for rt in ref_types ]
    rec_types_json = json.dumps( rec_types_list )

    all_roles = session.query( models_alch.Role ).all()
    roles_list = [ { 'id': role.id, 'value': role.name, 'name': role.name } for role in all_roles ]
    roles_json = json.dumps( roles_list )

    all_ntl_contexts = session.query( models_alch.NationalContext ).all()
    natl_ctxs_list = [ { 'id': nc.id, 'value': nc.name, 'name': nc.name } for nc in all_ntl_contexts ]
    natl_ctxs_json = json.dumps( natl_ctxs_list )

    uniq_locs = uniq_cols = { (l.location.name, l.location_id) for l in locs if l.location_rank == 0 }  # i think `uniq_cols` was a typo.
    uniq_town = { (l.location.name, l.location_id) for l in locs if l.location_rank == 1 }
    uniq_addl = { (l.location.name, l.location_id) for l in locs if l.location_rank == 2 and l.location_id is not None}

    col_state_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_cols ]  # again, typo?
    col_state_json = json.dumps( col_state_list )

    towns_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_town ]
    towns_json = json.dumps( towns_list )

    addl_loc_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_addl ]
    addl_loc_json = json.dumps( addl_loc_list )

    data = {
        'rec_types_list': rec_types_list,   # not used in template; for possible viewing convenience
        'rec_types': rec_types_json,
        'roles_list': roles_list,           # not used; for reference
        'roles': roles_json,
        'natl_ctxs_list': natl_ctxs_list,   # not used; for reference
        'natl_ctxs': natl_ctxs_json,
        'col_state_list': col_state_list,   # not used; for reference
        'col_state': col_state_json,
        'towns_list': towns_list,           # not used; for reference
        'towns': towns_json,
        'addl_loc_list': addl_loc_list,     # not used; for reference
        'addl_loc': addl_loc_json,
        }

    log.debug( 'data prepared' )
    return data

    ## end def prepare_common_data




# def prep_rec_id_context( rec_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
#     """ Preps context for template when a rec_id (meaning a `Reference` id) is included.
#         Called by views.edit_record() """
#     context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
#     session = make_session()

#     locs = session.query( models_alch.ReferenceLocation ).all()

#     ref_types = session.query( models_alch.ReferenceType ).all()
#     rec_types_list = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name } for rt in ref_types ]
#     rec_types_json = json.dumps( rec_types_list )

#     all_roles = session.query( models_alch.Role ).all()
#     roles_list = [ { 'id': role.id, 'value': role.name, 'name': role.name } for role in all_roles ]
#     roles_json = json.dumps( roles_list )

#     all_ntl_contexts = session.query( models_alch.NationalContext ).all()
#     natl_ctxs_list = [ { 'id': nc.id, 'value': nc.name, 'name': nc.name } for nc in all_ntl_contexts ]
#     natl_ctxs_json = json.dumps( natl_ctxs_list )

#     # uniq_cols = { (l.location.name, l.location_id) for l in locs if l.location_rank == 0 }
#     uniq_locs = uniq_cols = { (l.location.name, l.location_id) for l in locs if l.location_rank == 0 }  # i think `uniq_cols` was a typo.

#     uniq_town = { (l.location.name, l.location_id) for l in locs if l.location_rank == 1 }

#     uniq_addl = { (l.location.name, l.location_id) for l in locs if l.location_rank == 2 and l.location_id is not None}

#     col_state_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_cols ]  # again, typo?
#     col_state_json = json.dumps( col_state_list )

#     towns_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_town ]
#     towns_json = json.dumps( towns_list )

#     addl_loc_list = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_addl ]
#     addl_loc_json = json.dumps( addl_loc_list )

#     rec = session.query( models_alch.Reference ).get( rec_id )

#     log.debug( 'data obtained' )

#     context['rec_id'] = rec.id

#     context['doc_display'] = rec.citation.display
#     context['doc_id'] = rec.citation.id

#     context['rec_types_list'] = rec_types_list  # not used; for reference
#     context['rec_types'] = rec_types_json

#     context['roles_list'] = roles_list  # not used; for reference
#     context['roles'] = roles_json

#     context['natl_ctxs_list'] = natl_ctxs_list  # not used; for reference
#     context['natl_ctxs'] = natl_ctxs_json

#     context['col_state_list'] = col_state_list  # not used; for reference
#     context['col_state'] = col_state_json

#     context['towns_list'] = towns_list
#     context['towns'] = towns_json

#     context['addl_loc_list'] = addl_loc_list
#     context['addl_loc'] = addl_loc_json

#     log.debug( 'context prepared' )
#     return context

#     ## end prep_rec_id_context()



## from DISA
# @app.route('/editor/records')
# @app.route('/editor/records/<recId>')
# @login_required
# def edit_record(recId=None):
#     log.debug( 'starting edit_record' )
#     locs = models.ReferenceLocation.query.all()
#     rec_types = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
#         for rt in models.ReferenceType.query.all() ]
#     roles = [ { 'id': role.id, 'value': role.name, 'name': role.name }
#         for role in models.Role.query.all() ]
#     natl_ctxs = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
#         for rt in models.NationalContext.query.all() ]
#     uniq_cols = { (l.location.name, l.location_id)
#         for l in locs if l.location_rank == 0 }
#     uniq_town = { (l.location.name, l.location_id)
#         for l in locs if l.location_rank == 1 }
#     uniq_addl = { (l.location.name, l.location_id)
#         for l in locs if l.location_rank == 2 and l.location_id is not None}
#     col_state = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
#         for loc in uniq_cols ]
#     towns = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
#         for loc in uniq_town ]
#     addl_loc = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
#         for loc in uniq_addl ]
#     if not recId:
#         doc_id = request.args.get('doc')
#         doc = models.Citation.query.get(doc_id)
#         return render_template(
#             'record_edit.html',  rec=None, doc=doc,
#             rec_types=rec_types, roles=roles,
#             natl_ctxs=natl_ctxs, col_state=col_state,
#             towns=towns, addl_loc=addl_loc)
#     rec = models.Reference.query.get(recId)
#     return render_template(
#         'record_edit.html', rec=rec, doc=rec.citation,
#             rec_types=rec_types, roles=roles,
#             natl_ctxs=natl_ctxs, col_state=col_state,
#             towns=towns, addl_loc=addl_loc)
