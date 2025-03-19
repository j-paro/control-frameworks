import asyncio

from httpx import AsyncClient


async def create_framework(
    client: AsyncClient,
    name: str = "Test Framework",
    description: str = "Test Description",
    owner: str = "Test Owner",
) -> int:
    data = {
        "name": name,
        "description": description,
        "owner": owner,
    }
    response = await client.post("/frameworks/", json=data)
    framework = response.json()
    return framework["id"]


async def create_category(
    client: AsyncClient,
    cat_string_id: str = "TEST_CAT_ID",
    name: str = "Test Category",
    type: str = "Test Type",
    description: str = "Test Description",
    framework_id: int = 11,
) -> int:
    data = {
        "cat_string_id": cat_string_id,
        "name": name,
        "type": type,
        "description": description,
        "framework_id": framework_id,
    }
    response = await client.post("/categories/", json=data)
    category = response.json()
    return category["id"]


async def create_control(
    client: AsyncClient,
    control_string_id: str = "TEST_CONTROL_ID",
    title: str = "Test Control",
    text: str = "Test Text",
    category_id: int = 309,
    framework_id: int = 11,
) -> int:
    data = {
        "control_string_id": control_string_id,
        "title": title,
        "text": text,
        "category_id": category_id,
        "framework_id": framework_id,
    }
    response = await client.post("/controls/", json=data)
    control = response.json()
    return control["id"]


if __name__ == "__main__":

    async def main() -> None:
        async with AsyncClient(base_url="http://localhost:8000/") as client:
            # framework_id = await create_framework(client)
            # print(f"Framework created with id: {framework_id}")
            # category_id = await create_category(client)
            # print(f"Category created with id: {category_id}")
            control_id = await create_control(client)
            print(f"Control created with id: {control_id}")

    asyncio.run(main())
