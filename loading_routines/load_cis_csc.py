import pandas

from app.schemas.mem_data import (
    Framework,
    Category,
    Control,
    CustomField,
)


def load_cis_csc_data(id) -> Framework:
    df = pandas.read_excel(
        open("content/CIS_CSC/CIS_Controls_Version_8.xlsx", "rb"),
        sheet_name="Controls V8",
    )
    df = df.astype({"CIS Safeguard": "string"})
    df.at[24, "CIS Safeguard"] = "3.10"
    df.at[39, "CIS Safeguard"] = "4.10"
    df.at[76, "CIS Safeguard"] = "8.10"
    df.at[120, "CIS Safeguard"] = "13.10"
    df.at[150, "CIS Safeguard"] = "16.10"

    cis_csc = Framework(
        id=id,
        name="CIS CSC",
        description="CIS Controls",
        owner="CIS",
    )

    cis_controls = [
        [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
        for row in zip(
            df["CIS Control"],
            df["CIS Safeguard"],
            df["Asset Type"],
            df["Security Function"],
            df["Title"],
            df["Description"],
            df["IG1"],
            df["IG2"],
            df["IG3"],
        )
    ]

    #
    # There is only one category level in CIS CSC.
    #
    current_category = None
    for row in cis_controls:
        if pandas.isna(row[1]):
            current_category = Category(
                cat_string_id=str(row[0]),
                name=row[4],
                type="N/A",
                description=row[5],
                framework=cis_csc,
            )
            cis_csc.categories.append(current_category)
        else:
            custom_fields = [
                CustomField(
                    name="Asset Type",
                    value=row[2] if not pandas.isna(row[2]) else "",
                ),
                CustomField(name="Security Function", value=row[3]),
                CustomField(
                    name="IG1", value=row[6] if not pandas.isna(row[6]) else ""
                ),
                CustomField(
                    name="IG2", value=row[7] if not pandas.isna(row[7]) else ""
                ),
                CustomField(
                    name="IG3", value=row[8] if not pandas.isna(row[8]) else ""
                ),
            ]
            current_control = Control(
                control_string_id=str(row[1]),
                title=row[4],
                text=row[5],
                framework=cis_csc,
                category=current_category,
                custom_fields=custom_fields,
            )
            current_category.controls.append(current_control)
            cis_csc.controls.append(current_control)

    return cis_csc
