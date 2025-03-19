"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio
from load_all_data import load_all_data_wrapper


async def main() -> None:
    print("Start initial data")
    await load_all_data_wrapper()


if __name__ == "__main__":
    asyncio.run(main())
