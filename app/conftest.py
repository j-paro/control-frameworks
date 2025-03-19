"""
Put here any Pytest related code (it will be executed before `app/tests/...`)
"""

import os

# This will ensure using test database
os.environ["ENVIRONMENT"] = "PYTEST"
