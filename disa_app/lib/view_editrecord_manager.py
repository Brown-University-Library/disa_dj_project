# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import sqlalchemy
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


def prep_context( rec_id ):
    context = {}
    session = make_session()

    locs = session.query( models_alch.ReferenceLocation ).all()

    ref_types = session.query( models_alch.ReferenceType ).all()
    rec_types = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name } for rt in ref_types ]

    all_roles = session.query( models_alch.Role ).all()
    roles = [ { 'id': role.id, 'value': role.name, 'name': role.name } for role in all_roles ]

    all_ntl_contexts = session.query( models_alch.NationalContext ).all()
    natl_ctxs = [ { 'id': nc.id, 'value': nc.name, 'name': nc.name } for nc in all_ntl_contexts ]

    # uniq_cols = { (l.location.name, l.location_id) for l in locs if l.location_rank == 0 }
    uniq_locs = uniq_cols = { (l.location.name, l.location_id) for l in locs if l.location_rank == 0 }  # i think `uniq_cols` was a typo.

    uniq_town = { (l.location.name, l.location_id) for l in locs if l.location_rank == 1 }

    uniq_addl = { (l.location.name, l.location_id) for l in locs if l.location_rank == 2 and l.location_id is not None}

    col_state = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_cols ]  # again, typo?

    towns = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_town ]

    addl_loc = [ {'id': loc[1], 'value': loc[0],'label': loc[0] } for loc in uniq_addl ]

    rec = session.query( models_alch.Reference ).get( rec_id )

    log.debug( 'data obtained' )

    context['rec_id'] = rec.id

    context['doc_display'] = rec.citation.display
    context['doc_id'] = rec.citation.id

    context['rec_types'] = rec_types

    context['roles'] = roles

    context['natl_ctxs'] = natl_ctxs

    context['col_state'] = col_state

    context['towns'] = towns

    context['addl_loc'] = addl_loc

    log.debug( f'context, ```{pprint.pformat(context)}```' )
    return context



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
