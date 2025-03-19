import json

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models import Framework, Category, Control


def print_category_tree(category, indent=0):
    print("  " * indent, category.cat_string_id)
    for child in category.children:
        print_category_tree(child, indent + 1)


def load_categories_and_controls(
    parent_category: Category,
    categories: dict,
    framework: Framework,
):
    for cat_id, contents in categories.items():
        category = Category(
            cat_string_id="HIPAA " + cat_id,
            name=contents["name"],
            type=contents["type"],
            framework=framework,
        )
        parent_category.children.append(category)

        if "categories" in contents.keys():
            load_categories_and_controls(
                category, contents["categories"], framework
            )

        if "controls" in contents.keys():
            for control_id, text in contents["controls"].items():
                # print(control_id)
                category.controls.append(
                    Control(
                        control_string_id=control_id,
                        text=text,
                        framework=framework,
                        category=category,
                    )
                )


def load_hipaa_data(session: Session):
    try:
        result = session.execute(
            select(Framework).where(
                and_(
                    Framework.name == "HIPAA Security Rule Controls",
                    Framework.owner == "HHS",
                )
            )
        )
        if not result.scalar_one_or_none():
            with open(
                "content/HIPAA/HIPAA-Part164-security-content.json", "r"
            ) as f:
                hipaa_json = json.load(f)

            hipaa = Framework(
                name="HIPAA Security Rule Controls",
                description="This contains only statements from HIPAA 164.306",
                owner="HHS",
            )
            root_category = Category(
                cat_string_id="ROOT", name="ROOT", type="ROOT", framework=hipaa
            )

            load_categories_and_controls(
                root_category,
                hipaa_json["categories"],
                hipaa,
            )
            print_category_tree(root_category)

            session.add(hipaa)
            session.add(root_category)
            session.commit()
            print("HIPAA loaded")
        else:
            print("HIPAA already loaded")
    except Exception as e:
        print(type(e))
        print("Error: ", e)
