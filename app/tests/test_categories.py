from uuid import uuid4, UUID

from app.main import app
from app.schemas.mem_data import Category
from app.lifespan import data


headers = {"Host": "localhost"}


def test_get_category(client):
    category_id = list(data.category_index.keys())[0]

    response = client.get(
        app.url_path_for("get_category", category_id=category_id), headers=headers
    )
    assert response.status_code == 200

    response_category_id = UUID(response.json()["id"])
    category = data.category_index.get(response_category_id)
    assert category

    response = client.get(
        app.url_path_for("get_category", category_id=uuid4()), headers=headers
    )
    assert response.status_code == 404


def test_get_categories_by_framework(client):
    framework = list(data.frameworks.values())[0]
    framework_id = framework.id
    category_ids = framework.get_category_id_list()

    response = client.get(
        app.url_path_for("get_categories_by_framework", framework_id=framework_id),
        headers=headers,
    )
    assert response.status_code == 200

    def get_category_ids(category: dict) -> list[UUID]:
        category_ids = [UUID(category["id"])]
        for child in category["categories"]:
            category_ids.extend(get_category_ids(child))
        return category_ids

    resp_cat_id_list = []
    for category in response.json():
        resp_cat_id_list.extend(get_category_ids(category))

    assert sorted(category_ids) == sorted(resp_cat_id_list)


def test_search_categories(client):
    search_string = "ID"
    response = client.get(
        app.url_path_for("search_categories"),
        params={"search_string": search_string},
        headers=headers,
    )
    assert response.status_code == 200
    all_match = True
    for category in response.json():
        if (
            search_string.lower()
            not in (
                category["name"]
                + category["cat_string_id"]
                + category["type"]
                + (category["description"] or "")
            ).lower()
        ):
            all_match = False
            break
    assert all_match

    response = client.get(
        app.url_path_for("search_categories"),
        params={"search_string": "<somthing that won't be found>"},
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
