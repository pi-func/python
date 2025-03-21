import os
from dotenv import load_dotenv
from pifunc import service, run_services

# Load environment variables from .env file
load_dotenv()


@service(zeromq={"pattern": "REQ_REP", "port": 5555})
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b


@service(zeromq={"pattern": "REQ_REP", "port": 5556})
def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b


@service(zeromq={"pattern": "PUB_SUB", "port": 5557, "interval": 5.0})
def status():
    """Publishes system status periodically."""
    import psutil
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }


@service(zeromq={"pattern": "PUSH_PULL", "port": 5558})
def process_task(task_id: str, data: dict) -> dict:
    """Processes a task asynchronously."""
    # Simulate processing
    import time
    time.sleep(0.5)
    return {
        "task_id": task_id,
        "status": "completed",
        "result": f"Processed data with {len(data)} items"
    }


if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("ZMQ_HOST", "localhost")

    print(f"Starting ZeroMQ services on {host}")

    # You can override ports using environment variables:
    # ZMQ_ADD_PORT, ZMQ_SUBTRACT_PORT, ZMQ_STATUS_PORT, ZMQ_PROCESS_TASK_PORT

    run_services(
        zeromq={"host": host},
        watch=True  # Auto-reload on file changes
    )