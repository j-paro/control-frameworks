from uuid import uuid4, UUID

from app.main import app
from app.lifespan import data


headers = {"Host": "localhost"}


def get_control_ids(category: dict) -> list[UUID]:
    control_ids = [UUID(control["id"]) for control in category["controls"]]
    for child in category["categories"]:
        control_ids.extend(get_control_ids(child))
    return control_ids


def test_get_control(client):
    control_id = list(data.control_index.keys())[0]
    response = client.get(
        app.url_path_for("get_control_by_id", control_id=control_id),
        headers=headers,
    )
    assert response.status_code == 200
    assert UUID(response.json()["id"]) == control_id

    response = client.get(
        app.url_path_for("get_control_by_id", control_id=uuid4()),
        headers=headers,
    )
    assert response.status_code == 404


def test_get_control_by_string_id(client):
    controls = [
        control
        for control in data.control_index.values()
        if "ID.AM-1" in control.control_string_id
    ]
    control_ids = [control.id for control in controls]
    response = client.get(
        app.url_path_for("get_control_by_string_id", control_string_id="ID.AM-1"),
        headers=headers,
    )
    assert response.status_code == 200
    assert sorted([UUID(control["id"]) for control in response.json()]) == sorted(
        control_ids
    )

    controls = [
        control
        for control in data.control_index.values()
        if "ID.AM" in control.control_string_id
    ]
    control_ids = [control.id for control in controls]
    response = client.get(
        app.url_path_for("get_control_by_string_id", control_string_id="ID.AM"),
        headers=headers,
    )
    assert response.status_code == 200
    assert sorted([UUID(control["id"]) for control in response.json()]) == sorted(
        control_ids
    )

    response = client.get(
        app.url_path_for("get_control_by_string_id", control_string_id="999999"),
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_controls_by_category(client):
    category = list(data.category_index.values())[0]
    category_id = category.id

    response = client.get(
        app.url_path_for("get_controls_by_category", category_id=category_id),
        headers=headers,
    )

    assert response.status_code == 200

    control_id_list = category.get_control_id_list()

    resp_control_id_list = []
    for control in response.json()["controls"]:
        resp_control_id_list.append(UUID(control["id"]))

    for category in response.json()["categories"]:
        resp_control_id_list.extend(get_control_ids(category))

    assert sorted(control_id_list) == sorted(resp_control_id_list)

    response = client.get(
        app.url_path_for("get_controls_by_category", category_id=uuid4()),
        headers=headers,
    )
    assert response.status_code == 404


def test_get_controls_by_framework(client):
    framework = list(data.frameworks.values())[0]
    framework_id = framework.id
    control_ids = framework.get_control_id_list()

    response = client.get(
        app.url_path_for("get_controls_by_framework", framework_id=framework_id),
        headers=headers,
    )
    assert response.status_code == 200

    resp_control_id_list = []
    for control in response.json():
        resp_control_id_list.append(UUID(control["id"]))

    assert sorted(control_ids) == sorted(resp_control_id_list)

    response = client.get(
        app.url_path_for("get_controls_by_framework", framework_id=uuid4()),
        headers=headers,
    )
    assert response.status_code == 404


def test_search_controls(client):
    controls = [
        control
        for control in data.control_index.values()
        if "ID.AM-1".lower()
        in (control.control_string_id + (control.title or "") + control.text).lower()
    ]
    control_ids = [control.id for control in controls]

    response = client.get(
        app.url_path_for("search_controls"),
        params={"search_string": "ID.AM-1"},
        headers=headers,
    )
    assert response.status_code == 200
    assert sorted([UUID(control["id"]) for control in response.json()]) == sorted(
        control_ids
    )

    controls = [
        control
        for control in data.control_index.values()
        if "ID.AM".lower()
        in (control.control_string_id + (control.title or "") + control.text).lower()
    ]
    control_ids = [control.id for control in controls]

    response = client.get(
        app.url_path_for("search_controls"),
        params={"search_string": "ID.AM"},
        headers=headers,
    )

    assert response.status_code == 200
    assert sorted([UUID(control["id"]) for control in response.json()]) == sorted(
        control_ids
    )


# def test_get_control_mappings(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = session.execute(
#         select(Control)
#         .where(Control.control_string_id == "ID.AM-1")
#         .options(selectinload(Control.control_mappings))
#     )
#     id_am_1: Control = result.scalars().first()
#     response = client.get(
#         app.url_path_for("get_control_mappings"),
#         params={"control_id": id_am_1.id},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()["control_mappings"]) == len(
#         id_am_1.control_mappings
#     )

#     response = client.get(
#         app.url_path_for("get_control_mappings"),
#         params={"control_id": 999999},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404
