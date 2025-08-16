import json

from app.schemas.mem_data import (
    Framework,
    Category,
    Control,
    CustomField,
)


def load_nist_csf_v2_0_data(id) -> Framework:
    nist_csf = Framework(
        id=id,
        name="NIST CSF v2.0",
        description="NIST Cybersecurity Framework 2.0",
        owner="NIST",
    )

    with open("content/NIST_CSF_v2_0/nist_csf_2_0_with_imp_exs.json") as f:
        nist_csf_data = json.load(f)

    for function_id, function in nist_csf_data["functions"].items():
        func_category = Category(
            name=function["title"],
            cat_string_id=function_id,
            type="Function",
            description=function["text"],
            framework=nist_csf,
        )

        nist_csf.categories.append(func_category)

        for category_id, category in function["categories"].items():
            cat_category = Category(
                name=category["title"],
                cat_string_id=category_id,
                type="Category",
                description=category["text"],
                framework=nist_csf,
            )
            func_category.categories.append(cat_category)

            for subcategory_id, subcategory in category["subcategories"].items():
                control = Control(
                    control_string_id=subcategory_id,
                    title=subcategory_id,
                    text=subcategory["text"],
                    framework=nist_csf,
                    category=cat_category,
                )

                cat_category.controls.append(control)
                nist_csf.controls.append(control)

                for imp_ex_id, imp_ex in subcategory["implementation_examples"].items():
                    custom_field = CustomField(
                        name=imp_ex_id,
                        value=imp_ex["text"],
                    )
                    control.custom_fields.append(custom_field)

    return nist_csf
