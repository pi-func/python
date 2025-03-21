from pifunc import service, run_services

@service(
    http={"path": "/api/add", "method": "POST"}
)
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    print("Starting service at http://localhost:8080/api/add")
    run_services(
        http={"port": 8083},
        watch=True
    )