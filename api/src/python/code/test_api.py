import json

from fastapi.testclient import TestClient
from code.api import app

client = TestClient(app)
# test de dev non definitif, pour tester lancer cette commande python -m pytest code dans le dossier api/src/python

def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200


def test_create():
    response = client.post(
        "/mountain-peaks",
        json=[{"name": "culo2", "altitude": 1200, "lat": 42.93307385294335, "lon": 0.6280411760313553},
        {"name": "Farrenberg2", "altitude": 1500, "lat": 48.38579802606362, "lon": 9.087365033069982}],
    )
    assert response.status_code == 200


def test_find_all():
    response = client.get("/mountain-peaks")
    
    
    assert response.status_code == 200
    assert len(response.json()) > 1
    