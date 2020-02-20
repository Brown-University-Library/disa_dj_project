# -*- coding: utf-8 -*-

import collections, datetime, json, logging, os, pprint, uuid
import sqlalchemy

from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def denormalize():
    """ Produces denormalized document-based json representing all data entered.
        Called manually for now. """
    log.debug( 'starting json_for_browse()' )
    start_time = datetime.datetime.now()

    session = make_session()

    output = []

    cites = session.query( models_alch.Citation ).all()

    for ( i, cite ) in enumerate( cites):

        # log.debug( f'len( cite.uuid ), ```{len( cite.uuid )}```' )
        # if cite.uuid == None:
        #     log.debug( 'adding uuid' )
        #     cite.uuid = uuid.uuid4().hex
        #     session.add( cite )
        #     session.commit()
        # else:
        #     log.debug( 'found existing uuid' )

        rfrncs = []
        for rfrnc in cite.references:
            rfrnc_dct = {
                'reference_id': rfrnc.id,
                'reference_transcription': rfrnc.transcription,
                }
            rfrncs.append( rfrnc_dct )


        cite_dct = {
            'citation_id': cite.id,
            # 'citation_uuid': cite.uuid,

            'citation_type_id_TEMP': cite.citation_type_id,
            'citation_type_name': cite.citation_type.name,
            'citation_type_zotero_type_id_TEMP': cite.citation_type.zotero_type_id,
            'citation_type_zotero_type_name': cite.citation_type.zotero_type.name,
            'citation_type_zotero_type_creator_name': cite.citation_type.zotero_type.creator_name,

            'citation_display': cite.display,
            'citation_zotero_id': cite.zotero_id,
            'citation_comments': cite.comments,
            'citation_acknowledgements': cite.acknowledgements,
            'citation_references': rfrncs
            }
        output.append( cite_dct )
        if i > 9:
            break

    log.debug( f'output, ```{pprint.pformat(output)}```' )
    return output
