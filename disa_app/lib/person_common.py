# -*- coding: utf-8 -*-

import collections, datetime, json, logging, os, pprint

import sqlalchemy
# from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from django.urls import reverse
# from django.conf import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def parse_person_name( prsn ) -> str:
    """ Returns display-name.
        Called by view_person_manager.query_person() """
    name: str = f'{prsn.first_name} {prsn.last_name}'.strip()
    if name == '':
        name = 'Not Listed'
    return name


def parse_person_descriptors( prsn, dscrptr ) -> str:
    """ Returns Referent descriptor value.
        Called by view_person_manager.query_person() """
    log.debug( f'person-id, `{prsn.id}`; descriptor, `{dscrptr}`' )
    vals = { desc.name for ref in prsn.references for desc in getattr(ref, dscrptr) }
    log.debug( f'vals, ```{vals}```' )
    out = ', '.join(list(vals))
    return out if out else 'Not Listed'


def parse_person_relations( prsn: models_alch.Referent ) -> list:
    """ Returns a list of relationship entries, each consisting of an id and name, and the relationship type.
        Called by view_person_manager.query_person() """
    rels = [ (r.related_as, r.obj) for e in prsn.references
                for r in e.as_subject ]
    grouped = collections.defaultdict( list )
    for r in rels:
        grouped[ r[0].name_as_relationship ].append( {
            'id': r[1].person_id,
            'name': parse_person_name(r[1].person)
            } )
    calc_rels = [ { 'type': k, 'related': v } for k,v in grouped.items() ]
    log.debug( f'calc_rels, ```{pprint.pformat(calc_rels)}```' )
    return calc_rels


def parse_person_references( prsn ) -> list:
    """ Returns Referent and Reference information for a Person.
        Called by view_person_manager.query_person()
        Reminder: A Person-record is a human.
                  A Referent-record is a bridge between a Person-record and a Reference-record.
                  A Reference-record contains transcription and some other info, and an id to a Citation-record.
        NOTE: prsn.references returns a list of Referent-objects, _not_ Reference-objects.
              To get reference data, we need to call the `referent-record.reference`.
        """
    rfrnts: sqlalchemy.orm.collections.InstrumentedList = prsn.references
    log.debug( f'type(rfrnts), ```{type( prsn.references )}```' )
    log.debug( f'rfrnts, ```{prsn.references}```' )
    j_rfrnts = []
    for rfrnt in rfrnts:  # ref: Referent
        data = {}
        data['rfrnc_display_date']: str = rfrnt.reference.display_date()
        rfnrt_role_names = []
        for role in rfrnt.roles:
            rfnrt_role_names.append( role.name )
        data['rfnrt_role_names'] = rfnrt_role_names  # TODO: change key to 'rfrnt_role_names'
        rfrnc_locations_names = []
        for location in rfrnt.reference.locations:
            rfrnc_locations_names.append( location.location.name )
        rfrnc_locations_names.reverse()
        data['rfrnc_location_names'] = rfrnc_locations_names
        data['rfrnc_id'] = rfrnt.reference.id
        source_item_segment = f'{rfrnt.reference.citation_id}/#/{rfrnt.reference.id}'
        # data['source_and_item_url'] = reverse( 'redesign_citation_url', kwargs={'cite_id': source_item_segment} )
        buffer_source_and_item_url = reverse( 'redesign_citation_url', kwargs={'cite_id': 'STUB'} )
        log.debug( f'buffer_source_and_item_url, ``{buffer_source_and_item_url}``' )
        source_and_item_url = buffer_source_and_item_url.replace( 'STUB', source_item_segment )
        log.debug( f'source_and_item_url, ``{source_and_item_url}``' )
        data['source_and_item_url'] = source_and_item_url
        j_rfrnts.append( data )
    log.debug( f'j_rfrnts, ```{pprint.pformat(j_rfrnts)}```' )
    return j_rfrnts

    # redirect_url = reverse( 'edit_record_w_recid_url', kwargs={'rec_id': src_id} )


# def parse_person_references( prsn ) -> list:
#     """ Returns Referent and Reference information for a Person.
#         Called by view_person_manager.query_person()
#         Reminder: A Person-record is a human.
#                   A Referent-record is a bridge between a Person-record and a Reference-record.
#                   A Reference-record contains transcription and some other info, and an id to a Citation-record.
#         NOTE: prsn.references returns a list of Referent-objects, _not_ Reference-objects.
#               To get reference data, we need to call the `referent-record.reference`.
#         """
#     rfrnts: sqlalchemy.orm.collections.InstrumentedList = prsn.references
#     log.debug( f'type(rfrnts), ```{type( prsn.references )}```' )
#     log.debug( f'rfrnts, ```{prsn.references}```' )
#     j_rfrnts = []
#     for rfrnt in rfrnts:  # ref: Referent
#         data = {}
#         data['rfrnc_display_date']: str = rfrnt.reference.display_date()
#         rfnrt_role_names = []
#         for role in rfrnt.roles:
#             rfnrt_role_names.append( role.name )
#         data['rfnrt_role_names'] = rfnrt_role_names  # TODO: change key to 'rfrnt_role_names'
#         rfrnc_locations_names = []
#         for location in rfrnt.reference.locations:
#             rfrnc_locations_names.append( location.location.name )
#         rfrnc_locations_names.reverse()
#         data['rfrnc_location_names'] = rfrnc_locations_names
#         data['rfrnc_id'] = rfrnt.reference.id
#         j_rfrnts.append( data )
#     log.debug( f'j_rfrnts, ```{pprint.pformat(j_rfrnts)}```' )
#     return j_rfrnts
