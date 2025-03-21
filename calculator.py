import os
from pifunc import service, run_services
# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not installed, using default environment variables")

# Get configuration from environment variables with defaults
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 8080))


@service(http={"path": "/api/add"})
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b


@service(http={"path": "/api/subtract"})
def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b


if __name__ == "__main__":
    print(f"Starting API service on {API_HOST}:{API_PORT}")
    run_services(
        http={"host": API_HOST, "port": API_PORT},
        watch=True  # Auto-reload on file changes
    )