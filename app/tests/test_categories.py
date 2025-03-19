from app.main import app
from app.schemas.mem_data import Category, Framework


# async def test_get_category(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Category).where(Category.cat_string_id == "ID")
#     )
#     id_category: Category = result.scalars().first()
#     response = await client.get(
#         app.url_path_for("get_category", category_id=id_category.id),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == id_category.id

#     response = await client.get(
#         app.url_path_for("get_category", category_id="999999"),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# def get_category_tree_hash(category: Category) -> int:
#     """Recursively compute a hash of a category tree."""
#     hash = 0
#     for child in category.children:
#         hash += get_category_tree_hash(child)
#     return hash + category.id


# def get_json_response_category_tree_hash(category: dict) -> int:
#     """Recursively compute a hash of a category tree."""
#     hash = 0
#     for child in category["children"]:
#         hash += get_json_response_category_tree_hash(child)
#     return hash + category["id"]


# async def test_get_categories_by_framework(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Framework).where(
#             and_(Framework.owner == "NIST", Framework.name == "NIST CSF")
#         )
#     )
#     nist_csf = result.scalars().first()
#     result = await session.execute(
#         select(Category).where(Category.framework_id == nist_csf.id)
#     )
#     categories = result.scalars().all()
#     response = await client.get(
#         app.url_path_for(
#             "get_categories_by_framework", framework_id=nist_csf.id
#         ),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     cat_id_hash = 0
#     for category in categories:
#         cat_id_hash += category.id
#     assert get_json_response_category_tree_hash(response.json()) == cat_id_hash


# async def test_get_category_by_string_id(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     result = await session.execute(
#         select(Category).where(Category.cat_string_id == "ID")
#     )
#     id_category: Category = result.scalars().first()
#     response = await client.get(
#         app.url_path_for(
#             "get_category_by_string_id",
#             cat_string_id=id_category.cat_string_id,
#         ),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == id_category.id

#     response = await client.get(
#         app.url_path_for("get_category_by_string_id", cat_string_id="999999"),
#         headers=default_user_headers,
#     )
#     assert response.status_code == 404


# async def test_search_categories(
#     client: AsyncClient, default_user_headers, session: AsyncSession
# ):
#     search_string = "ID"
#     result = await session.execute(
#         select(Category).where(
#             or_(
#                 Category.name.ilike(f"%{search_string}%"),
#                 Category.cat_string_id.ilike(f"%{search_string}%"),
#                 Category.description.ilike(f"%{search_string}%"),
#                 Category.type.ilike(f"%{search_string}%"),
#             )
#         )
#     )
#     categories = result.scalars().all()
#     response = await client.get(
#         app.url_path_for("search_categories"),
#         params={"search_string": search_string},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == len(categories)

#     response = await client.get(
#         app.url_path_for("search_categories"),
#         params={"search_string": "ID.AM.1.1.1"},
#         headers=default_user_headers,
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 0
