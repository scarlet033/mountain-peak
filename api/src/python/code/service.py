
import logging
from code.dao import MountainPeakDao
from code.schemas import MountainPeak
from code.models import MountainPeakModel
from typing import List
from fastapi import HTTPException

class MountainPeakService(object):

    def find_all(self, mountain_peak_dao: MountainPeakDao):
        return mountain_peak_dao.find_all()

    def find_all_in_box(self, mountain_peak_dao: MountainPeakDao, south: str, west: str, north: str,  east: str):
        return mountain_peak_dao.find_all_in_box(south, west, north,  east)

    def find_by_name(self, mountain_peak_dao: MountainPeakDao, name:str):
        res = mountain_peak_dao.find_by_name(name)
        if res:
            return res
        else:
            msg=f'mountain peak not found with name {name}'
            logging.error(msg)
            raise HTTPException(status_code=404, detail=msg)

    def create(self, mountain_peak_dao: MountainPeakDao, mountain_peak_list: List[MountainPeak]):
        mountain_peak_list = list(map(lambda x: MountainPeakModel(**x.dict(), geom=f'POINT({x.lat} {x.lon})'), mountain_peak_list))
        return mountain_peak_dao.create(mountain_peak_list)

    def update(self, mountain_peak_dao: MountainPeakDao, mountain_peak: MountainPeak, id: int):
        res = mountain_peak_dao.find_by_id(id)
        if res is None:
            msg=f'mountain peak not found with id {id}'
            logging.error(msg)
            raise HTTPException(status_code=404, detail=msg)
        return mountain_peak_dao.update(mountain_peak, id)


    def delete(self, mountain_peak_dao: MountainPeakDao, id: int):
        res = mountain_peak_dao.find_by_id(id)
        if res is None:
            msg= f'mountain peak not found with id {id}'
            logging.error(msg)
            raise HTTPException(status_code=404, detail=msg)
        return mountain_peak_dao.delete(id)
