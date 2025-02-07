import fastapi

from llm_gateway.app import app
from llm_gateway.constants import get_settings

print(f"FastAPI version: {fastapi.__version__}")
print(f"Settings loaded: {get_settings()}")
