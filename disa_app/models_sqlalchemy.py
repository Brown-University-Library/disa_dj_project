"""
Manages sqlalchemy setup and queries.

Resources...
- <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
- <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>
"""

import logging
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UnicodeText
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.orm import backref


log = logging.getLogger(__name__)
Base = declarative_base()



# ==========
# RDF-ish
# ==========


citationtype_referencetypes = Table('3_citationtype_referencetypes',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('citation_type', Integer, ForeignKey('2_citation_types.id')),
    Column('reference_type', Integer, ForeignKey('1_reference_types.id')),
)


enslaved_as = Table('6_enslaved_as',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('enslavement', Integer, ForeignKey('1_enslavement_types.id'))
)

has_origin = Table('6_has_origin',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('origin', Integer, ForeignKey('1_locations.id'))
)


has_race = Table('6_has_race',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('race', Integer, ForeignKey('1_races.id'))
)


has_role = Table('6_has_role',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('role', Integer, ForeignKey('1_roles.id'))
)


has_title = Table('6_has_title',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('title', Integer, ForeignKey('1_titles.id'))
)


has_tribe = Table('6_has_tribe',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('tribe', Integer, ForeignKey('1_tribes.id'))
)


has_vocation = Table('6_has_vocation',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('vocation', Integer, ForeignKey('1_vocations.id'))
)


referencetype_roles = Table('2_referencetype_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('reference_type', Integer, ForeignKey('1_reference_types.id')),
    Column('role', Integer, ForeignKey('1_roles.id'))
)


# ==========
# models
# ==========



class Citation(Base):
    __tablename__ = '3_citations'

    id = Column(Integer, primary_key=True)
    citation_type_id = Column(Integer, ForeignKey('2_citation_types.id'),
        nullable=False)
    display = Column(String(500))
    zotero_id = Column(String(255))
    comments = Column(UnicodeText())
    acknowledgements = Column(String(255))
    references = relationship('Reference', backref='citation', lazy=True)

    def __repr__(self):
        return '<Citation {0}>'.format(self.id)

class CitationType(Base):
    __tablename__ = '2_citation_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    zotero_type_id = Column(Integer, ForeignKey('1_zotero_types.id'),
        nullable=False)
    reference_types = relationship(
        'ReferenceType', secondary=citationtype_referencetypes,
        back_populates='citation_types')
    citations = relationship('Citation',
        backref='citation_type', lazy=True)


class Reference(Base):
    __tablename__ = '4_references'

    id = Column(Integer, primary_key=True)
    citation_id = Column(Integer, ForeignKey('3_citations.id'),
        nullable=False)
    reference_type_id = Column(Integer, ForeignKey('1_reference_types.id'),
        nullable=False)
    national_context_id = Column(Integer, ForeignKey('1_national_context.id'),
        nullable=False)
    date = Column(DateTime())
    transcription = Column(UnicodeText())
    referents = relationship(
        'Referent', backref='reference', lazy=True, cascade="delete")

    def last_edit(self):
        edits = sorted([ (e.timestamp, e) for e in self.edits ],
             key=operator.itemgetter(0), reverse=True)
        return edits[0][1]

    def display_date(self):
        if self.date:
            return self.date.strftime('%Y %B %d')
        else:
            return ''

    def __repr__(self):
        return '<Reference {0}>'.format(self.id)

    ## end class ReferenceType


class ReferenceType(Base):
    __tablename__ = '1_reference_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    references = relationship('Reference',
        backref='reference_type', lazy=True)
    roles = relationship(
        'Role', secondary=referencetype_roles,
        back_populates='reference_types')
    citation_types = relationship(
        'CitationType', secondary=citationtype_referencetypes,
        back_populates='reference_types')


class Location(Base):
    __tablename__ = '1_locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    origin_for = relationship('Referent',
        secondary=has_origin, back_populates='origins')

    def __repr__(self):
        return '<Location {0}: {1}>'.format(self.id, self.name)




class ReferenceLocation(Base):
    __tablename__ = '5_has_location'

    id = Column(Integer, primary_key=True)
    reference_id = Column(Integer, ForeignKey('4_references.id'))
    location_id = Column(Integer, ForeignKey('1_locations.id'))
    location_type_id = Column(Integer, ForeignKey('1_location_types.id'))
    location_rank = Column(Integer)
    reference = relationship(Reference,
        primaryjoin=(reference_id == Reference.id),
        backref='locations')
    location = relationship(Location,
        primaryjoin=(location_id == Location.id),
        backref='references')




