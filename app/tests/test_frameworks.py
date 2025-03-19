from fastapi.testclient import TestClient

from app.main import app
from app.schemas.mem_data import Framework
from app.lifespan import data


client = TestClient(app)
headers = {"Host": "localhost"}


def test_get_frameworks():
    with TestClient(app) as client:
        response = client.get(
            app.url_path_for("get_frameworks"), headers=headers
        )

        print("length of frameworks", len(data.frameworks))
        print("length of response", len(response.json()))

        assert response.status_code == 200
        assert len(data.frameworks) == len(response.json())


def test_get_framework_by_id():
    with TestClient(app) as client:
        response = client.get(
            app.url_path_for(
                "get_framework_by_id", framework_id="NIST CSF v1.1"
            ),
            headers=headers,
        )

        print("length of frameworks", len(data.frameworks))
        print("length of response", len(response.json()))

        assert response.status_code == 200

        framework = data.frameworks["NIST CSF v1.1"]
        assert framework.string_id == response.json()["string_id"]


def test_search_frameworks():
    with TestClient(app) as client:
        response = client.get(
            app.url_path_for("search_frameworks"),
            params={"search_string": "nist"},
            headers=headers,
        )
        assert response.status_code == 200
        string_found_in_all = True
        for framework in response.json():
            if (
                "nist"
                not in (
                    framework["name"]
                    + framework["description"]
                    + framework["owner"]
                ).lower()
            ):
                string_found_in_all = False
                break

        assert string_found_in_all

        reponse = client.get(
            app.url_path_for("search_frameworks"),
            params={"search_string": "<something not found>"},
            headers=headers,
        )
        response_length = len(reponse.json())
        assert response.status_code == 200
        assert response_length == 0
