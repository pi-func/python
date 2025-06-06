# PI func -> Protocol Interface Functions

PIfunc revolutionizes how you build networked applications by letting you **write your function once** and expose it via **multiple communication protocols simultaneously**. No duplicate code. No inconsistencies. Just clean, maintainable, protocol-agnostic code.

<div align="center">
  <h3>One function, every protocol. Everywhere.</h3>
</div>

## 🚀 Installation

```bash
pip install pifunc
```

## 📚 Quick Start

```python
from pifunc import service, run_services

@service(
    http={"path": "/api/add", "method": "POST"},
    websocket={"event": "math.add"},
    grpc={}
)
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    run_services(
        http={"port": 8080},
        websocket={"port": 8081},
        grpc={"port": 50051},
        watch=True  # Auto-reload on code changes
    )
```

Now your function is accessible via:
- HTTP: `POST /api/add` with JSON body `{"a": 5, "b": 3}`
- WebSocket: Send event `math.add` with payload `{"a": 5, "b": 3}`
- gRPC: Call the `add` method with parameters `a=5, b=3`

## 🔌 Supported Protocols

| Protocol | Description | Best For |
|----------|-------------|----------|
| **HTTP/REST** | RESTful API with JSON | Web clients, general API access |
| **gRPC** | High-performance RPC | Microservices, performance-critical systems |
| **MQTT** | Lightweight pub/sub | IoT devices, mobile apps |
| **WebSocket** | Bidirectional comms | Real-time applications, chat |
| **GraphQL** | Query language | Flexible data requirements |
| **ZeroMQ** | Distributed messaging | High-throughput, low-latency systems |
| **AMQP** | Advanced Message Queuing | Enterprise messaging, reliable delivery |
| **Redis** | In-memory data structure | Caching, pub/sub, messaging |
| **CRON** | Scheduled tasks | Periodic jobs, background tasks |

## ✨ Features

- **Multi-Protocol Support**: Expose functions via multiple protocols at once
- **Protocol Auto-Detection**: Just specify configuration for each protocol you want to use
- **Zero Boilerplate**: Single decorator approach with sensible defaults
- **Type Safety**: Automatic type validation and conversion
- **Hot Reload**: Instant updates during development
- **Protocol-Specific Configurations**: Fine-tune each protocol interface
- **Automatic Documentation**: OpenAPI, gRPC reflection, and GraphQL introspection
- **Client Integration**: Built-in client with `@client` decorator for inter-service communication
- **Scheduled Tasks**: CRON-like scheduling with `cron` protocol
- **Environment Variable Control**: Limit available protocols with `PIFUNC_PROTOCOLS`
- **Monitoring & Health Checks**: Built-in observability
- **Enterprise-Ready**: Authentication, authorization, and middleware support

## 📚 Examples

### Complete Product API Example



![img.png](img.png)

![img_1.png](img_1.png)

This demonstrates the power of PIfunc's protocol-agnostic approach - the same function can be exposed via multiple protocols, and clients can interact with services seamlessly across protocol boundaries,
demonstrates protocol filtering, client-service communication with CRON scheduling, and the API landing page:

```python
# product.py
from random import randint, choice
from string import ascii_letters
import os
import json

# Optional: Filter protocols via environment variable
os.environ["PIFUNC_PROTOCOLS"] = "http,cron"

# Import pifunc after setting environment variables
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


@service(http={"path": "/", "method": "GET"})
def hello() -> dict:
    """API landing page with documentation."""
    return {
        "description": "Create a new product API",
        "path": "/api/products",
        "url": "http://127.0.0.1:8080/api/products/",
        "method": "POST",
        "protocol": "HTTP",
        "version": "1.1",
        "example_data": {
            "id": "1",
            "name": "test",
            "price": "10",
            "in_stock": True
        },
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
```

**Key Features Demonstrated:**

1. **Protocol Filtering**: Using environment variables to limit which protocols are loaded (`os.environ["PIFUNC_PROTOCOLS"] = "http,cron"`)

2. **API Creation**: Creating a simple product API with POST endpoint (`/api/products`)

3. **Landing Page**: Providing API documentation via a root endpoint (`/`)

4. **Scheduled Client**: Automatically generating random products every minute using the CRON protocol

5. **Auto Protocol Detection**: The `run_services` function automatically detects which protocols to enable based on service configurations

6. **Simplified Client Syntax**: Using the simplified `@client(http={...})` syntax instead of specifying protocol separately

When you run this example:
* An HTTP server starts on port 8080
* The CRON scheduler begins running
* Every minute, a random product is generated and sent to the `/api/products` endpoint
* You can visit `http://localhost:8080/` to see the API documentation
* You can POST to `http://localhost:8080/api/products` to create products manually



### Parameter Handling

```python
@service(
    http={"path": "/api/products", "method": "POST"},
    mqtt={"topic": "products/create"}
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
```

### Client-Server Pattern

```python
from pifunc import service, client, run_services
import random

# Server-side service
@service(http={"path": "/api/products", "method": "POST"})
def create_product(product: dict) -> dict:
    """Create a new product."""
    return {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "created": True
    }

# Client-side function with scheduled execution
@client(http={"path": "/api/products", "method": "POST"})  # Simplified syntax!
@service(cron={"interval": "1h"})  # Run every hour
def generate_product() -> dict:
    """Generate a random product and send it to the create_product service."""
    return {
        "id": f"PROD-{random.randint(1000, 9999)}",
        "name": f"Automated Product {random.randint(1, 100)}",
        "price": round(random.uniform(10.0, 100.0), 2)
    }

if __name__ == "__main__":
    # Protocols are auto-detected from registered services!
    run_services(
        http={"port": 8080},
        cron={"check_interval": 1},
        watch=True
    )
```

