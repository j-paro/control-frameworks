from uuid import uuid4
import dill as dill_pickle
import hmac

from dotenv import dotenv_values

config = dotenv_values(".env")


from app.schemas.mem_data import Framework, Category, Control
from loading_routines.load_nist_csf_v1_1 import load_nist_csf_v1_1_data
from loading_routines.load_nist_csf_v2_0 import load_nist_csf_v2_0_data
from loading_routines.load_800_171_r2 import load_800_171_r2_data
from loading_routines.load_cis_csc import load_cis_csc_data
from loading_routines.load_ccm_v4_0_5 import load_ccm_data
from loading_routines.load_nist_privacy import load_nist_privacy_data


class ControlFrameworksData:
    def __init__(self):
        self.frameworks: dict[str, Framework] = {}
        self.category_index: dict[str, Category] = {}
        self.control_index: dict[str, Control] = {}

    def set_all_data(self, frameworks: dict[str, Framework]):
        def index_cats_and_controls(category: Category):
            self.category_index[category.id] = category
            for child in category.categories:
                index_cats_and_controls(child)

            for control in category.controls:
                self.control_index[control.id] = control

        self.frameworks = frameworks

        for framework in self.frameworks.values():
            for category in framework.categories:
                index_cats_and_controls(category)


data: ControlFrameworksData = ControlFrameworksData()


print("Loading data...")

frameworks = {}
load_functions = [
    load_800_171_r2_data,
    load_cis_csc_data,
    load_ccm_data,
    load_nist_csf_v1_1_data,
    load_nist_csf_v2_0_data,
    load_nist_privacy_data,
]

for load_function in load_functions:
    framework: Framework = load_function(uuid4())
    frameworks[framework.id] = framework

data.set_all_data(frameworks)

with open("data.pickle", "wb") as f:
    dill_pickle.dump(data, f)

print("Data loaded and saved to data.pickle")

signature = hmac.new(
    bytes(config["SECRET_KEY"], "utf-8"),
    dill_pickle.dumps(data),
    digestmod="sha256",
)

print("Signature:", signature.hexdigest())
