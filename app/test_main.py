from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "OK"}


def test_get_schools_by_name():
    response = client.get("/v1/schools/?school_name=Alabama&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["header"]["total"] >= 1
    assert any("Alabama" in school["name"] for school in data["results"])


def test_get_school_by_state():
    response = client.get("/v1/schools/state/?state_code=CA&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "header" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["header"]["total"] >= 1
    assert any(
        school["location"]["state"] == "CA"
        for school in data["results"]
        if school["location"] is not None
    )


def test_get_school_by_region():
    response = client.get("/v1/schools/region/?region=Southeast&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "header" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["header"]["total"] >= 1
    assert any(
        "Southeast" in school["location"]["region"]
        for school in data["results"]
        if school["location"] is not None
    )


def test_get_school_by_locale():
    response = client.get("/v1/schools/locale/?locale=City&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "header" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["header"]["total"] >= 1
    assert any(
        "City" in school["location"]["locale"]
        for school in data["results"]
        if school["location"] is not None
    )


def test_get_school_by_zipcode():
    response = client.get("/v1/schools/zipcode/?zipcode=98926&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "header" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["header"]["total"] >= 1
    assert any(
        school["location"]["zipcode"] == "98926"
        for school in data["results"]
        if school["location"] is not None
    )
