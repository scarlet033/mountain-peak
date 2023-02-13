import threading
import logging

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc, asc, select, update, insert, delete, tuple_, and_
from code import context
from code.schemas import MountainPeak, MountainPeakFull
from code.models import MountainPeakModel
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, InternalError
from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction

_the_sessionmaker = None
_engine = None

class ST_GeographyFromText(GenericFunction):
    name = 'ST_GeographyFromText'
    type = Geometry

def get_engine():
    global _engine

    if _engine is None:
        with threading.Lock():
            if _engine is None:
                _engine = create_engine(
                    context.DB_URL,
                    echo=context.DB_SQLALCHEMY_ECHO,
                    pool_pre_ping=True)
    return _engine


def get_session():
    global _the_sessionmaker
    if _the_sessionmaker is None:
        with threading.Lock():
            if _the_sessionmaker is None:
                get_engine()
                _the_sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=_engine, future=True)
    return _the_sessionmaker()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

class MountainPeakDao(object):

    def __init__(self, db: Session()):
        self.db = db

    def find_all(self) -> List[MountainPeakFull]:
        try:
            select_statement = select(MountainPeakModel)
            res = self.db.execute(select_statement).scalars()
            return [MountainPeakFull.from_orm(r) for r in res]
        except Exception as ex:
            msg = f"Errors while retrieving data from mountain_peak, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    def find_all_in_box(self, south: str, west: str, north: str,  east: str) -> List[MountainPeakFull]:
        try:
            select_statement = select(MountainPeakModel).where(MountainPeakModel.geom.ST_Intersects(ST_GeographyFromText(f'SRID=4326;POLYGON(({south},{west},{north},{east},{south}))')))
            res = self.db.execute(select_statement).scalars()
            return [MountainPeakFull.from_orm(r) for r in res]
        except InternalError as e:
            msg = f"Errors while retrieving data from mountain_peak, Check First the format of polygon point, two float separate by a space. detail of error : {e}"
            logging.error(msg)
            raise HTTPException(status_code=400, detail=msg)
        except Exception as ex:
            msg = f"Errors while retrieving data from mountain_peak, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)
    
    def find_by_name(self, name: str) -> MountainPeakFull:
        try:
            select_statement = select(MountainPeakModel).where(MountainPeakModel.name == name)
            res = self.db.execute(select_statement).scalar()
            return MountainPeakFull.from_orm(res) if res is not None else  None
        except Exception as ex:
            msg = f"Errors while retrieving data from mountain_peak, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)
    
    def find_by_id(self, id: int) -> MountainPeakFull:
        try:
            select_statement = select(MountainPeakModel).where(MountainPeakModel.id == id)
            res = self.db.execute(select_statement).scalar()
            return MountainPeakFull.from_orm(res) if res is not None else  None
        except Exception as ex:
            msg = f"Errors while retrieving data from mountain_peak, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)
    
    def create(self, mountain_peak_list: List[MountainPeakModel]) :
        try:
            self.db.add_all(mountain_peak_list)
            self.db.commit()
            return
        except IntegrityError:
            msg = f"Mountain Peak alredy exists"
            logging.error(msg)
            raise HTTPException(status_code=409, detail=msg)
        except Exception as ex:
            msg = f"Errors while creating mountain peaks, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    
    def update(self, mountain_peak: MountainPeak, id: int) :
        try:
            data = mountain_peak.dict()
            data['geom']=geom=f'POINT({mountain_peak.lat} {mountain_peak.lon})'
            update_statement = update(MountainPeakModel).where(MountainPeakModel.id == id).values(data)
            self.db.execute(update_statement)
            self.db.commit()
            return
        except IntegrityError:
            msg = f"Name already used"
            logging.error(msg)
            raise HTTPException(status_code=409, detail=msg)
        except Exception as ex:
            msg = f"Errors while updating mountain peaks, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    def delete(self, id: int) :
        try:
            delete_statement = delete(MountainPeakModel).where(MountainPeakModel.id == id)
            self.db.execute(delete_statement)
            self.db.commit()
            return
        except Exception as ex:
            msg = f"Errors while deleting mountain peaks, details: {ex}"
            logging.error(msg)
            raise HTTPException(status_code=500, detail=msg)