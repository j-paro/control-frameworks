from app.schemas.mem_data import Framework, Category, Control, CustomField


def load_tsc_data():
    framework = Framework(
        name="TSC",
        description="TSC Framework -- used for SOC 2 certification",
        owner="AICPA",
    )

    with open("content/TSC/TSC_2020.txt", "r") as f:
        lines = f.readlines()

    #
    # Category Hierarchy (the following are the labels searched for):
    # TOP-LEVEL
    #   -> >> Common Control with optional COSO
    #      -> -- Trusted Service Criteria with optional Privacy,
    #            Integrity, Confidentiality, Availability, System
    #
    current_cat_for_controls = None
    control_counter = 0
    last_cat_at_levels = {0: root_category, 1: None, 2: None, 3: None}
    for line in lines:
        if line.startswith("TOP-LEVEL"):
            cat_id = line.split(": ")[1].strip()
            category = Category(
                cat_string_id=cat_id,
                name=cat_id,
                type="Top-Level",
                description="Top level category for TSC",
                framework=framework,
            )
            last_cat_at_levels[0].children.append(category)
            last_cat_at_levels[1] = category
            current_cat_for_controls = category
            control_counter = 0
        elif line.startswith(">>"):
            cat_id = line.split(" ")[0].split(">>")[1].strip()
            category = Category(
                cat_string_id=cat_id,
                name=cat_id,
                type="Common Control",
                description=line.split(" ", 1)[1].strip(),
                framework=framework,
            )
            last_cat_at_levels[1].children.append(category)
            last_cat_at_levels[2] = category
            current_cat_for_controls = category
            control_counter = 0
        elif line.startswith("--"):
            cat_id = line.split("--")[1].strip()
            category = Category(
                cat_string_id=last_cat_at_levels[2].cat_string_id
                + " "
                + cat_id,
                name=cat_id,
                type="Trusted Service Criteria",
                framework=framework,
            )
            last_cat_at_levels[2].children.append(category)
            last_cat_at_levels[3] = category
            current_cat_for_controls = category
            control_counter = 0
        else:
            control_counter += 1
            control_id = (
                current_cat_for_controls.cat_string_id
                + " "
                + str(control_counter)
            )
            control = Control(
                control_string_id=control_id,
                text=line.split(" ", 1)[1].strip(),
                framework=framework,
            )
            current_cat_for_controls.controls.append(control)
