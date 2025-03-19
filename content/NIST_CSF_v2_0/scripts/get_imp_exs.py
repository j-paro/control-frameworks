import json
from pprint import pprint

if __name__ == "__main__":
    with open("content/NIST_CSF_v2_0/cprt_CSF_2_0_0_04-24-2024.json") as f:
        nist_csf_data = json.load(f)

    implementation_examples = {}

    elements = nist_csf_data["response"]["elements"]["elements"]
    for element in elements:
        if element["element_type"] == "implementation_example":
            implementation_example = element["element_identifier"]
            implementation_examples[implementation_example] = {
                "title": element["title"],
                "text": element["text"],
                "categories": {},
            }

    with open("content/NIST_CSF_v2_0/nist_csf_2_0_imp_exs.json", "w") as f:
        json.dump(implementation_examples, f, indent=2)
