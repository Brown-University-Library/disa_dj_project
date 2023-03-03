# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from disa_app.lib import person_common
from disa_app.models import MarkedForDeletion
from django.conf import settings
from django.urls import reverse
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


def manage_get( doc_id: str, user_id: int ) -> dict:
    """ Queries and massages data for given doc_id.
        Called by views.data_documents() on GET """
    assert type(doc_id) == str; assert type(user_id) == int
    session = make_session()
    data = { 'doc': {} }
    included: list = CITATION_TYPES
    # ct = models.CitationType.query.filter( models.CitationType.name.in_(included) ).all()
    ct = session.query( models_alch.CitationType ).filter( models_alch.CitationType.name.in_(included) ).all()
    log.debug( f'ct, ```{ct}```' )
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]

    # if doc_id == None:
    #     log.debug( f'returning data for docID equals None, ```{pprint.pformat(data)}```' )
    #     return jsonify(data)

    if doc_id == 'copy':

        last_edit = edit = session.query( models_alch.ReferenceEdit ).filter_by( user_id=user_id ).order_by( models_alch.ReferenceEdit.timestamp.desc() ).first()
        log.debug( f'last_edit, ```{last_edit}```' )

        if not last_edit or not last_edit.edited:
            log.debug( f'returning data for docID equals copy with no last_edit, ```{pprint.pformat(data)}```' )
            return jsonify(data)
        doc = session.query( models_alch.Citation ).get( last_edit.edited.citation_id )
        log.debug( f'doc, ```{doc}```' )
    else:
        doc = session.query( models_alch.Citation ).get( doc_id )
        if doc == None:
            log.debug( 'citation query not found' )
            return 'not_found'
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

    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data

    ## end def manage_get()


def manage_get_all( user_id: int ) -> dict:
    """ Queries and massages data for new-document.
        Called by views.data_documents() on GET, with no doc_id.
        2021-April-27: i don't think this is being used. """
    log.debug( f'\n\nstarting manage_get_all()' )
    session = make_session()
    data = { 'doc': {} }
    included: list = CITATION_TYPES
    # ct = models.CitationType.query.filter( models.CitationType.name.in_(included) ).all()
    ct = session.query( models_alch.CitationType ).filter( models_alch.CitationType.name.in_(included) ).all()
    log.debug( f'ct, ```{ct}```' )
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


def manage_put( cite_id: str, user_id: int, payload: bytes ) -> dict:
    """ Updates document.
        Called by views.data_documents() on PUT """
    assert type(cite_id) == str; assert type(user_id) == int; assert type(payload) == bytes
    session = make_session()
    return_data = {}

    try:
        # data: dict = json.loads( payload )
        incoming_data: dict = json.loads( payload )
        log.debug( f'incoming_data (from payload), ``{pprint.pformat(incoming_data)}``' )
    except:
        log.exception( 'problem parsing payload; error will be returned' )
        # return '400 / Bad Request'
        return { 'err': '400 / Bad Request' }

    try:  # temp; remove after debugging
        import copy
        data_to_process: dict = copy.deepcopy( incoming_data )
        unspec = session.query( models_alch.CitationType ).filter_by( name='Document' ).first()

        data_to_process['citation_type_id'] = incoming_data['citation_type_id'] or unspec.id

        cite = session.query( models_alch.Citation ).get( cite_id )

        cite.citation_type_id = data_to_process['citation_type_id']
        # doc.zotero_id = data['zotero_id']
        cite.comments = incoming_data['comments']
        cite.acknowledgements = incoming_data['acknowledgements']
        field_order_map = { f.zotero_field.name: f.rank
            for f in cite.citation_type.zotero_type.template_fields }
        citation_display = []
        cite.citation_data = []
        addendums = []
        for field, val in incoming_data['fields'].items():
            if val == '':
                continue

            zfield = session.query( models_alch.ZoteroField ).filter_by( name=field ).first()

            cfield = models_alch.CitationField(citation_id=cite.id,
                field_id=zfield.id, field_data=val)
            try:
                citation_display.append( (field_order_map[zfield.name], val) )
            except KeyError:
                addendums.append(val)
            session.add(cfield)
        if len(citation_display) == 0:
            now = datetime.datetime.utcnow()
            cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
        else:
            vals = [ v[1] for v in sorted(citation_display) ]
            cite.display = ', '.join(vals + addendums)
        session.add( cite )
        session.commit()

        # data = { 'doc': {} }
        return_data: dict = { 'doc': {}, 'doc_types': [] }

        included = [ 
            'Book', 'Book Section', 'Document', 'Interview',
            'Journal Article', 'Magazine Article', 'Manuscript',
            'Newspaper Article', 'Thesis', 'Webpage' ]

        ct = session.query( models_alch.CitationType ).filter( models_alch.CitationType.name.in_(included) ).all()

        return_data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]

        doc_dct: dict = { 
            'id': cite_id,
            'citation': cite.display,
            'comments': cite.comments,
            'acknowledgements': cite.acknowledgements,
            'citation_type_id': cite.citation_type_id
        }

        return_data['doc'] = doc_dct
        log.debug( f'return_data, ```{pprint.pformat(return_data)}```' )

    except:
        log.exception( 'problem on api PUT; traceback follows...' )
    return return_data

    ## end def manage_put()


