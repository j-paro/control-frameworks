from uuid import UUID

from app.main import app
from app.lifespan import data


headers = {"Host": "localhost"}


def test_get_frameworks(client):
    response = client.get(app.url_path_for("get_frameworks"), headers=headers)

    assert response.status_code == 200
    assert len(data.frameworks) == len(response.json())


def test_get_framework_by_id(client):
    response = client.get(app.url_path_for("get_frameworks"), headers=headers)

    response_json = response.json()
    framework_id = UUID(response_json[0]["id"])

    response = client.get(
        app.url_path_for("get_framework_by_id", framework_id=framework_id),
        headers=headers,
    )

    assert response.status_code == 200

    framework = data.frameworks.get(framework_id)
    assert framework


def test_search_frameworks(client):
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
                framework["name"] + framework["description"] + framework["owner"]
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
