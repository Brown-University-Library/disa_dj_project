"""
Manages sqlalchemy setup and queries.

Resources...
- <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
- <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>
"""

import logging
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


log = logging.getLogger(__name__)
Base = declarative_base()



# ==========
# RDF-ish
# ==========


has_role = Table('6_has_role',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('role', Integer, ForeignKey('1_roles.id'))
)


has_race = Table('6_has_race',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('referent', Integer, ForeignKey('5_referents.id')),
    Column('race', Integer, ForeignKey('1_races.id'))
)


class Person(Base):
    __tablename__ = '1_people'

    id = Column( Integer, primary_key=True )
    first_name = Column( String(255) )
    last_name = Column( String(255) )
    comments = Column( String(255) )
    # references = relationship( 'Referent', backref='person', lazy=True )

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
    # primary_name = relationship('ReferentName',
    #     primaryjoin=(primary_name_id == 'ReferentName.id'),
    #     post_update=True )
    # roles = relationship('Role',
    #     secondary='has_role', back_populates='referents')
    # tribes = relationship('Tribe',
    #     secondary='has_tribe', back_populates='referents')
    races = relationship('Race',
        secondary=has_race, back_populates='referents')
    # titles = relationship('Title',
    #     secondary='has_title', back_populates='referents')
    # vocations = relationship('Vocation',
    #     secondary='has_vocation', back_populates='referents')
    # origins = relationship('Location',
    #     secondary='has_origin', back_populates='origin_for')
    # enslavements = relationship('EnslavementType',
    #     secondary='enslaved_as', back_populates='referents')

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


class ReferentName(Base):
    __tablename__ = '6_referent_names'

    id = Column(Integer, primary_key=True)
    referent_id = Column(Integer, ForeignKey('5_referents.id'))
    name_type_id = Column(Integer, ForeignKey('1_name_types.id'))
    first = Column(String(255))
    last = Column(String(255))
    # name_type = relationship('NameType',
    #     primaryjoin=(name_type_id == 'NameType.id') )


class Race(Base):
    __tablename__ = '1_races'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship('Referent',
        secondary=has_race, back_populates='races')


# # ==========
# # RDF-ish
# # ==========


# has_role = Table('6_has_role',
#     Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('referent', Integer, ForeignKey('5_referents.id')),
#     Column('role', Integer, ForeignKey('1_roles.id'))
# )


# has_race = Table('6_has_race',
#     Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('referent', Integer, ForeignKey('5_referents.id')),
#     Column('race', Integer, ForeignKey('1_races.id'))
# )

