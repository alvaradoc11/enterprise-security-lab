import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise EnvironmentError(
            f'Missing required env var: {key}. '
            'Copy .env.example to .env and fill in values.'
        )
    return value
