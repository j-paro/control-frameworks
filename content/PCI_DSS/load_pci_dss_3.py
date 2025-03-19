import math

import pandas as pd

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models import Framework, Category, Control, CustomField


def load_pci_dss_data(session: Session):
    try:
        result = session.execute(
            select(Framework).where(
                and_(
                    Framework.name == "PCI DSS v3.2.1",
                    Framework.owner == "PCI Security Standards Council",
                )
            )
        )
        if not result.scalar_one_or_none():
            pci_dss = Framework(
                name="PCI DSS v3.2.1",
                description="Payment Card Industry Data Security Standard",
                owner="PCI Security Standards Council",
            )

            root_category = Category(
                name="ROOT",
                cat_string_id="ROOT",
                type="ROOT",
                framework=pci_dss,
            )

            pci_dss_df = pd.read_excel(
                "content/PCI_DSS/Prioritized-Approach-Tool-v3_2_1.xlsx",
                sheet_name="Prioritized Approach Milestones",
            )

            pci_dss_df = pci_dss_df[
                ["PCI DSS Requirements v3.2.1", "Milestone"]
            ]
            pci_dss_df = pci_dss_df[1:]

            current_req_category_obj = None
            for _, row in pci_dss_df.iterrows():
                if row["PCI DSS Requirements v3.2.1"].startswith("Note: "):
                    continue
                elif row["PCI DSS Requirements v3.2.1"].startswith(
                    "Requirement"
                ):
                    current_req_category_obj = Category(
                        cat_string_id=row[
                            "PCI DSS Requirements v3.2.1"
                        ].partition(": ")[0],
                        name=row["PCI DSS Requirements v3.2.1"].partition(": ")[
                            2
                        ],
                        type="REQUIREMENT",
                        framework=pci_dss,
                    )
                    root_category.children.append(current_req_category_obj)
                elif row["PCI DSS Requirements v3.2.1"].startswith("Appendix"):
                    current_req_category_obj = Category(
                        cat_string_id=row[
                            "PCI DSS Requirements v3.2.1"
                        ].partition(": ")[0],
                        name=row["PCI DSS Requirements v3.2.1"].partition(": ")[
                            2
                        ],
                        type="APPENDIX",
                        framework=pci_dss,
                    )
                    root_category.children.append(current_req_category_obj)
                else:
                    pci_control = Control(
                        control_string_id="PCI DSS "
                        + row["PCI DSS Requirements v3.2.1"].partition(" ")[0],
                        text=row["PCI DSS Requirements v3.2.1"].partition(" ")[
                            2
                        ],
                        framework=pci_dss,
                    )
                    current_req_category_obj.controls.append(pci_control)

                    if not math.isnan(row["Milestone"]):
                        pci_control.custom_fields.append(
                            CustomField(
                                name="Milestone",
                                value=str(int(row["Milestone"])),
                            )
                        )

            # for child in root_category.children:
            #     print(child.__repr__())
            #     for control in child.controls:
            #         print("\t" + control.__repr__())
            #         for custom_field in control.custom_fields:
            #             print("\t\t" + custom_field.__repr__())

            session.add(pci_dss)
            session.add(root_category)
            session.commit()
        else:
            print("PCI DSS v3.2.1 already loaded")
    except Exception as e:
        print("Error: ", e)
