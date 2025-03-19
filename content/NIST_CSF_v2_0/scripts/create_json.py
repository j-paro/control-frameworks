import json

if __name__ == "__main__":
    with open("content/NIST_CSF_20/nist_csf_2_0_sort_order.json") as f:
        nist_csf_sort_order = json.load(f)

    framework = {"functions": {}}

    for sort_key, value in nist_csf_sort_order.items():
        if len(sort_key) == 5:
            framework["functions"][value] = {}
            framework["functions"][value]["categories"] = {}
            current_function = value
        elif len(sort_key) == 11:
            framework["functions"][current_function]["categories"][value] = {}
            framework["functions"][current_function]["categories"][value][
                "subcategories"
            ] = {}
            current_category = value
        elif len(sort_key) == 17:
            framework["functions"][current_function]["categories"][
                current_category
            ]["subcategories"][value] = True

    with open("content/NIST_CSF_20/nist_csf_2_0_ids_only.json", "w") as f:
        f.write(json.dumps(framework, indent=2))
