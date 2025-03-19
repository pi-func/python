# PI func -> Protocol Interface Functions

PIfunc revolutionizes how you build networked applications by letting you **write your function once** and expose it via **multiple communication protocols simultaneously**. No duplicate code. No inconsistencies. Just clean, maintainable, protocol-agnostic code.

```python
@service(
    http={"path": "/api/calculator/add", "method": "POST"},
    mqtt={"topic": "calculator/add"},
    websocket={"event": "calculator.add"}
)
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
```

## 🚀 This simple function is now simultaneously available via:

- HTTP/REST
- gRPC
- MQTT
- WebSocket
- GraphQL

...all without writing a single line of additional code!

![pifunc-graph.png](pifunc-graph.png)

## 📦 Installation

Install from PyPI:

```bash
pip install pifunc
```

Or install with specific protocol support:

```bash
pip install pifunc[http,mqtt,websocket]
```

## 🏁 Quick Start

1. Create a file `calculator.py`:

```python
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
        grpc={"port": 50051},
        http={"port": 8080},
        watch=True  # Auto-reload on file changes
    )
```

2. Run your service:

```bash
python calculator.py
```

3. Call your functions via HTTP:

```bash
curl -X POST http://localhost:8080/api/add -H "Content-Type: application/json" -d '{"a": 5, "b": 3}'
curl -X POST http://localhost:8080/api/subtract -H "Content-Type: application/json" -d '{"a": 5, "b": 3}'
# {"result": 8}
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
def get_user(user_id: str) -> Dict:
    """Get user details by ID."""
    return db.get_user(user_id)
```

### Streaming Data

```python
@service(
    grpc={"streaming": True},
    websocket={"event": "monitoring.metrics"}
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
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && python3 -m pip install -e .
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
