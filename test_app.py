from fastapi.testclient import TestClient
from main import app
client = TestClient(app)


def test_hello():
    response = client.get("/dosomething")
    assert response.status_code == 200
    assert response.text == "Hello"


def test_read_inexistent_item():
    response = client.get("/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
