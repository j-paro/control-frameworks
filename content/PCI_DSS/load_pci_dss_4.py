import json

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models import Framework, Category, Control, CustomField


def load_pci_dss_data(session: Session):
    with open("content/PCI_DSS/pci_401_framework.json") as f:
        pci_dss_401_data = json.load(f)

    result = session.execute(
        select(Framework).where(
            and_(
                Framework.name == "PCI DSS v4.0.1",
                Framework.owner == "PCI Security Standards Council",
            )
        )
    )
    if not result.scalar_one_or_none():
        pci_dss = Framework(
            name="PCI DSS v4.0.1",
            description="Payment Card Industry Data Security Standard",
            owner="PCI Security Standards Council",
        )

        root_category = Category(
            name="ROOT",
            cat_string_id="ROOT",
            type="ROOT",
            framework=pci_dss,
        )

        print("Loading PCI DSS v4.0.1")
        for req_id, req in pci_dss_401_data.items():
            req_category = Category(
                cat_string_id=req_id,
                name=req["title"],
                type="REQUIREMENT",
                framework=pci_dss,
            )
            root_category.children.append(req_category)

            for subreq_id, subreq in req["subreqs"].items():
                subreq_category = Category(
                    cat_string_id=subreq_id,
                    name=subreq["title"],
                    type="SUB-REQUIREMENT",
                    framework=pci_dss,
                )
                req_category.children.append(subreq_category)

                for defined_approach_id, defined_approach in subreq[
                    "defined_approaches"
                ].items():
                    control = Control(
                        control_string_id=defined_approach_id,
                        text=defined_approach["title"],
                        framework=pci_dss,
                    )
                    subreq_category.controls.append(control)

        # for child in root_category.children:
        #     print(child.__repr__())
        #     for child in child.children:
        #         print(child.__repr__())
        #         for control in child.controls:
        #             print("\t" + control.__repr__())
        #             for custom_field in control.custom_fields:
        #                 print("\t\t" + custom_field.__repr__())

        session.add(pci_dss)
        session.add(root_category)
        session.commit()
    else:
        print("PCI DSS v4.0.1 already loaded")
