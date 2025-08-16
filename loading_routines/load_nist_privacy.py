import re
from typing import Union

import pandas as pd
import numpy as np

from app.schemas.mem_data import Framework, Category, Control, CustomField


def get_id_between_parens(text):
    """Returns all values within parentheses in a given string"""
    regex = r"\((.*?)\)"
    matches = re.findall(regex, text)
    return matches[0]


def check_alignment(value, obj: Union[Framework, Category, Control], obj_type):
    if value == "E":
        obj.custom_fields.append(
            CustomField(
                name="Alignment to NIST CSF v1.1",
                value=f"Identical to the analogous NIST CSF v1.1 {obj_type}",
            )
        )
    elif value == "A":
        obj.custom_fields.append(
            CustomField(
                name="Alignment to NIST CSF v1.1",
                value=f"The {obj_type} aligns with the NIST CSF v1.1, but the text has been adapted for the Privacy Framework",
            )
        )


def load_nist_privacy_data(id) -> Framework:
    nist_privacy_df = pd.read_excel(
        "content/NIST_Privacy/NIST-Privacy-Framework-V1.0-Core.xlsx",
        sheet_name="Privacy Framework Core",
    )
    nist_privacy_df.columns = nist_privacy_df.iloc[1]
    nist_privacy_df = nist_privacy_df[2:]
    nist_privacy_df = nist_privacy_df.rename_axis(None, axis=1)
    nist_privacy_df.columns = [
        f"Column_{i}" if pd.isna(col) else col
        for i, col in enumerate(nist_privacy_df.columns)
    ]

    nist_privacy_df = nist_privacy_df[
        [
            "Function",
            "Column_2",
            "Category",
            "Column_4",
            "Subcategory",
            "Column_6",
        ]
    ]
    nist_privacy_df.replace(np.nan, "", inplace=True)

    nist_privacy_framework = Framework(
        id=id,
        name="NIST Privacy Framework",
        description="NIST Privacy Framework v1.0",
        owner="NIST",
    )

    current_function_obj = None
    current_category_obj = None
    for _, row in nist_privacy_df.iterrows():
        if row["Function"]:
            current_function_obj = Category(
                cat_string_id=get_id_between_parens(row["Function"]),
                name=row["Function"].split("(")[0].strip(),
                type="Function",
                description=row["Function"].split(":")[1].strip(),
                framework=nist_privacy_framework,
            )
            check_alignment(row["Column_2"], current_function_obj, "Function")
            nist_privacy_framework.categories.append(current_function_obj)

        if row["Category"]:
            current_category_obj = Category(
                cat_string_id=get_id_between_parens(row["Category"]),
                name=row["Category"].split("(")[0].strip(),
                type="Category",
                description=row["Category"].split(":")[1].strip(),
                framework=nist_privacy_framework,
            )
            check_alignment(row["Column_4"], current_category_obj, "Category")
            current_function_obj.categories.append(current_category_obj)

        current_control_obj = Control(
            control_string_id=row["Subcategory"].split(":")[0],
            text=row["Subcategory"].split(":")[1].strip(),
            category=current_category_obj,
            framework=nist_privacy_framework,
        )
        check_alignment(row["Column_6"], current_control_obj, "Control")

        current_category_obj.controls.append(current_control_obj)
        nist_privacy_framework.controls.append(current_control_obj)

    return nist_privacy_framework
