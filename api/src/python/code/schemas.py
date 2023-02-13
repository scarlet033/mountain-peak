

from pydantic import BaseModel

class MountainPeak(BaseModel):
    name: str
    altitude: float
    lat: float
    lon: float 
    
    class Config:
        orm_mode = True


class MountainPeakFull(MountainPeak):
    id: int