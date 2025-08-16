import json

if __name__ == "__main__":
    with open("content/NIST_CSF_20/cprt_CSF_2_0_0_04-24-2024.json") as f:
        nist_csf_data = json.load(f)

    elements = nist_csf_data["response"]["elements"]["elements"]
    sorted_framework = {}

    for element in elements:
        if element["element_type"] == "sort":
            sorted_framework[element["title"]] = element["element_identifier"][
                2:
            ]

    with open("content/NIST_CSF_20/nist_csf_2_0_sort_order.json", "w") as f:
        json.dump(sorted_framework, f, indent=2)