class Person(Base):
    __tablename__ = '1_people'

    id = Column( Integer, primary_key=True )
    first_name = Column( String(255) )
    last_name = Column( String(255) )
    comments = Column( String(255) )
    references = relationship( 'Referent', backref='person', lazy=True )

    @classmethod
    def filter_on_description( cls, desc ):
        return cls.query.join(
            cls.references).join(Referent.roles).filter(Role.name==desc)

    def display_name( self ):
        display = "{0} {1}".format(
            self.first_name, self.last_name).strip()
        if display == "":
            return "Unknown"
        else:
            return display

    def display_attr( self, attr ):
        vals = { desc.name for ref in self.references
            for desc in getattr(ref, attr) }
        return ', '.join(list(vals))

    ## end class Person


class NationalContext(Base):
    __tablename__ = '1_national_context'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    references = relationship('Reference', backref='national_context', lazy=True)


class ReferentName(Base):
    __tablename__ = '6_referent_names'

    id = Column(Integer, primary_key=True)
    referent_id = Column(Integer, ForeignKey('5_referents.id'))
    name_type_id = Column(Integer, ForeignKey('1_name_types.id'))
    first = Column(String(255))
    last = Column(String(255))
    # name_type = relationship('NameType',
    #     primaryjoin=(name_type_id == 'NameType.id') )


class Referent(Base):
    __tablename__ = '5_referents'

    id = Column(Integer, primary_key=True)
    age = Column(String(255))
    sex = Column(String(255))
    primary_name_id = Column(Integer,
        ForeignKey('6_referent_names.id'),
        nullable=True)
    reference_id = Column(Integer, ForeignKey('4_references.id'),
        nullable=False)
    person_id = Column(Integer, ForeignKey('1_people.id'),
        nullable=True)
    # names = relationship('ReferentName',
    #     primaryjoin=(id == 'ReferentName.referent_id'),
    #     backref='referent', cascade='delete')
    primary_name = relationship(
        'ReferentName',
        primaryjoin=(primary_name_id == ReferentName.id),
        post_update=True )
    roles = relationship(
        'Role',
        secondary=has_role,
        back_populates='referents' )
    tribes = relationship(
        'Tribe',
        secondary=has_tribe,
        back_populates='referents' )
    races = relationship(
        'Race',
        secondary=has_race,
        back_populates='referents')
    titles = relationship('Title',
        secondary=has_title, back_populates='referents')
    vocations = relationship('Vocation',
        secondary=has_vocation, back_populates='referents')
    origins = relationship('Location',
        secondary=has_origin, back_populates='origin_for')
    enslavements = relationship('EnslavementType',
        secondary=enslaved_as, back_populates='referents')

    def __repr__(self):
        return '<Referent {0}: {1}>'.format(
            self.id, self.display_name() )

    def display_name(self):
        display = "{0} {1}".format(
            self.primary_name.first, self.primary_name.last).strip()
        if display == "":
            return "Unknown"
        else:
            return display

    ## end class Referent


class Title(Base):
    __tablename__ = '1_titles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship('Referent',
        secondary=has_title, back_populates='titles')


class Race(Base):
    __tablename__ = '1_races'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship(
        'Referent',
        secondary=has_race,
        back_populates='races' )


class Vocation(Base):
    __tablename__ = '1_vocations'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship('Referent',
        secondary=has_vocation, back_populates='vocations')


class EnslavementType(Base):
    __tablename__ = '1_enslavement_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship(
        'Referent',
        secondary=enslaved_as,
        back_populates='enslavements' )


class Role(Base):
    __tablename__ = '1_roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    name_as_relationship = Column(String(255))
    referents = relationship(
        'Referent',
        secondary=has_role,
        back_populates='roles' )
    reference_types = relationship(
        'ReferenceType',
        secondary=referencetype_roles,
        back_populates='roles' )


class ReferentRelationship(Base):
    __tablename__ = '6_referent_relationships'

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('5_referents.id'))
    object_id = Column(Integer, ForeignKey('5_referents.id'))
    role_id = Column(Integer, ForeignKey('1_roles.id'))
    sbj = relationship(Referent,
        primaryjoin=(subject_id == Referent.id),
        backref=backref('as_subject', cascade='delete'))
    obj = relationship(Referent,
        primaryjoin=(object_id == Referent.id),
        backref=backref('as_object', cascade='delete'))
    related_as = relationship(Role,
        primaryjoin=(role_id == Role.id),
        backref='describes')

    def entailed_relationships(self):
        implied = []
        entailed = RoleRelationship.query.filter_by(role1=self.role_id).all()
        for e in entailed:
            implied.append(e.entail_relationships(
                self.subject_id, self.object_id))
        return implied


class Tribe(Base):
    __tablename__ = '1_tribes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship(
        'Referent',
        secondary=has_tribe,
        back_populates='tribes' )