# def manage_put( cite_id: str, user_id: int, payload: bytes ):
#     """ Updates document.
#         Called by views.data_documents() on PUT """
#     assert type(cite_id) == str; assert type(user_id) == int; assert type(payload) == bytes
#     session = make_session()

#     try:
#         data: dict = json.loads( payload )
#         log.debug( f'data (from payload), ``{pprint.pformat(data)}``' )
#     except:
#         log.exception( 'problem parsing payload; error will be returned' )
#         return '400 / Bad Request'

#     try:  # temp; remove after debugging
#         unspec = session.query( models_alch.CitationType ).filter_by( name='Document' ).first()

#         data['citation_type_id'] = data['citation_type_id'] or unspec.id

#         cite = session.query( models_alch.Citation ).get( cite_id )

#         cite.citation_type_id = data['citation_type_id']
#         # doc.zotero_id = data['zotero_id']
#         cite.comments = data['comments']
#         cite.acknowledgements = data['acknowledgements']
#         field_order_map = { f.zotero_field.name: f.rank
#             for f in cite.citation_type.zotero_type.template_fields }
#         citation_display = []
#         cite.citation_data = []
#         addendums = []
#         for field, val in data['fields'].items():
#             if val == '':
#                 continue

#             zfield = session.query( models_alch.ZoteroField ).filter_by( name=field ).first()

#             cfield = models_alch.CitationField(citation_id=cite.id,
#                 field_id=zfield.id, field_data=val)
#             try:
#                 citation_display.append( (field_order_map[zfield.name], val) )
#             except KeyError:
#                 addendums.append(val)
#             session.add(cfield)
#         if len(citation_display) == 0:
#             now = datetime.datetime.utcnow()
#             cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
#         else:
#             vals = [ v[1] for v in sorted(citation_display) ]
#             cite.display = ', '.join(vals + addendums)
#         session.add( cite )
#         session.commit()

#         data = { 'doc': {} }
#         included = [ 'Book', 'Book Section', 'Document', 'Interview',
#             'Journal Article', 'Magazine Article', 'Manuscript',
#             'Newspaper Article', 'Thesis', 'Webpage' ]

#         ct = session.query( models_alch.CitationType ).filter( models_alch.CitationType.name.in_(included) ).all()

#         data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
#         data['doc']['id'] = cite.id
#         data['doc']['citation'] = cite.display
#         # data['doc']['zotero_id'] = doc.zotero_id
#         data['doc']['comments'] = cite.comments
#         data['doc']['acknowledgements'] = cite.acknowledgements
#         data['doc']['citation_type_id'] = cite.citation_type_id
#         log.debug( f'data, ```{pprint.pformat(data)}```' )

#     except:
#         log.exception( 'problem on api PUT; traceback follows...' )
#     log.debug( f'data (put-context), ``{pprint.pformat(data)}``' )
#     return data

#     ## end def manage_put()


