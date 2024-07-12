import os

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.main:create_app",
    )
