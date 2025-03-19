from httpx import AsyncClient

import pandas as pd

from app.models import Framework, Category, Control


def load_ccm_data(client: AsyncClient):
    try:
        result = session.execute(
            select(Framework).where(
                and_(
                    Framework.name == "CCM",
                    Framework.owner == "The Cloud Security Alliance",
                )
            )
        )
        if not result.scalar_one_or_none():
            ccm = Framework(
                name="CCM",
                description="Cloud Controls Matrix v4.0.5",
                owner="The Cloud Security Alliance",
            )

            ccm_df = pd.read_excel(
                "content/CSA_CCM/CCMv4.0.5.xlsx", sheet_name="CCM"
            )

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
                ]
            ]

            root_category = Category(
                name="ROOT",
                cat_string_id="ROOT",
                type="ROOT",
                framework=ccm,
            )

            current_category = None
            current_category_obj = None
            for _, row in ccm_df_main.iterrows():
                control = Control(
                    control_string_id=row["Control ID"],
                    title=row["Control Title"],
                    text=row["Control Specification"],
                )

                if current_category != row["Control Domain"]:
                    current_category = row["Control Domain"]
                    current_category_obj = Category(
                        cat_string_id=row["Control ID"].split("-")[0],
                        name=row["Control Domain"],
                        type="Control Domain",
                        description="N/A",
                        framework=ccm,
                    )
                    root_category.children.append(current_category_obj)

                ccm.controls.append(control)
                current_category_obj.controls.append(control)

            session.add(ccm)
            session.add(root_category)
            session.commit()
        else:
            print("CCM already loaded")
    except Exception as e:
        print("Error: ", e)
