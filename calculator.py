from pifunc import service, run_services

@service()
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@service()
def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b

if __name__ == "__main__":
    run_services(
        http={"port": 8080},
        watch=True  # Auto-reload on file changes
    )
