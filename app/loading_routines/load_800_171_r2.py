import pandas as pd

from app.schemas.mem_data import (
    Framework,
    Category,
    Control,
    CustomField,
)


def load_800_171_r2_data(id) -> Framework:

    one_7_one = Framework(
        id=id,
        name="NIST SP 800-171",
        description="NIST Special Publication 800-171",
        owner="NIST",
    )

    one_7_one_df = pd.read_excel(
        "content/SP800_171/sp800-171r2-security-reqs.xlsx",
        sheet_name="SP 800-171",
    )

    one_7_one_df = one_7_one_df[
        [
            "Family",
            "Basic/Derived Security Requirement",
            "Identifier",
            "Sort-As",
            "Security Requirement",
            "Discussion",
        ]
    ]

    #
    # There is only one category level in SP 800-171
    #
    current_category = None
    current_category_obj = None
    for _, row in one_7_one_df.iterrows():
        if row["Family"] != current_category:
            current_category = row["Family"]
            current_category_obj = Category(
                cat_string_id=row["Family"],
                name=row["Family"],
                type="Family",
                framework=one_7_one,
            )
            one_7_one.categories.append(current_category_obj)

        custom_fields = [
            CustomField(name="Discussion", value=row["Discussion"]),
            CustomField(name="Sort-As", value=row["Sort-As"]),
            CustomField(
                name="Basic/Derived Security Requirement",
                value=row["Basic/Derived Security Requirement"],
            ),
        ]

        control = Control(
            control_string_id=row["Identifier"],
            text=row["Security Requirement"],
            framework=one_7_one,
            category=current_category_obj,
            custom_fields=custom_fields,
        )

        one_7_one.controls.append(control)
        current_category_obj.controls.append(control)

    return one_7_one
