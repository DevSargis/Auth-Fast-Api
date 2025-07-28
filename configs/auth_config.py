import os
from dotenv import load_dotenv

load_dotenv()

AUTH_PROVIDER = os.getenv("AUTH_PROVIDER")
if not AUTH_PROVIDER:
    raise ValueError("AUTH_PROVIDER environment variable is not set")
AUTH_PROVIDER = AUTH_PROVIDER.lower()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
if not CLERK_SECRET_KEY:
    raise ValueError("CLERK_SECRET_KEY environment variable is not set")

CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY", "")
CLERK_JWT_ISSUER = os.getenv("CLERK_JWT_ISSUER", "")
CLERK_API_URL = os.getenv("CLERK_API_URL", "https://api.clerk.dev/v1") 