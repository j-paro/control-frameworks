from app.main import app
from app.schemas.mem_data import Control, Category, Framework


# async def test_get_control(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     response = await client.get(
#         app.url_path_for("get_control", control_id=1),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == 1

#     response = await client.get(
#         app.url_path_for("get_control", control_id=999999),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# async def test_get_control_by_string_id(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     response = await client.get(
#         app.url_path_for(
#             "get_control_by_string_id", control_string_id="ID.AM-1"
#         ),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     result = await session.execute(
#         select(Control).where(Control.control_string_id == "ID.AM-1")
#     )
#     assert response.json()[0]["id"] == result.scalars().first().id

#     response = await client.get(
#         app.url_path_for("get_control_by_string_id", control_string_id="ID.AM"),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     result = await session.execute(
#         select(Control).where(Control.control_string_id.like("%ID.AM%"))
#     )
#     assert len(response.json()) == len(result.scalars().all())

#     response = await client.get(
#         app.url_path_for(
#             "get_control_by_string_id", control_string_id="999999"
#         ),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 0


# async def test_get_controls_by_category(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Framework).where(
#             and_(Framework.name == "NIST CSF", Framework.owner == "NIST")
#         )
#     )
#     nist_csf = result.scalars().first()
#     result = await session.execute(
#         select(Category).where(
#             and_(
#                 Category.cat_string_id == "ID.AM",
#                 Category.framework_id == nist_csf.id,
#             )
#         )
#     )
#     id_am_category = result.scalars().first()
#     response = await client.get(
#         app.url_path_for(
#             "get_controls_by_category", category_id=id_am_category.id
#         ),
#         headers=default_user_headers,
#     )
#     result = await session.execute(
#         select(Control).where(Control.category_id == id_am_category.id)
#     )
#     controls = result.scalars().all()

#     assert response.status_code == 200
#     assert len(response.json()["controls"]) == len(controls)
#     result = await session.execute(
#         select(Control).where(
#             and_(
#                 Control.category_id == id_am_category.id,
#                 Control.framework_id == nist_csf.id,
#             )
#         )
#     )
#     assert len(response.json()["controls"]) == len(result.scalars().all())

#     response = await client.get(
#         app.url_path_for("get_controls_by_category", category_id=999999),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# async def test_get_controls_by_framework(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Framework).where(
#             and_(Framework.name == "NIST CSF", Framework.owner == "NIST")
#         )
#     )
#     nist_csf = result.scalars().first()
#     response = await client.get(
#         app.url_path_for("get_controls_by_framework", framework_id=nist_csf.id),
#         headers=default_user_headers,
#     )
#     result = await session.execute(
#         select(Control).where(Control.framework_id == nist_csf.id)
#     )
#     controls = result.scalars().all()

#     assert response.status_code == 200
#     assert len(response.json()) == len(controls)

#     response = await client.get(
#         app.url_path_for("get_controls_by_framework", framework_id=999999),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# async def test_get_control_mappings(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Control)
#         .where(Control.control_string_id == "ID.AM-1")
#         .options(selectinload(Control.control_mappings))
#     )
#     id_am_1: Control = result.scalars().first()
#     response = await client.get(
#         app.url_path_for("get_control_mappings"),
#         params={"control_id": id_am_1.id},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()["control_mappings"]) == len(
#         id_am_1.control_mappings
#     )

#     response = await client.get(
#         app.url_path_for("get_control_mappings"),
#         params={"control_id": 999999},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# async def test_search_controls(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     response = await client.get(
#         app.url_path_for("search_controls"),
#         params={"search_string": "ID.AM-1"},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 1

#     response = await client.get(
#         app.url_path_for("search_controls"),
#         params={"search_string": "ID.AM"},
#         headers=default_user_headers,
#     )
#     result = await session.execute(
#         select(Control).where(Control.control_string_id.like("%ID.AM%"))
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == len(result.scalars().all())