### Protocol Filtering with Environment Variables

```python
# Control available protocols via environment variables
import os
os.environ["PIFUNC_PROTOCOLS"] = "http,cron"  # Only enable HTTP and CRON

from pifunc import service, run_services

@service(
    http={"path": "/api/data"},
    grpc={},          # Will be ignored due to PIFUNC_PROTOCOLS
    websocket={}      # Will be ignored due to PIFUNC_PROTOCOLS
)
def get_data():
    return {"status": "success", "data": [...]}

if __name__ == "__main__":
    # Only HTTP and CRON adapters will be loaded
    run_services(
        http={"port": 8080},
        watch=True
    )
```

### Advanced Configuration

```python
@service(
    # HTTP configuration
    http={
        "path": "/api/users/{user_id}",
        "method": "GET",
        "middleware": [auth_middleware, logging_middleware]
    },
    # MQTT configuration
    mqtt={
        "topic": "users/get",
        "qos": 1,
        "retain": False
    },
    # WebSocket configuration
    websocket={
        "event": "user.get",
        "namespace": "/users"
    },
    # GraphQL configuration
    graphql={
        "field_name": "user",
        "description": "Get user by ID"
    }
)
def get_user(user_id: str) -> dict:
    """Get user details by ID."""
    return db.get_user(user_id)
```

## 🛠️ CLI Usage

PIfunc comes with a powerful command-line interface that lets you interact with services, generate client code, and access documentation without writing additional code.

### Installation

When you install PIfunc, the CLI is automatically available as the `pifunc` command:

```bash
# Install PIfunc
pip install pifunc

# Verify CLI installation
pifunc --help
```

### Calling Functions

The most common use case is calling functions on running PIfunc services:

```bash
# Basic usage - call a function via HTTP (default protocol)
pifunc call add --args '{"a": 5, "b": 3}'

# Expected output:
# 8
```

#### Call Options

```bash
# Specify a different protocol
pifunc call add --protocol grpc --args '{"a": 5, "b": 3}'

# Call a function on a remote host
pifunc call add --host api.example.com --port 443 --args '{"a": 5, "b": 3}'

# Use a different HTTP method (default is POST)
pifunc call get_user --method GET --args '{"user_id": "123"}'

# Specify a custom path (default is /api/{function_name})
pifunc call user_details --path "/users/details" --args '{"id": "123"}'

# Set a longer timeout for long-running operations
pifunc call process_data --args '{"size": "large"}' --timeout 60

# Enable verbose output for debugging
pifunc call add --args '{"a": 5, "b": 3}' --verbose
```

### Generating Client Code

Generate client libraries to interact with PIfunc services programmatically:

```bash
# Generate a Python client
pifunc generate client --language python --output my_client.py

# Generate a client for a specific protocol
pifunc generate client --protocol grpc --language python

# Generate a client for a specific server
pifunc generate client --host api.example.com --port 443
```

The generated client can be used in your code:

```python
from my_client import PiFuncClient

# Create a client instance
client = PiFuncClient()

# Call functions
result = client.add(a=5, b=3)
print(result)  # 8
```

### Documentation Tools

Access and generate documentation for your services:

```bash
# Start an interactive documentation server
pifunc docs serve

# Generate OpenAPI documentation
pifunc docs generate --format openapi --output ./docs

# Generate Markdown documentation
pifunc docs generate --format markdown

# Generate HTML documentation
pifunc docs generate --format html
```

### Examples in Context

#### Example 1: Start a service and call it

Terminal 1:
```bash
# Start the example service
python examples/calculator.py
```

Terminal 2:
```bash
# Call a function on the running service
pifunc call add --args '{"a": 10, "b": 20}'
# Output: 30

# Get service information
pifunc call get_info
# Output: {"name": "Calculator", "version": "1.0.0", "functions": ["add", "subtract", "multiply", "divide"]}
```

#### Example 2: Generate a client and use it in a script

```bash
# Generate a client for the calculator service
pifunc generate client --output calculator_client.py
```

Then in your Python code:

```python
from calculator_client import PiFuncClient

client = PiFuncClient()

# Direct function calls
sum_result = client.add(a=5, b=3)
product = client.multiply(a=4, b=7)

print(f"Sum: {sum_result}, Product: {product}")
```

#### Example 3: View and explore API documentation

```bash
# Start the documentation server
pifunc docs serve

# Browser automatically opens at http://localhost:8000
# You can explore the API interactively
```

### Troubleshooting CLI Usage

If you encounter issues with the CLI:

#### Command not found

```bash
# If 'pifunc' command isn't found, you can run it as:
python -m pifunc.cli call add --args '{"a": 5, "b": 3}'

# Or check if the package is installed in development mode
pip install -e .
```

#### Connection errors

```bash
# If connection to service fails, verify:
# 1. The service is running
# 2. The port is correct
# 3. No firewall is blocking the connection

# Test with verbose mode
pifunc call add --args '{"a": 5, "b": 3}' --verbose
```

#### Wrong function or arguments

```bash
# If you get errors about missing functions or arguments, check:
# 1. The function name is correct
# 2. You're using the right protocol
# 3. Arguments match the expected format

# Get information about available functions
pifunc docs serve
```







## 🧪 Testing

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run specific test categories
pytest tests/test_http_adapter.py
pytest tests/test_integration.py
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

PIfunc is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <p>Built with ❤️ by the PIfunc team and contributors</p>
</div>