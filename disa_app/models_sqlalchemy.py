"""
Manages sqlalchemy setup and queries.

Resources...
- <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
- <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>
"""

import logging
from typing import List

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


log = logging.getLogger(__name__)


# engine = create_engine( settings_app.DB_URL, echo=True )
Base = declarative_base()
# Session = sessionmaker(bind = engine)
# session = Session()


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

    # resultset: List(sqlalchemy.util._collections.result) = session.query(
    #     Person.id, Person.first_name, Person.last_name, Person.comments ).all()

    # log.debug( f'type(resultset), `{type(resultset)}`' )

    # j_resultset: List(dict) = [ dict( zip(row.keys(), row) ) for row in resultset ]
    # log.debug( f'j_resultset, ```{pprint.pformat(j_resultset)}```' )



