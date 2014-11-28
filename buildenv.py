#!/usr/bin/env python

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String


# Create the SQLEngine object
db = create_engine('sqlite:///:memory:', echo=True)


def create_base_classes():
    base = declarative_base()

    class Champion(base):
        __tablename__ = 'champions'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        abbreviations = Column('names', postgresql.ARRAY(String))

        def __repr__(self):
            return "<Champion(name='%s', abbreviations='%s')>" % (self.name, self.abbreviations)

    base.metadata.create_all(db)

if __name__ == "__main__":
    create_base_classes()