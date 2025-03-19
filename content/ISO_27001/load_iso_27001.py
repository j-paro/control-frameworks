import json

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models import Framework, Category, Control


def load_iso_27001_data(session: Session):
    print("*** ISO 27001 data load not implemented yet ***")
