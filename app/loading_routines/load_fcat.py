import pandas

from app.schemas.mem_data import (
    Category,
    Control,
    Framework,
)


def print_cat_tree(cat, level=0):
    print("  " * level + cat.__repr__())
    for child in cat.children:
        


def get_fcat_df():
    fcat_df = pandas.read_excel(
        "content/FFIEC/FFIEC-Cyber-Assessment-Tool-v3.4.2.xlsx",
        sheet_name="Table Roll Up",
    )

    fcat_df.columns = fcat_df.iloc[5]
    fcat_df = fcat_df.rename_axis(None, axis=1)
    fcat_df.drop([0, 1, 2, 3, 4, 5], inplace=True)
    fcat_df = fcat_df[
        ["domain", "Assesment Factor", "Component", "Maturity Level", "DS"]
    ]

    return fcat_df


def load_fcat_data() -> Framework:
    abbreviations = {
        "Domain": {
            "Cyber Risk Management and Oversight": "D1",
            "Threat Intelligence and Collaboration": "D2",
            "Cybersecurity Controls": "D3",
            "External Dependency Management": "D4",
            "Cyber Incident Management and Resilience": "D5",
        },
        "Assessment Factor": {
            "Governance": "G",
            "Risk Management": "RM",
            "Resources": "R",
            "Training and Culture": "TC",
            "Threat Intelligence": "TI",
            "Monitoring and Analyzing": "MA",
            "Information Sharing": "IS",
            "Preventative Controls": "PC",
            "Detective Controls": "DC",
            "Corrective Controls": "CC",
            "Connections": "C",
            "Relationship Management": "RM",
            "Incident Resilience Planning and Strategy": "IR",
            "Detection, Response, and Mitigation": "DR",
            "Escalation and Reporting": "ER",
        },
        "Component": {
            "Oversight": "Ov",
            "Strategy/Policies": "SP",
            "IT Asset Management": "IT",
            "Risk Management Program": "RMP",
            "Risk Assessment": "RA",
            "Audit": "Au",
            "Staffing": "St",
            "Training": "Tr",
            "Culture": "Cu",
            "Threat Intelligence and Information": "Ti",
            "Monitoring and Analyzing": "Ma",
            "Information Sharing": "Is",
            "Infrastructure Management": "Im",
            "Access and Data Management": "Am",
            "Device/End-Point Security": "De",
            "Secure Coding": "Se",
            "Threat and Vulnerability Detection": "Th",
            "Anomalous Activity Detection": "An",
            "Event Detection": "Ev",
            "Patch Management": "Pa",
            "Remediation": "Re",
            "Connections": "Co",
            "Due Diligence": "Dd",
            "Contracts": "Co",
            "Ongoing Monitoring": "Om",
            "Planning": "Pl",
            "Testing": "Te",
            "Detection": "De",
            "Response and Mitigation": "Re",
            "Escalation and Reporting": "Es",
        },
        "Maturity Level": {
            "Baseline": "B",
            "Evolving": "E",
            "Intermediate": "Int",
            "Advanced": "A",
            "Innovative": "Inn",
        },
    }

    fcat_df = get_fcat_df()

    fcat = Framework(
        name="FFIEC Cyber Assessment Tool",
        description="FFIEC Cyber Assessment Tool",
        owner="FFIEC",
    )

    current_domain = ""
    current_maturity_level = ""
    maturity_level_counter = 1
    current_domain_obj = None
    for _, row in fcat_df.iterrows():
        if current_domain != row["domain"]:
            current_domain = row["domain"]
            current_domain_obj = Category(
                cat_string_id=current_domain,
                name=current_domain,
                type="DOMAIN",
                framework=fcat,
            )
            fcat.categories.append(current_domain_obj)
        if current_maturity_level != row["Maturity Level"]:
            current_maturity_level = row["Maturity Level"]
            maturity_level_counter = 1

        control = Control(
            control_string_id=abbreviations["Domain"][row["domain"]]
            + "."
            + abbreviations["Assessment Factor"][row["Assesment Factor"]]
            + "."
            + abbreviations["Component"][row["Component"]]
            + "."
            + abbreviations["Maturity Level"][row["Maturity Level"]]
            + "."
            + str(maturity_level_counter),
            text=row["DS"],
            framework=fcat,
            category=current_domain_obj,
        )
        current_domain_obj.controls.append(control)
        fcat.controls.append(control)
        maturity_level_counter += 1

    # for control in fcat.controls:
    #     pprint(control.__repr__())

    # print_cat_tree(root_category)
