import uvicorn

from fastapi import FastAPI, Depends, status
from code import context
from code.models import Base
from code.schemas import MountainPeak, MountainPeakFull
from code.dao import get_db, get_engine, MountainPeakDao
from code.service import MountainPeakService
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List


mountain_peak_service = MountainPeakService()


# Initiate postgres
Base.metadata.create_all(bind=get_engine())
# Create app
app = FastAPI(
    title="API Mountain Peak",
    description="API Mountain Peak",
    version=context.VERSION,
    root_path=context.DEPLOYED_PREFIX
)


@app.get('/version',
         responses={200: {"content": {"application/json": {"example": {"version": "1.0.0.0000"}}}}})
def get_version() -> dict:
    """
    Endpoint to get full version
    """
    return {"version": str(context.VERSION_FULL)}


@app.get('/mountain-peaks')
def find_all_mountain_peaks(response: Response, postgres_db: Session = Depends(get_db)) -> List[MountainPeakFull]:
    """
    Endpoint to get all mountain peaks
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    rsp = mountain_peak_service.find_all(mountain_peak_dao)
    response.status = status.HTTP_200_OK
    return rsp

@app.get('/box/mountain-peaks')
def find_all_in_box(south_lat: float, south_lon: float, west_lat: float, west_lon: float, north_lat: float, north_lon: float, east_lat: float, east_lon: float,response: Response, postgres_db: Session = Depends(get_db)) -> List[MountainPeakFull]:
    """
    <p>Endpoint to get all mountain peaks in a bounding box</p>
    <p>south west north and east: values represent geographic points that constitute a polygon</p>
    <p><h2>Type of values is a float: (latitude or longitude)<p>
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    rsp = mountain_peak_service.find_all_in_box(mountain_peak_dao, f'{south_lat} {south_lon}', f'{west_lat} {west_lon}', f'{north_lat} {north_lon}', f'{east_lat} {east_lon}')
    response.status = status.HTTP_200_OK
    return rsp

@app.get('/mountain-peaks/{name}')
def find_mountain_peak_by_name(name: str, response: Response, postgres_db: Session = Depends(get_db)) -> MountainPeakFull:
    """
    Endpoint to get  mountain peak by name
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    rsp = mountain_peak_service.find_by_name(mountain_peak_dao, name)
    response.status = status.HTTP_200_OK
    return rsp

@app.post('/mountain-peaks')
def create_mountain_peaks(mountain_peak_list: List[MountainPeak], response: Response, postgres_db: Session = Depends(get_db)) :
    """
    Endpoint to create one or many mountain peaks
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    mountain_peak_service.create(mountain_peak_dao, mountain_peak_list)
    response.status = status.HTTP_201_CREATED
    return {}

@app.put('/mountain-peaks/{id}')
def update_mountain_peak(id: int, mountain_peak: MountainPeak, response: Response, postgres_db: Session = Depends(get_db)) :
    """
    Endpoint to update a mountain peak
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    mountain_peak_service.update(mountain_peak_dao, mountain_peak, id)
    response.status = status.HTTP_200_OK
    return {}

@app.delete('/mountain-peaks/{id}')
def delete_mountain_peak(id: int, response: Response, postgres_db: Session = Depends(get_db)) :
    """
    Endpoint to delete a mountain peak
    """
    mountain_peak_dao = MountainPeakDao(postgres_db)
    mountain_peak_service.delete(mountain_peak_dao, id)
    response.status = status.HTTP_200_OK
    return {}


if __name__ == "__main__":
    uvicorn.run(app, host=context.HTTP_HOST, port=int(context.HTTP_PORT), log_level="info")
