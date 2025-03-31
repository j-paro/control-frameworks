from contextlib import asynccontextmanager
import dill as dill_pickle

from app.schemas.mem_data import ControlFrameworksData


data: ControlFrameworksData = ControlFrameworksData()


@asynccontextmanager
async def lifespan(_):
    with open("data.pickle", "rb") as f:
        file_data: ControlFrameworksData = dill_pickle.load(f)

    data.set_frameworks(file_data.frameworks)
    data.set_category_index(file_data.category_index)
    data.set_control_index(file_data.control_index)

    yield
