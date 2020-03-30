"""
Manages sqlalchemy setup and queries.

Resources...
- <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
- <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>
"""

import datetime, logging, operator, pprint
from typing import List

import sqlalchemy
from disa_app import settings_app
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UnicodeText
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)
Base = declarative_base()


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


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

    # uuid = Column( String(32) )

    citation_type_id = Column(Integer, ForeignKey('2_citation_types.id'),
        nullable=False)
    display = Column(String(500))
    zotero_id = Column(String(255))
    comments = Column(UnicodeText())
    acknowledgements = Column(String(255))
    references = relationship('Reference', backref='citation', lazy=True)

    def dictify( self ):
        jsn_references = []
        for rfrnc in self.references:
            jsn_references.append( rfrnc.dictify() )
        data = {
            'id': self.id,
            'citation_type_id': self.citation_type_id,
            'display': self.display,
            'zotero_id': self.zotero_id,
            'comments': self.comments,
            'references': jsn_references
            }
        return data

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


class ZoteroType(Base):
    __tablename__ = '1_zotero_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    creator_name = Column(String(255))
    citation_types = relationship('CitationType',
        backref='zotero_type', lazy=True)


class ZoteroField(Base):
    __tablename__ = '1_zotero_fields'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    display_name = Column(String(255))


class ZoteroTypeField(Base):
    __tablename__ = '2_zoterotype_fields'

    id = Column(Integer, primary_key=True)
    zotero_type_id = Column(Integer, ForeignKey('1_zotero_types.id'))
    zotero_field_id = Column(Integer, ForeignKey('1_zotero_fields.id'))
    rank = Column(Integer)
    zotero_type = relationship(ZoteroType,
        primaryjoin=(zotero_type_id == ZoteroType.id),
        backref='template_fields')
    zotero_field = relationship(ZoteroField,
        primaryjoin=(zotero_field_id == ZoteroField.id),
        backref='templates')


class CitationField(Base):
    __tablename__ = '4_citation_fields'

    id = Column(Integer, primary_key=True)
    citation_id = Column(Integer, ForeignKey('3_citations.id'))
    field_id = Column(Integer, ForeignKey('1_zotero_fields.id'))
    field_data = Column(String(255))
    citation = relationship(Citation,
        primaryjoin=(citation_id == Citation.id),
        backref='citation_data')
    field = relationship(ZoteroField,
        primaryjoin=(field_id == ZoteroField.id),
        backref='citations')


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
        edits: List(tuple) = sorted([ (e.timestamp, e) for e in self.edits ],
             key=operator.itemgetter(0), reverse=True)
        log.debug( f'edits, ```{edits}```' )
        if edits:
            return_edits = edits[0][1]
        else:
            return_edits = []
        return return_edits

    def display_date(self):
        if self.date:
            return self.date.strftime('%Y %B %d')
        else:
            return ''

    def dictify( self ):
        if self.date:
            isodate = datetime.date.isoformat( self.date )
        else:
            isodate = ''
        jsn_referents = []
        for rfrnt in self.referents:
            jsn_referents.append( {'id': rfrnt.id, 'age': rfrnt.age, 'sex': rfrnt.sex} )
        last_edit = self.last_edit()
        if last_edit:
            last_edit = last_edit.timestamp.strftime( '%Y-%m-%d' )
        data = {
            'id': self.id,
            'citation_id': self.citation_id,
            'reference_type_id': self.reference_type_id,
            'reference_type_name': self.reference_type.name,  # NB: this appears to be an sqlalchemy convention -- that if there is a ForeignKey, I can just go ahead and refernce the property name.
            'national_context_id': self.national_context_id,
            'date': isodate,
            'transcription': self.transcription,
            'referents': jsn_referents,
            'last_edit': last_edit
            }
        return data

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

    def dictify( self ):
        data = {
            'id': self.id,
            'name': self.name
            }
        return data


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


class LocationType(Base):
    __tablename__ = '1_location_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    locations = relationship( ReferenceLocation,
        backref='location_type', lazy=True )


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

    def dictify( self ):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'comments': self.comments,
            }
        return data

    def __repr__(self):
        display_repr = f'<Person {self.id}: {self.display_name()}>'
        return display_repr

    # def __repr__(self):
    #     return '<Referent {0}: {1}>'.format(
    #         self.id, self.display_name() )

    ## end class Person


