import pytest
import json
import sys
sys.path.append("..")
from run import app

@pytest.fixture 
def client():
    test_client = app.test_client()
    return test_client

@pytest.fixture
def sample_ride():
    test_rides = {
        "driver_id":1,
        "starting":"Juja",   
        "destination":"Thika",
        "departure":"1:00 pm",
        "capacity":"5"
    }

    return test_rides


def test_api_ridescreate(client,sample_ride):
    response = client.post('/ridesadd', data = json.dumps(sample_ride), content_type = 'application/json')
    result = json.loads(response.data)
    assert response.status_code == 201
    data = []
    data = result["ride"]
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["starting"] == sample_ride["starting"]
    assert data["destination"] == sample_ride["destination"]
    assert data["departure"] == sample_ride["departure"]

def test_api_ridesall(client,sample_ride):
    response = client.get('/rides')
    result = json.loads(response.data)
    assert response.status_code == 200
    data = result["rides"][0]
    assert data["id"] == 1
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["starting"] == sample_ride["starting"]
    assert data["destination"] == sample_ride["destination"]
    assert data["departure"] == sample_ride["departure"]
    assert data["arrived"] == False
    assert data["full"] == False

def test_api_specificride(client,sample_ride):
    ride_id = 1 
    response = client.get("/rides"+str(ride_id))
    result = json.loads(response.data)
    assert response.status_code == 200
    assert len(result["ride"]) ==  1
    data = result["ride"][0]
    assert data["id"] == 1
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["starting"] == sample_ride["starting"]
    assert data["destination"] == sample_ride["destination"]
    assert data["departure"] == sample_ride["departure"]
    assert data["arrived"] == False
    assert data["full"] == False
