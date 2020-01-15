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
CITATION_TYPES = [
    'Book',
    'Book Section',
    'Document',
    'Interview',
    'Journal Article',
    'Magazine Article',
    'Manuscript',
    'Newspaper Article',
    'Thesis',
    'Webpage' ]


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def query_document( doc_id: str, old_usr_db_id: int ) -> dict:
    """ Queries and massages data.
        Called by views.read_document_data() """
    session = make_session()
    data = { 'doc': {} }
    included: list = CITATION_TYPES
    # ct = models.CitationType.query.filter( models.CitationType.name.in_(included) ).all()
    ct = session.query( models_alch.CitationType ).filter( models_alch.CitationType.name.in_(included) ).all()
    log.debug( f'ct, ```{ct}```' )
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]




    if doc_id == None:
        log.debug( f'returning data for docID equals None, ```{pprint.pformat(data)}```' )
        return jsonify(data)
    if doc_id == 'copy':

        # last_edit = edit = models.ReferenceEdit.query.filter_by(
        #     user_id=current_user.id).order_by(
        #     models.ReferenceEdit.timestamp.desc()).first()

        last_edit = edit = session.query( models_alch.ReferenceEdit ).filter_by( user_id=old_usr_db_id ).order_by( models_alch.ReferenceEdit.timestamp.desc() ).first()
        log.debug( f'last_edit, ```{last_edit}```' )



        if not last_edit or not last_edit.edited:
            log.debug( f'returning data for docID equals copy with no last_edit, ```{pprint.pformat(data)}```' )
            return jsonify(data)
        # doc = models.Citation.query.get(last_edit.edited.citation_id)
        doc = session.query( models_alch.Citation ).get( last_edit.edited.citation_id )
        log.debug( f'doc, ```{doc}```' )
    else:
        doc = models.Citation.query.get(doc_id)
        data['doc']['id'] = doc.id
    data['doc']['citation'] = doc.display
    # data['doc']['zotero_id'] = doc.zotero_id
    data['doc']['comments'] = doc.comments
    data['doc']['acknowledgements'] = doc.acknowledgements
    if doc.citation_type_id not in [ c.id for c in ct ]:
        doctype_document = [ c for c in ct if c.name == 'Document'][0]
        data['doc']['citation_type_id'] = doctype_document.id
    else:
        data['doc']['citation_type_id'] = doc.citation_type_id
    data['doc']['fields'] = { f.field.name: f.field_data for f in doc.citation_data }
    log.debug( f'returning data for given docID, ```{pprint.pformat(data)}```' )




    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


## from DISA
# @app.route('/data/documents/', methods=['GET'])
# @app.route('/data/documents/<docId>', methods=['GET'])
# @login_required
# def read_document_data(docId=None):
#     log.debug( f'starting "data/documents/" GET processing; docId, `{docId}`' )
#     data = { 'doc': {} }
#     included = [ 'Book', 'Book Section', 'Document', 'Interview',
#         'Journal Article', 'Magazine Article', 'Manuscript',
#         'Newspaper Article', 'Thesis', 'Webpage' ]
#     ct = models.CitationType.query.filter(
#         models.CitationType.name.in_(included)).all()
#     log.debug( f'ct, ```{ct}```' )
#     data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
#     if docId == None:
#         log.debug( f'returning data for docID equals None, ```{pprint.pformat(data)}```' )
#         return jsonify(data)
#     if docId == 'copy':
#         last_edit = edit = models.ReferenceEdit.query.filter_by(
#             user_id=current_user.id).order_by(
#             models.ReferenceEdit.timestamp.desc()).first()
#         log.debug( f'last_edit, ```{last_edit}```' )
#         if not last_edit or not last_edit.edited:
#             log.debug( f'returning data for docID equals copy with no last_edit, ```{pprint.pformat(data)}```' )
#             return jsonify(data)
#         doc = models.Citation.query.get(last_edit.edited.citation_id)
#     else:
#         doc = models.Citation.query.get(docId)
#         data['doc']['id'] = doc.id
#     data['doc']['citation'] = doc.display
#     # data['doc']['zotero_id'] = doc.zotero_id
#     data['doc']['comments'] = doc.comments
#     data['doc']['acknowledgements'] = doc.acknowledgements
#     if doc.citation_type_id not in [ c.id for c in ct ]:
#         doctype_document = [ c for c in ct if c.name == 'Document'][0]
#         data['doc']['citation_type_id'] = doctype_document.id
#     else:
#         data['doc']['citation_type_id'] = doc.citation_type_id
#     data['doc']['fields'] = { f.field.name: f.field_data for f in doc.citation_data }
#     log.debug( f'returning data for given docID, ```{pprint.pformat(data)}```' )
#     return jsonify(data)
