import json

import pandas
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models import Framework, Category, Control


def load_800_53_r5_data(session: Session):
    try:
        result = session.execute(
            select(Framework).where(
                and_(
                    Framework.name == "NIST SP 800-53 Revision 5",
                    Framework.owner == "NIST",
                )
            )
        )
        if not result.scalar_one_or_none():
            r5_800_53_framework = Framework(
                name="NIST SP 800-53 Revision 5",
                description="NIST Special Publication 800-53 Revision 5",
                owner="NIST",
            )

            root_category = Category(
                name="ROOT",
                cat_string_id="ROOT",
                type="ROOT",
                framework=r5_800_53_framework,
            )

            with open("content/SP800_53/800-53.json") as f:
                json_800_53 = json.load(f)

            current_family = None
            families = {}
            for control in json_800_53["controls"]["control"]:
                family = control["family"]
                two_letter_id = control["number"][:2]
                if family != current_family:
                    current_family = family
                    families[two_letter_id] = family

            df = pandas.read_excel(
                "content/SP800_53/sp800-53r5-controls.xlsx",
                sheet_name="SP 800-53 Revision 5",
            )
            df = df[
                [
                    "Control Identifier",
                    "Control (or Control Enhancement) Name",
                    "Control (or Control Enhancement)",
                    "Related Controls",
                ]
            ]
            df.fillna("<No Text>", inplace=True)

            current_two_letter_id = None
            current_category = None
            for _, row in df.iterrows():
                two_letter_id = row[0][:2]
                if two_letter_id != current_two_letter_id:
                    current_two_letter_id = two_letter_id
                    current_category = Category(
                        name=families[two_letter_id].title(),
                        cat_string_id=two_letter_id,
                        type="Family",
                        framework=r5_800_53_framework,
                    )
                    root_category.children.append(current_category)

                current_category.controls.append(
                    Control(
                        control_string_id=row[0],
                        title=row[1],
                        text=row[2],
                        framework=r5_800_53_framework,
                    )
                )

            # for category in root_category.children:
            #     print(category.__repr__())
            #     for control in category.controls:
            #         print(control.__repr__())

            session.add(r5_800_53_framework)
            session.add(root_category)
            session.commit()
        else:
            print("NIST SP 800-53 Revision 5 already loaded")
    except Exception as e:
        print("Error: ", e)
