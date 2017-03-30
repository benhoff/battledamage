from sqlalchemy import (create_engine,
                        Column,
                        String,
                        Integer,
                        Float,
                        Boolean,
                        Table,
                        ForeignKey,
                        DateTime)

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from battle_damage.utils import get_sqlite_url


def get_session():
    engine_url = get_sqlite_url()

    engine = create_engine(engine_url)
    # create a configured “Session” class
    Session = sessionmaker(bind=engine, autoflush=False)
    return Session


Base = _declarative_base()


def add_material(name,
                 temper,
                 standard=None,
                 source='MMPDS',
                 **material_properties):

    Session = get_session()
    session = Session()
    material = Material(name=name,
                        temper=temper,
                        standard=standard,
                        source=source,
                        **material_properties)

    session.add(material)
    session.commit(material)

    return material


def add_properties(material_id, **properties):
    property_ = Property(material_id=material_id, **properties)
    session.add(property_)
    session.commit()


class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    temper = Column(String(50))
    standard = Column(String(50))
    # Forged, extruded, etc
    formation = Column(String(50))
    source = Column(String)
    # Maybe not needed?
    description = Column(String)


class Properity(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    bearing_yield = Column(Float)
    bearing_ultimate = Column(Float)
    compressive_yield = Column(Float)
    modulus_elasticiy = Column(Float)
    modulus_elasticity_compressive = Column(Float)
    shear_ultimate = Column(Float)
    tensile_ultimate = Column(Float)
    tensile_yield = Column(Float)
    thickness_lower = Column(Float)
    thickness_upper = Column(Float)


class FastenerType(Base):
    __tablename__ = 'fastener_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Fastener(Base):
    __tablename__ = 'fasteners'
    id = Column(Integer, primary_key=True)
    fastener_type_id = Column(ForeignKey('FastenerType.id'), nullable=False)
    diameter = Column(String)
    # More properties?
