import json
from pprint import pprint

if __name__ == "__main__":
    with open("content/NIST_CSF_v2_0/cprt_CSF_2_0_0_04-24-2024.json") as f:
        nist_csf_data = json.load(f)

    with open("content/NIST_CSF_v2_0/nist_csf_2_0_sort_order.json") as f:
        sort_order = json.load(f)

    framework = {}

    elements = nist_csf_data["response"]["elements"]["elements"]
    for element in elements:
        if element["element_type"] == "function":
            function = element["element_identifier"]
            framework[function] = {
                "title": element["title"],
                "text": element["text"],
                "categories": {},
            }
        elif element["element_type"] == "category":
            category = element["element_identifier"]
            function = category[:2]
            framework[function]["categories"][category] = {
                "title": element["title"],
                "text": element["text"],
                "subcategories": {},
            }
        elif element["element_type"] == "subcategory":
            subcategory = element["element_identifier"]
            category = subcategory[:5]
            function = category[:2]
            framework[function]["categories"][category]["subcategories"][
                subcategory
            ] = {"title": element["title"], "text": element["text"]}
            framework[function]["categories"][category]["subcategories"][
                subcategory
            ]["implementation_examples"] = {}
        elif element["element_type"] == "implementation_example":
            implementation_example = element["element_identifier"]
            function = implementation_example[:2]
            category = implementation_example[:5]
            subcategory = implementation_example[:8]
            framework[function]["categories"][category]["subcategories"][
                subcategory
            ]["implementation_examples"][implementation_example] = {
                "title": element["title"],
                "text": element["text"],
            }

    sorted_framework = {}
    sorted_framework["functions"] = {}
    for sort_key, id in sort_order.items():
        if len(sort_key) == 5:
            sorted_framework["functions"][id] = {
                "title": framework[id]["title"],
                "text": framework[id]["text"],
                "categories": {},
            }
        elif len(sort_key) == 11:
            function_id = id[:2]
            category_id = id
            sorted_framework["functions"][function_id]["categories"][
                category_id
            ] = {
                "title": framework[function_id]["categories"][category_id][
                    "title"
                ],
                "text": framework[function_id]["categories"][category_id][
                    "text"
                ],
                "subcategories": {},
            }
        elif len(sort_key) == 17:
            function_id = id[:2]
            category_id = id[:5]
            subcategory_id = id
            sorted_framework["functions"][function_id]["categories"][
                category_id
            ]["subcategories"][subcategory_id] = {
                "title": framework[function_id]["categories"][category_id][
                    "subcategories"
                ][subcategory_id]["title"],
                "text": framework[function_id]["categories"][category_id][
                    "subcategories"
                ][subcategory_id]["text"],
            }
            sorted_framework["functions"][function_id]["categories"][
                category_id
            ]["subcategories"][subcategory_id]["implementation_examples"] = {}
            for imp_ex in framework[function_id]["categories"][category_id][
                "subcategories"
            ][subcategory_id]["implementation_examples"]:
                sorted_framework["functions"][function_id]["categories"][
                    category_id
                ]["subcategories"][subcategory_id]["implementation_examples"][
                    imp_ex
                ] = framework[
                    function_id
                ][
                    "categories"
                ][
                    category_id
                ][
                    "subcategories"
                ][
                    subcategory_id
                ][
                    "implementation_examples"
                ][
                    imp_ex
                ]

    with open("content/NIST_CSF_v2_0/nist_csf_2_0_with_imp_exs.json", "w") as f:
        json.dump(sorted_framework, f, indent=2)
