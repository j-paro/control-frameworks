import json

from app.schemas.mem_data import (
    Framework,
    Category,
    Control,
)


def load_nist_csf_v1_1_data(id) -> Framework:
    nist_csf = Framework(
        id=id,
        name="NIST CSF v1.1",
        description="NIST Cybersecurity Framework",
        owner="NIST",
    )

    with open("content/NIST_CSF_v1_1/NIST-CSF.json") as f:
        nist_csf_data = json.load(f)

    for function_id, function in nist_csf_data["functions"].items():
        func_category = Category(
            name=function["name"],
            cat_string_id=function_id,
            type="Function",
            framework=nist_csf,
        )

        nist_csf.categories.append(func_category)

        for category_id, category in function["categories"].items():
            cat_category = Category(
                cat_string_id=category_id,
                name=category["name"],
                type="Category",
                description=category["description"],
                framework=nist_csf,
            )
            func_category.categories.append(cat_category)

            for subcategory_id, subcategory in category["subcategories"].items():
                control = Control(
                    control_string_id=subcategory_id,
                    title=subcategory_id,
                    text=subcategory["description"],
                    framework=nist_csf,
                    category=cat_category,
                )

                cat_category.controls.append(control)
                nist_csf.controls.append(control)

    return nist_csf
