from random import randint, choice
from string import ascii_letters
import os
import json
from pifunc import service, client, run_services


@service(http={"path": "/api/products", "method": "POST"})
def create_product(product: dict) -> dict:
    """Create a new product."""
    return {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "in_stock": product.get("in_stock", True)
    }

@client(http={"path": "/api/products", "method": "POST"})
@service(cron={"interval": "1m"})
def generate_product() -> dict:
    """Generate a random product every minute."""
    product = {
        "id": str(randint(1000, 9999)),
        "name": ''.join(choice(ascii_letters) for i in range(8)),
        "price": str(randint(10, 100)),
        "in_stock": True
    }
    print(f"Generating random product: {product}")
    return product


if __name__ == "__main__":
    # Protocols are auto-detected, no need to specify them explicitly
    run_services(
        http={"port": 8080},
        cron={"check_interval": 1},
        watch=True
    )

