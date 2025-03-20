import pandas as pd

from app.schemas.mem_data import (
    Framework,
    Category,
    Control,
    CustomField,
)


def load_ccm_data(id) -> Framework:

    ccm = Framework(
        id=id,
        name="CCM",
        description="Cloud Controls Matrix v4.0.5",
        owner="The Cloud Security Alliance",
    )

    ccm_df = pd.read_excel("content/CSA_CCM/CCMv4.0.5.xlsx", sheet_name="CCM")

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    ccm_df_main = ccm_df.dropna().reset_index(drop=True)
    ccm_df_main.columns = ccm_df_main.iloc[0]
    ccm_df_main = ccm_df_main.iloc[1:].reset_index(drop=True)
    ccm_df_main = ccm_df_main.rename_axis(None, axis=1)

    ccm_df_main = ccm_df_main[
        [
            "Control Domain",
            "Control Title",
            "Control ID",
            "Control Specification",
            "IaaS",
            "PaaS",
            "SaaS",
            "Phys",
            "Network",
            "Compute",
            "Storage",
            "App",
            "Data",
            "Cybersecurity",
            "Internal Audit",
            "Architecture Team",
            "SW Development",
            "Operations",
            "Legal/Privacy",
            "GRC Team",
            "Supply Chain Management",
            "HR",
        ]
    ]

    #
    # CCM has only one category level
    #
    current_category = None
    current_category_obj = None
    for _, row in ccm_df_main.iterrows():
        if current_category != row["Control Domain"]:
            current_category = row["Control Domain"]
            current_category_obj = Category(
                cat_string_id=row["Control ID"].split("-")[0],
                name=row["Control Domain"],
                type="Control Domain",
                description="N/A",
                framework=ccm,
            )
            ccm.categories.append(current_category_obj)

        custom_fields = [
            CustomField(name="IaaS", value=row["IaaS"]),
            CustomField(name="PaaS", value=row["PaaS"]),
            CustomField(name="SaaS", value=row["SaaS"]),
            CustomField(name="Phys", value=row["Phys"]),
            CustomField(name="Network", value=row["Network"]),
            CustomField(name="Compute", value=row["Compute"]),
            CustomField(name="Storage", value=row["Storage"]),
            CustomField(name="App", value=row["App"]),
            CustomField(name="Data", value=row["Data"]),
            CustomField(name="Cybersecurity", value=row["Cybersecurity"]),
            CustomField(name="Internal Audit", value=row["Internal Audit"]),
            CustomField(
                name="Architecture Team",
                value=row["Architecture Team"],
            ),
            CustomField(
                name="SW Development",
                value=row["SW Development"],
            ),
            CustomField(
                name="Operations",
                value=row["Operations"],
            ),
            CustomField(
                name="Legal/Privacy",
                value=row["Legal/Privacy"],
            ),
            CustomField(
                name="GRC Team",
                value=row["GRC Team"],
            ),
            CustomField(
                name="Supply Chain Management",
                value=row["Supply Chain Management"],
            ),
            CustomField(
                name="HR",
                value=row["HR"],
            ),
        ]

        control = Control(
            control_string_id=row["Control ID"],
            title=row["Control Title"],
            text=row["Control Specification"],
            framework=ccm,
            category=current_category_obj,
            custom_fields=custom_fields,
        )

        ccm.controls.append(control)
        current_category_obj.controls.append(control)

    return ccm