class NationalContext(Base):
    __tablename__ = '1_national_context'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    references = relationship('Reference', backref='national_context', lazy=True)


class NameType(Base):
    __tablename__ = '1_name_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))  # eg 'Enlgish', 'European', 'Indian', 'Given', etc


class ReferentName(Base):
    __tablename__ = '6_referent_names'

    id = Column(Integer, primary_key=True)
    referent_id = Column(Integer, ForeignKey('5_referents.id'))
    name_type_id = Column(Integer, ForeignKey('1_name_types.id'))
    first = Column(String(255))
    last = Column(String(255))
    name_type = relationship(
        'NameType',
        primaryjoin=(name_type_id == NameType.id) )


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
    names = relationship(
        'ReferentName',
        primaryjoin=(id == ReferentName.referent_id),
        backref='referent',
        cascade='delete')
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
        session = make_session()
        implied = []
        # entailed = RoleRelationship.query.filter_by(role1=self.role_id).all()
        entailed = session.query( RoleRelationship ).filter_by(role1=self.role_id).all()

        for e in entailed:
            implied.append(e.entail_relationships(
                self.subject_id, self.object_id))
        return implied




class RoleRelationship(Base):
    __tablename__ = '2_role_relationships'

    id = Column(Integer, primary_key=True)
    role1 = Column(Integer, ForeignKey('1_roles.id'))
    role2 = Column(Integer, ForeignKey('1_roles.id'))
    relationship_type = Column(Integer,
        ForeignKey('1_role_relationship_types.id'))
    alternate_text = Column(String(255))

    def entail_role(self):
        pass

    def entail_relationships(self, sbjId, objId):
        if self.related_as.name == 'inverse':
            return ReferentRelationship(
                subject_id=objId, role_id=self.role2, object_id=sbjId)
        elif self.related_as.name == 'is_a':
            return ReferentRelationship(
                subject_id=sbjId, role_id=self.role2, object_id=objId)
        else:
            return

class RoleRelationshipType(Base):
    __tablename__ = '1_role_relationship_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    relationships = relationship(
        'RoleRelationship', backref='related_as', lazy=True)







class Tribe(Base):
    __tablename__ = '1_tribes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    referents = relationship(
        'Referent',
        secondary=has_tribe,
        back_populates='tribes' )




class User(Base):
    __tablename__ = '1_users'

    id = Column(Integer, primary_key=True)
    role = Column(String(64))
    name = Column(String(64))
    email = Column(String(120))
    created = Column(DateTime())
    last_login = Column(DateTime())
    password_hash = Column(String(128))

    # def set_password(self, password):
    #     self.password_hash = security.generate_password_hash(password)

    # def check_password(self, password):
    #     try:
    #         return security.check_password_hash(self.password_hash, password)
    #     except:
    #         return None


# class User(UserMixin, db.Model):
#     __tablename__ = '1_users'

#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String(64))
#     name = db.Column(db.String(64))
#     email = db.Column(db.String(120))
#     created = db.Column(db.DateTime())
#     last_login = db.Column(db.DateTime())
#     password_hash = db.Column(db.String(128))

#     def set_password(self, password):
#         self.password_hash = security.generate_password_hash(password)

#     def check_password(self, password):
#         try:
#             return security.check_password_hash(self.password_hash, password)
#         except:
#             return None


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))




class ReferenceEdit(Base):
    __tablename__ = '5_reference_edits'

    id = Column(Integer, primary_key=True)
    reference_id = Column(Integer, ForeignKey('4_references.id'))
    user_id = Column(Integer, ForeignKey('1_users.id'))
    timestamp = Column(DateTime())
    edited = relationship(Reference,
        primaryjoin=(reference_id == Reference.id),
        backref='edits')
    edited_by = relationship(User,
        primaryjoin=(user_id == User.id),
        backref='edits')

# class ReferenceEdit(db.Model):
#     __tablename__ = '5_reference_edits'

#     id = db.Column(db.Integer, primary_key=True)
#     reference_id = db.Column(db.Integer, db.ForeignKey('4_references.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('1_users.id'))
#     timestamp = db.Column(db.DateTime())
#     edited = db.relationship(Reference,
#         primaryjoin=(reference_id == Reference.id),
#         backref='edits')
#     edited_by = db.relationship(User,
#         primaryjoin=(user_id == User.id),
#         backref='edits')
