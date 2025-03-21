# PI func -> Protocol Interface Functions

PIfunc revolutionizes how you build networked applications by letting you **write your function once** and expose it via **multiple communication protocols simultaneously**. No duplicate code. No inconsistencies. Just clean, maintainable, protocol-agnostic code.


## 📚 Examples

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

# Call via HTTP:
# POST /api/products
# {"product": {"id": "123", "name": "Widget", "price": 99.99}}

# Call via MQTT:
# Topic: products/create
# Payload: {"product": {"id": "123", "name": "Widget", "price": 99.99}}
```

4. Or use the CLI:

```bash
pifunc call add --protocol http --args '{"a": 5, "b": 3}'
# 8
```


## kill

```bash
pkill -f "python calculator.py" && python calculator.py
```

## ✨ Features

- **Multi-Protocol Support**: Expose functions via HTTP/REST, gRPC, MQTT, WebSocket, and GraphQL
- **Zero Boilerplate**: Single decorator approach with sensible defaults
- **Type Safety**: Automatic type validation and conversion
- **Hot Reload**: Instant updates during development
- **Protocol-Specific Configurations**: Fine-tune each protocol interface
- **Automatic Documentation**: OpenAPI, gRPC reflection, and GraphQL introspection
- **Comprehensive CLI**: Manage and test your services with ease
- **Monitoring & Health Checks**: Built-in observability
- **Enterprise-Ready**: Authentication, authorization, and middleware support

## 🔌 Supported Protocols

| Protocol | Description | Best For |
|----------|-------------|----------|
| **HTTP/REST** | RESTful API with JSON | Web clients, general API access |
| **gRPC** | High-performance RPC | Microservices, performance-critical systems |
| **MQTT** | Lightweight pub/sub | IoT devices, mobile apps |
| **WebSocket** | Bidirectional comms | Real-time applications, chat |
| **GraphQL** | Query language | Flexible data requirements |

## 📚 Examples

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
def get_user(user_id: str) -> dict:  # Use dict instead of Dict
    """Get user details by ID."""
    return db.get_user(user_id)
```

### Debugging and Logging

PIfunc provides detailed logging for both HTTP and MQTT adapters to help with debugging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

@service(
    grpc={"streaming": True},
    websocket={"event": "monitoring.metrics"}
    http={"path": "/api/data", "method": "POST"},
    mqtt={"topic": "data/process"}
)
async def stream_metrics(interval: int = 1):
    """Stream system metrics."""
    while True:
        metrics = get_system_metrics()
        yield metrics
        await asyncio.sleep(interval)
```

### Working with Complex Types

```python
@dataclass
class Product:
    id: str
    name: str
    price: float
    in_stock: bool

@service()
def create_product(product: Product) -> Product:
    """Create a new product."""
    # PIfunc automatically converts JSON to your dataclass
    product.id = generate_id()
    db.save_product(product)
    return product
```

## 🛠️ CLI Usage

PIfunc includes a CLI for interacting with your services:

```bash
# Call a function via HTTP (default protocol)
pifunc call add --args '{"a": 5, "b": 3}'

# Call a function with specific protocol
pifunc call add --protocol http --args '{"a": 5, "b": 3}'

# Get help
pifunc --help
pifunc call --help
```

Note: Additional CLI features like service management, client code generation, documentation viewing, and benchmarking are coming in future releases.

## 📖 Documentation

Comprehensive documentation is available at [https://www.pifunc.com/docs](https://www.pifunc.com/docs)

- [API Reference](https://www.pifunc.com/docs/api-reference)
- [Protocol Configurations](https://www.pifunc.com/docs/protocols)
- [Advanced Usage](https://www.pifunc.com/docs/advanced)
- [Deployment Guide](https://www.pifunc.com/docs/deployment)
- [Extending PIfunc](https://www.pifunc.com/docs/extending)
def process_data(data: dict) -> dict:
    """Process data with detailed logging."""
    return {"processed": data}

## 🧪 Testing

PIfunc includes a comprehensive test suite that ensures reliability across all supported protocols and features:

### CLI Tests
- Command-line interface functionality
- Protocol-specific service calls
- Error handling and edge cases
- Help command documentation

### Service Tests
- Service decorator functionality
- Protocol-specific configurations (HTTP, MQTT, WebSocket)
- Complex data type handling
- Async function support
- Middleware integration

### HTTP Adapter Tests
- Route registration and handling
- Parameter parsing (path, query, body)
- Request/response processing
- Error handling
- CORS support
- Middleware execution

### Integration Tests
- Cross-protocol communication
- Real-world service scenarios
- Data streaming capabilities
- Multi-protocol support validation

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && python -m pip install -e .
# Logs will show:
# - Incoming request/message details
# - Parameter conversion steps
# - Function execution details
# - Response/publication details
# - Any errors or issues that occur
```

To run the tests:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest -v
pytest

# Run specific test categories
pytest tests/test_cli.py
pytest tests/test_service.py
pytest tests/test_http_adapter.py
pytest tests/test_integration.py
```


## PUBLISH


```bash
python -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

```bash
sudo pip install --upgrade pip build twine
pip install --upgrade pip build twine
python -m build
twine check dist/*
twine upload dist/*
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



Generate directory structures from ASCII art or Markdown files.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

---

<div align="center">
  <img src="assets/logo.svg" alt="PIfunc Logo" width="200">
  <h1>PIfunc</h1>
  <p><strong>Protocol Interface Functions</strong></p>
  <p>One function, every protocol. Everywhere.</p>
  
  <p>
    <a href="#installation"><strong>Installation</strong></a> •
    <a href="#quick-start"><strong>Quick Start</strong></a> •
    <a href="#features"><strong>Features</strong></a> •
    <a href="#examples"><strong>Examples</strong></a> •
    <a href="#documentation"><strong>Documentation</strong></a> •
    <a href="#contributing"><strong>Contributing</strong></a> •
    <a href="#license"><strong>License</strong></a>
  </p>
  
  <p>
    <a href="https://github.com/pifunc/pifunc/actions">
      <img src="https://github.com/pifunc/pifunc/workflows/Tests/badge.svg" alt="Tests">
    </a>
    <a href="https://pypi.org/project/pifunc/">
      <img src="https://img.shields.io/pypi/v/pifunc.svg" alt="PyPI">
    </a>
    <a href="https://pepy.tech/project/pifunc">
      <img src="https://pepy.tech/badge/pifunc" alt="Downloads">
    </a>
    <a href="https://github.com/pifunc/pifunc/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/pifunc/pifunc.svg" alt="License">
    </a>
    <a href="https://discord.gg/pifunc">
      <img src="https://img.shields.io/discord/1156621449362239529?color=7289da&label=discord&logo=discord&logoColor=white" alt="Discord">
    </a>
  </p>
</div>


---

---

---

<div align="center">
  <p>Built with ❤️ by the PIfunc team and contributors</p>
  <p>
    <a href="https://www.pifunc.com">Website</a> •
    <a href="https://twitter.com/pifunc">Twitter</a> •
    <a href="https://discord.gg/pifunc">Discord</a>
  </p>
</div>
