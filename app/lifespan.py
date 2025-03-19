from contextlib import asynccontextmanager

from app.schemas.mem_data import Framework, Category, Control
from app.loading_routines.load_nist_csf_v1_1 import load_nist_csf_v1_1_data
from app.loading_routines.load_nist_csf_v2_0 import load_nist_csf_v2_0_data
from app.loading_routines.load_800_171_r2 import load_800_171_r2_data
from app.loading_routines.load_cis_csc import load_cis_csc_data
from app.loading_routines.load_ccm_v4_0_5 import load_ccm_data
from app.loading_routines.load_nist_privacy import load_nist_privacy_data


class ControlFrameworksData:
    def __init__(self):
        self.frameworks: dict[str, Framework] = {}
        self.category_index: dict[str, Category] = {}
        self.control_index: dict[str, Control] = {}

    def set_all_data(self, frameworks: dict[str, Framework]):
        def index_cats_and_controls(category: Category):
            self.category_index[category.cat_string_id] = category
            for child in category.categories:
                index_cats_and_controls(child)

            for control in category.controls:
                self.control_index[control.control_string_id] = control

        self.frameworks = frameworks

        for framework in self.frameworks.values():
            for category in framework.categories:
                index_cats_and_controls(category)


data: ControlFrameworksData = ControlFrameworksData()


@asynccontextmanager
async def lifespan(_):
    print("Loading data...")

    id = 0
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
        framework: Framework = load_function()
        frameworks[framework.string_id] = framework

    data.set_all_data(frameworks)

    yield
