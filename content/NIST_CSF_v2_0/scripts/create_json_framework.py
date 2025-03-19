import json

if __name__ == "__main__":
    with open("content/NIST_CSF_20/nist_csf_2_0_ids_only.json") as f:
        nist_csf_ids_only = json.load(f)

    with open("content/NIST_CSF_20/NIST-CSF-20.json") as f:
        old_framework = json.load(f)

    framework = {"functions": {}}

    for function_id, func_value in old_framework["functions"].items():
        framework["functions"][function_id] = {
            "title": func_value["title"],
            "text": func_value["text"],
            "categories": {},
        }
        for category_id, cat_value in func_value["categories"].items():
            if (
                category_id
                in nist_csf_ids_only["functions"][function_id]["categories"]
            ):
                framework["functions"][function_id]["categories"][
                    category_id
                ] = {
                    "title": cat_value["title"],
                    "text": cat_value["text"],
                    "subcategories": {},
                }
                for subcategory_id, subcat_value in cat_value[
                    "subcategories"
                ].items():
                    if (
                        subcategory_id
                        in nist_csf_ids_only["functions"][function_id][
                            "categories"
                        ][category_id]["subcategories"]
                    ):
                        framework["functions"][function_id]["categories"][
                            category_id
                        ]["subcategories"][subcategory_id] = {
                            "title": subcat_value["title"],
                            "text": subcat_value["text"],
                        }

    with open("content/NIST_CSF_20/nist_csf_2_0.json", "w") as f:
        json.dump(framework, f, indent=2)