def manage_post( user_id, payload ):
    """ Updates document.
        Called by views.data_documents() on POST """
    log.debug( 'starting manage_post()' )
    assert type(user_id) == int; assert type(payload) == bytes
    log.debug( f'user_id, ``{user_id}``' )
    log.debug( f'payload, ``{payload}``' )

    try:  # temp; remove after debugging

        session = make_session()
        data: dict = json.loads( payload )
        log.debug( f'data, ``{pprint.pformat(data)}``' )

        log.debug( f'initial data["citation_type_id"], ``{data["citation_type_id"]}``' )

        unspec = session.query( models_alch.CitationType ).filter_by( name='Document' ).first()
        data['citation_type_id'] = data['citation_type_id'] or unspec.id

        log.debug( f'unspec.id, ``{unspec.id}``')
        log.debug( f'final data["citation_type_id"], ``{data["citation_type_id"]}``' )

        cite = models_alch.Citation(
            citation_type_id=data['citation_type_id'],
            comments=data['comments'],
            acknowledgements=data['acknowledgements']
            )
        session.add(cite)  # this creates the citation in mysql
        session.commit()
        log.debug( 'citation-obj added to mysql' )

        field_order_map = { f.zotero_field.name: f.rank
            for f in cite.citation_type.zotero_type.template_fields }

        citation_display = []
        for field, val in data['fields'].items():
            if val == '':
                continue

            # zfield = models.ZoteroField.query.filter_by(name=field).first()
            zfield = session.query( models_alch.ZoteroField ).filter_by( name=field ).first()

            # cfield = models.CitationField(citation_id=cite.id,
            #     field_id=zfield.id, field_data=val)
            cfield = models_alch.CitationField(
                citation_id=cite.id,
                field_id=zfield.id,
                field_data=val )

            citation_display.append( (field_order_map[zfield.name], val) )
            session.add(cfield)

        log.debug( f'initial citation_display, ``{citation_display}``' )
        if len(citation_display) == 0:
            now = datetime.datetime.utcnow()
            cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
        else:
            vals = [ v[1] for v in sorted(citation_display) ]
            cite.display = ' '.join(vals)
        log.debug( f'final citation_display, ``{citation_display}``' )

        session.add(cite)  # I assume this simply updates the existing citation in mysql
        session.commit()

        # context = { 'redirect': reverse( 'edit_citation_url', kwargs={'cite_id': cite.id} ) }
        context = { 'redirect': reverse( 'redesign_citation_url', kwargs={'cite_id': cite.id} ) }

    except:
        log.exception( 'problem on api POST; traceback follows; processing will continue.' )
        context = 'error'

    log.debug( f'context, ```{context}```' )
    return context

    ## end def manage_post()


def manage_delete( doc_id, user_uuid_str, user_email ):
    """ Adds mark-for-deletion entry to django-db table.
        Called by: views.data_documents() when request.method is 'DELETE'. """
    log.debug( f'doc_id, ``{doc_id}``; user_uuid_str, ``{user_uuid_str}``; user_email, ``{user_email}``' )
    assert type(doc_id) == str
    assert type(user_uuid_str) == str
    assert type(user_email) == str
    context = None

    ## build citation_jsn for storage
    try:
        session = make_session()
        log.debug( f'session, ``{session}``' )
        citation_result = session.query( models_alch.Citation ).get( doc_id )
        log.debug( f'citation_result, ``{citation_result}``' )
        citaton_dct = citation_result.dictify()
        log.debug( f'citaton_dct, ``{citaton_dct}``' )
        citation_jsn = json.dumps( citaton_dct, sort_keys=True, indent=2 )
        log.debug( f'citation_jsn, ``{citation_jsn}``' )
    except:
        log.exception( 'problem getting citation json; traceback follows; returning error-message' )
        context = '500 / Server Error'

    ## build user_jsn for storage
    if context == None:
        try:
            usr_dct = { 'user_uuid': user_uuid_str, 'user_email': user_email }
            user_jsn = json.dumps( usr_dct, sort_keys=True, indent=2 )
        except:
            log.exception( 'problem getting user json; traceback follows; returning error-message' )
            context = '500 / Server Error'

    ## save the citation_jsn and user_jsn to the marked-for-deletion entry
    if context == None:
        try:
            log.debug( 'saving markedfordeletion_entry' )
            markedfordeletion_entry = MarkedForDeletion(
                old_db_id=doc_id,
                doc_json_data=citation_jsn,
                patron_json_data=user_jsn )
            markedfordeletion_entry.save()
            context = { 'marked_for_deletion_result': 'success' }
            log.debug( 'markedfordeletion_entry save successful' )
        except:
            log.exception( 'problem saving markedfordeletion_entry; traceback follows; eturning error-message' )
            context = '500 / Server Error'
    log.debug( f'context, ``{context}``' )
    return context

