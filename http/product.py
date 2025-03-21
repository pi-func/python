from random import randint, choice
from string import ascii_letters

from pifunc import service, client, run_services

@service(
    http={"path": "/api/products", "method": "POST"}
)
def create_product(product: dict) -> dict:
    """Create a new product.

    Note: When working with dictionary parameters, use `dict` instead of `Dict`
    for better type handling across protocols.
    """
    return {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "in_stock": product.get("in_stock", True)
    }


@service(
    http={"path": "/", "method": "GET"}
)
def hello() -> dict:
    return {
        "description": "Create a new product. Note: When working with dictionary parameters, use `dict` instead of `Dict`  for better type handling across protocols.",
        "path": "/api/products",
        "url": "http://127.0.0.1:8080/api/products/",
        "method": "POST",
        "protocol": "HTTP",
        "version": "1.1",
        "data": {"id": "1",
                "name": "test",
                "price": "10",
                "in_stock": True},
    }


@client(
    http={"path": "/api/products", "method": "POST"}
)
@service(
    cron={"interval": "1m"}
)
def generate_product() -> dict:
    return {
        "id": str(randint(1000, 9999)),
        "name": ''.join(choice(ascii_letters) for i in range(8)),
        "price": str(randint(10, 100)),
        "in_stock": True
    }

if __name__ == "__main__":
    # Określamy tylko protokoły, których faktycznie używamy
    run_services(
        http={"port": 8080},
        cron={"check_interval": 1},
        # Wyraźnie określamy dostępne protokoły, pomijając MQTT
        protocols=["http", "cron"],
        watch=True
    )