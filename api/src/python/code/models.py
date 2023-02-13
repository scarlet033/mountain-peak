from sqlalchemy import Text, Integer, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography

Base = declarative_base()


class MountainPeakModel(Base):
    __tablename__ = "mountain_peak"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)  
    name = Column(Text, nullable=False, unique=True)
    altitude = Column(Float, nullable=False)  
    lat = Column(Float, nullable=False)  
    lon = Column(Float, nullable=False)
    geom = Column(Geography(geometry_type='POINT', srid=4326))