# def manage_delete( doc_id, user_id ):
#     """ Adds mark-for-deletion entry to django-db table.
#         Called by: views.data_documents() when request.method is 'DELETE'. """
#     log.debug( f'doc_id, ``{doc_id}``' )
#     markedfordeletion_entry = MarkedForDeletion( old_db_id=doc_id )
#     markedfordeletion_entry.save()
#     # context = { 'status': 'foo' }
#     # log.debug( f'context, ``{context}``' )
#     # return context
#     return


# ----------------
# for reference...
# ----------------


## from DISA -- GET
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


## from DISA -- PUT
# @app.route('/data/documents/', methods=['PUT'])
# @app.route('/data/documents/<citeId>', methods=['PUT'])
# @login_required
# def update_citation_data(citeId):
#     data = request.get_json()
#     if citeId is None:
#         return jsonify({})
#     unspec = models.CitationType.query.filter_by(name='Document').first()
#     data['citation_type_id'] = data['citation_type_id'] or unspec.id
#     cite = models.Citation.query.get(citeId)
#     cite.citation_type_id = data['citation_type_id']
#     # doc.zotero_id = data['zotero_id']
#     cite.comments = data['comments']
#     cite.acknowledgements = data['acknowledgements']
#     field_order_map = { f.zotero_field.name: f.rank
#         for f in cite.citation_type.zotero_type.template_fields }
#     citation_display = []
#     cite.citation_data = []
#     addendums = []
#     for field, val in data['fields'].items():
#         if val == '':
#             continue
#         zfield = models.ZoteroField.query.filter_by(name=field).first()
#         cfield = models.CitationField(citation_id=cite.id,
#             field_id=zfield.id, field_data=val)
#         try:
#             citation_display.append( (field_order_map[zfield.name], val) )
#         except KeyError:
#             addendums.append(val)
#         db.session.add(cfield)
#     if len(citation_display) == 0:
#         now = datetime.datetime.utcnow()
#         cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
#     else:
#         vals = [ v[1] for v in sorted(citation_display) ]
#         cite.display = ', '.join(vals + addendums)
#     db.session.add(cite)
#     db.session.commit()

#     data = { 'doc': {} }
#     included = [ 'Book', 'Book Section', 'Document', 'Interview',
#         'Journal Article', 'Magazine Article', 'Manuscript',
#         'Newspaper Article', 'Thesis', 'Webpage' ]
#     ct = models.CitationType.query.filter(
#         models.CitationType.name.in_(included)).all()
#     data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
#     data['doc']['id'] = cite.id
#     data['doc']['citation'] = cite.display
#     # data['doc']['zotero_id'] = doc.zotero_id
#     data['doc']['comments'] = cite.comments
#     data['doc']['acknowledgements'] = cite.acknowledgements
#     data['doc']['citation_type_id'] = cite.citation_type_id
#     return jsonify(data)


# @app.route('/data/documents/', methods=['POST'])
# @login_required
# def create_citation():
#     data = request.get_json()
#     unspec = models.CitationType.query.filter_by(name='Document').first()
#     data['citation_type_id'] = data['citation_type_id'] or unspec.id
#     cite = models.Citation(citation_type_id=data['citation_type_id'],
#         comments=data['comments'], acknowledgements=data['acknowledgements'])
#     db.session.add(cite)
#     db.session.commit()
#     field_order_map = { f.zotero_field.name: f.rank
#         for f in cite.citation_type.zotero_type.template_fields }
#     citation_display = []
#     for field, val in data['fields'].items():
#         if val == '':
#             continue
#         zfield = models.ZoteroField.query.filter_by(name=field).first()
#         cfield = models.CitationField(citation_id=cite.id,
#             field_id=zfield.id, field_data=val)
#         citation_display.append( (field_order_map[zfield.name], val) )
#         db.session.add(cfield)
#     if len(citation_display) == 0:
#         now = datetime.datetime.utcnow()
#         cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
#     else:
#         vals = [ v[1] for v in sorted(citation_display) ]
#         cite.display = ' '.join(vals)
#     db.session.add(cite)
#     db.session.commit()
#     return jsonify(
#         { 'redirect': url_for('edit_citation', citeId=cite.id) })
