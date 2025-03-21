"""
pifunc - Generate directory structures from ASCII art or Markdown files.
"""

# from .cli import main
# Próbujemy zaimportować klienta, jeśli nie ma go, tworzymy stub
try:
    from pifunc_client import PiFuncClient
except ImportError:
    # Tworzymy prosty stub klienta jako workaround
    class PiFuncClient:
        def __init__(self, base_url="", protocol=""):
            self.base_url = base_url
            self.protocol = protocol

        def call(self, service_name, args=None, **kwargs):
            print(f"Warning: PiFuncClient stub called for {service_name}")
            return {}

from functools import wraps
import inspect
import sys
import os
import signal
import importlib.util
from typing import Any, Callable, Dict, List, Optional, Set, Type
import importlib

__version__ = "0.1.11"
__all__ = ["service", "run_services", "load_module_from_file", "pifunc_client", "PiFuncClient",
           "http", "websocket", "grpc", "mqtt", "zeromq", "redis", "amqp", "graphql", "cron"]

# Rejestr wszystkich zarejestrowanych funkcji
_SERVICE_REGISTRY = {}
_CLIENT_REGISTRY = {}

# Dictionary to store adapter classes
_ADAPTER_CLASSES = {}

# Get enabled protocols from environment
_ENABLED_PROTOCOLS = set(os.environ.get("PIFUNC_PROTOCOLS", "").lower().split(",")) or None


def _import_adapter(protocol_name):
    """Conditionally import adapter only when needed"""
    if protocol_name in _ADAPTER_CLASSES:
        return _ADAPTER_CLASSES[protocol_name]

    # Skip if protocol is explicitly disabled
    if _ENABLED_PROTOCOLS is not None and protocol_name not in _ENABLED_PROTOCOLS:
        print(f"Protocol {protocol_name} is disabled by PIFUNC_PROTOCOLS environment variable")
        return None

    adapter_module_name = f"pifunc.adapters.{protocol_name}_adapter"
    adapter_class_name = f"{protocol_name.capitalize()}Adapter"

    try:
        module = importlib.import_module(adapter_module_name)
        adapter_class = getattr(module, adapter_class_name)
        _ADAPTER_CLASSES[protocol_name] = adapter_class
        return adapter_class
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not import {adapter_module_name}: {e}")
        return None


def http(path, method="GET"):
    """HTTP route decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store HTTP configuration in function metadata
        wrapper._pifunc_http = {
            "path": path,
            "method": method
        }
        return wrapper

    return decorator


def websocket(event):
    """WebSocket event decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store WebSocket configuration in function metadata
        wrapper._pifunc_websocket = {
            "event": event
        }
        return wrapper

    return decorator


def grpc(service_name=None, method=None, streaming=False):
    """gRPC service decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store gRPC configuration in function metadata
        wrapper._pifunc_grpc = {
            "service_name": service_name or func.__name__,
            "method": method or func.__name__,
            "streaming": streaming
        }
        return wrapper

    return decorator


def mqtt(topic, qos=0):
    """MQTT topic decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store MQTT configuration in function metadata
        wrapper._pifunc_mqtt = {
            "topic": topic,
            "qos": qos
        }
        return wrapper

    return decorator


def zeromq(socket_type="REP", identity=None):
    """ZeroMQ socket decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store ZeroMQ configuration in function metadata
        wrapper._pifunc_zeromq = {
            "socket_type": socket_type,
            "identity": identity or func.__name__
        }
        return wrapper

    return decorator


def redis(channel=None, pattern=None, command=None):
    """Redis pub/sub or command decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store Redis configuration in function metadata
        wrapper._pifunc_redis = {
            "channel": channel,
            "pattern": pattern,
            "command": command or func.__name__
        }
        return wrapper

    return decorator


def amqp(queue=None, exchange=None, routing_key=None, exchange_type="direct"):
    """AMQP (RabbitMQ) decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store AMQP configuration in function metadata
        wrapper._pifunc_amqp = {
            "queue": queue or func.__name__,
            "exchange": exchange or "",
            "routing_key": routing_key or func.__name__,
            "exchange_type": exchange_type
        }
        return wrapper

    return decorator


def graphql(field_name=None, is_mutation=False, description=None):
    """GraphQL field decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store GraphQL configuration in function metadata
        wrapper._pifunc_graphql = {
            "field_name": field_name or func.__name__,
            "is_mutation": is_mutation,
            "description": description or func.__doc__ or ""
        }
        return wrapper

    return decorator


def cron(interval=None, at=None, cron_expression=None, description=None):
    """CRON job decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store CRON configuration in function metadata
        config = {}
        if interval:
            config["interval"] = interval
        if at:
            config["at"] = at
        if cron_expression:
            config["cron_expression"] = cron_expression
        if description:
            config["description"] = description or func.__doc__ or ""

        wrapper._pifunc_cron = config
        return wrapper

    return decorator


def client(
        protocol=None,
        service=None,
        **protocol_configs
):
    """
    Dekorator służący do rejestracji funkcji jako klienta usługi.

    Args:
        protocol: Protokół, przez który ma być wywołana usługa (http, grpc, zeromq, itd.).
        service: Nazwa usługi docelowej (domyślnie nazwa funkcji).
        **protocol_configs: Konfiguracje dla konkretnego protokołu.

    Returns:
        Dekorowana funkcja.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Ustalamy nazwę usługi docelowej
        target_service = service or func.__name__

        # Zbieramy metadane o funkcji klienckiej
        metadata = {
            "name": func.__name__,
            "target_service": target_service,
            "function": func,
            "module": func.__module__,
            "file": inspect.getfile(func),
            "_is_client_function": True
        }

        # Ustalamy protokół komunikacji
        if protocol:
            metadata["protocol"] = protocol
            # Dodajemy specyficzną konfigurację protokołu
            metadata[protocol] = protocol_configs

        # Rejestrujemy funkcję w rejestrze klientów
        _CLIENT_REGISTRY[func.__name__] = metadata

        # Ustawiamy atrybut _pifunc_client na dekorowanej funkcji
        wrapper._pifunc_client = metadata

        return wrapper

    return decorator


def service(
        protocols: Optional[List[str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **protocol_configs
):
    """
    Dekorator służący do rejestracji funkcji jako usługi dostępnej przez różne protokoły.

    Args:
        protocols: Lista protokołów, przez które funkcja ma być dostępna.
                  Domyślnie włączone są wszystkie obsługiwane protokoły.
        name: Nazwa usługi (domyślnie nazwa funkcji).
        description: Opis usługi (domyślnie docstring funkcji).
        **protocol_configs: Konfiguracje dla poszczególnych protokołów.
                           Np. http={"path": "/api/add", "method": "POST"}

    Returns:
        Dekorowana funkcja.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Ustalamy nazwę i opis
        service_name = name or func.__name__
        service_description = description or func.__doc__ or ""

        # Ustalamy protokoły
        available_protocols = ["grpc", "http", "mqtt", "websocket", "graphql", "zeromq", "redis", "amqp", "cron"]
        # Filter protocols by environment variable if set
        if _ENABLED_PROTOCOLS is not None:
            available_protocols = [p for p in available_protocols if p in _ENABLED_PROTOCOLS]

        enabled_protocols = protocols or available_protocols

        # Analizujemy sygnaturę funkcji
        signature = inspect.signature(func)

        # Zbieramy metadane o funkcji
        metadata = {
            "name": service_name,
            "description": service_description,
            "function": func,
            "module": func.__module__,
            "file": inspect.getfile(func),
            "signature": {
                "parameters": {},
                "return_annotation": None
            },
            "protocols": enabled_protocols
        }

        # Dodajemy informacje o parametrach
        for param_name, param in signature.parameters.items():
            metadata["signature"]["parameters"][param_name] = {
                "annotation": param.annotation if param.annotation != inspect.Parameter.empty else None,
                "default": None if param.default == inspect.Parameter.empty else param.default
            }

        # Dodajemy informację o typie zwracanym
        metadata["signature"][
            "return_annotation"] = signature.return_annotation if signature.return_annotation != inspect.Parameter.empty else None

        # Sprawdzamy, czy funkcja ma już skonfigurowane protokoły za pomocą dedykowanych dekoratorów
        if hasattr(func, '_pifunc_http'):
            metadata["http"] = func._pifunc_http

        if hasattr(func, '_pifunc_websocket'):
            metadata["websocket"] = func._pifunc_websocket

        if hasattr(func, '_pifunc_grpc'):
            metadata["grpc"] = func._pifunc_grpc

        if hasattr(func, '_pifunc_mqtt'):
            metadata["mqtt"] = func._pifunc_mqtt

        if hasattr(func, '_pifunc_zeromq'):
            metadata["zeromq"] = func._pifunc_zeromq

        if hasattr(func, '_pifunc_redis'):
            metadata["redis"] = func._pifunc_redis

        if hasattr(func, '_pifunc_amqp'):
            metadata["amqp"] = func._pifunc_amqp

        if hasattr(func, '_pifunc_graphql'):
            metadata["graphql"] = func._pifunc_graphql

        if hasattr(func, '_pifunc_cron'):
            metadata["cron"] = func._pifunc_cron

        # Dodajemy także konfigurację przekazaną jako argumenty dekoratora
        for protocol, config in protocol_configs.items():
            if protocol in available_protocols:
                metadata[protocol] = config

        # Sprawdzamy, czy funkcja jest klientem
        if hasattr(func, '_pifunc_client'):
            metadata["client"] = func._pifunc_client
            metadata["_is_client_function"] = True

        # Rejestrujemy funkcję w globalnym rejestrze
        _SERVICE_REGISTRY[service_name] = metadata

        # Ustawiamy atrybut _pifunc_service na dekorowanej funkcji
        wrapper._pifunc_service = metadata

        return wrapper

    # Obsługa przypadku, gdy dekorator jest użyty bez nawiasów
    if callable(protocols):
        func = protocols
        protocols = None
        return decorator(func)

    return decorator


def run_services(**config):
    """
    Uruchamia wszystkie zarejestrowane usługi z podaną konfiguracją.

    Args:
        **config: Konfiguracja dla poszczególnych protokołów i ogólne ustawienia.
                 Np. grpc={"port": 50051}, http={"port": 8080}, watch=True
    """
    # Override enabled protocols from config if provided
    explicit_protocols = config.pop("protocols", None)
    if explicit_protocols:
        global _ENABLED_PROTOCOLS
        _ENABLED_PROTOCOLS = set(explicit_protocols)

    # Tworzymy słownik na adaptery
    adapters = {}
    clients = {}

    # Get the list of protocols we need
    required_protocols = set()

    # Add protocols from config
    for key in config.keys():
        if key in ["http", "websocket", "grpc", "zeromq", "redis", "mqtt", "graphql", "amqp", "cron"]:
            required_protocols.add(key)

    # Add protocols used by registered services
    for protocol in _get_used_protocols():
        required_protocols.add(protocol)

    # Filter by enabled protocols
    if _ENABLED_PROTOCOLS is not None:
        required_protocols = required_protocols.intersection(_ENABLED_PROTOCOLS)

    # Dynamically import only needed adapters
    for protocol in required_protocols:
        adapter_class = _import_adapter(protocol)
        if adapter_class:
            adapters[protocol] = adapter_class()
            print(f"Loaded adapter for protocol: {protocol}")

    # Prepare CRON configuration with clients
    if "cron" in adapters:
        cron_config = config.get("cron", {}).copy() if "cron" in config else {}
        cron_config["clients"] = clients
        config["cron"] = cron_config

    # Konfigurujemy adaptery
    for protocol, adapter in adapters.items():
        if protocol in config:
            adapter.setup(config[protocol])
        else:
            # Używamy domyślnej konfiguracji
            adapter.setup({})

    # Tworzymy klientów dla każdego protokołu
    from pifunc_client import PiFuncClient

    for protocol, adapter in adapters.items():
        # Tworzymy bazowy URL dla klienta w zależności od protokołu
        if protocol == "http":
            host = config.get("http", {}).get("host", "localhost")
            port = config.get("http", {}).get("port", 8080)
            base_url = f"http://{host}:{port}"
            clients[protocol] = PiFuncClient(base_url=base_url, protocol=protocol)

        elif protocol == "grpc":
            host = config.get("grpc", {}).get("host", "localhost")
            port = config.get("grpc", {}).get("port", 50051)
            base_url = f"{host}:{port}"
            clients[protocol] = PiFuncClient(base_url=base_url, protocol=protocol)

        elif protocol == "zeromq":
            host = config.get("zeromq", {}).get("host", "localhost")
            port = config.get("zeromq", {}).get("port", 5555)
            base_url = f"{host}:{port}"
            clients[protocol] = PiFuncClient(base_url=base_url, protocol=protocol)

        elif protocol == "amqp":
            host = config.get("amqp", {}).get("host", "localhost")
            port = config.get("amqp", {}).get("port", 5672)
            base_url = f"{host}:{port}"
            clients[protocol] = PiFuncClient(base_url=base_url, protocol=protocol)

        elif protocol == "graphql":
            host = config.get("graphql", {}).get("host", "localhost")
            port = config.get("graphql", {}).get("port", 8082)
            base_url = f"http://{host}:{port}/graphql"
            clients[protocol] = PiFuncClient(base_url=base_url, protocol=protocol)

    # Rejestrujemy funkcje w adapterach
    for service_name, metadata in _SERVICE_REGISTRY.items():
        enabled_protocols = metadata.get("protocols", [])
        # Filter by globally enabled protocols
        if _ENABLED_PROTOCOLS is not None:
            enabled_protocols = [p for p in enabled_protocols if p in _ENABLED_PROTOCOLS]

        for protocol in enabled_protocols:
            if protocol in adapters:
                adapters[protocol].register_function(metadata["function"], metadata)

    # Rejestrujemy funkcje klienckie w adapterze CRON
    if "cron" in adapters:
        # Aktualizujemy klientów w konfiguracji CRON
        adapters["cron"].config["clients"] = clients

        # Rejestrujemy funkcje klienckie
        for client_name, metadata in _CLIENT_REGISTRY.items():
            if "_is_client_function" in metadata:
                adapters["cron"].register_function(metadata["function"], metadata)

    # Uruchamiamy adaptery
    for protocol, adapter in adapters.items():
        try:
            adapter.start()
        except Exception as e:
            print(f"Error starting {protocol} adapter: {e}")
            # Don't fail completely if one adapter fails

    # Jeśli włączone jest watchowanie, uruchamiamy wątek monitorujący
    if config.get("watch", False):
        _start_file_watcher(adapters)

    # Konfigurujemy handler dla sygnałów, aby graceful shutdown
    def handle_signal(signum, frame):
        print("Zatrzymywanie serwerów...")
        for adapter in adapters.values():
            adapter.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print(f"Uruchomiono {len(_SERVICE_REGISTRY)} usług przez {len(adapters)} protokołów.")

    # Blokujemy główny wątek
    try:
        while True:
            # Używamy signal.pause() zamiast sleep, aby lepiej reagować na sygnały
            if hasattr(signal, 'pause'):
                signal.pause()
            else:
                # W systemach, które nie obsługują signal.pause()
                import time
                time.sleep(3600)
    except KeyboardInterrupt:
        handle_signal(None, None)


def _get_used_protocols() -> Set[str]:
    """Zwraca zbiór protokołów używanych przez zarejestrowane usługi."""
    used_protocols = set()

    for metadata in _SERVICE_REGISTRY.values():
        used_protocols.update(metadata.get("protocols", []))

    return used_protocols


def _start_file_watcher(adapters):
    """Uruchamia wątek monitorujący zmiany w plikach."""
    import threading
    import time

    def watch_files():
        file_times = {}

        # Zbieramy pliki, w których zdefiniowane są usługi
        for metadata in _SERVICE_REGISTRY.values():
            file_path = metadata.get("file")
            if file_path and os.path.exists(file_path):
                file_times[file_path] = os.path.getmtime(file_path)

        while True:
            # Sprawdzamy, czy któryś plik został zmodyfikowany
            changed = False
            for file_path in list(file_times.keys()):
                try:
                    mtime = os.path.getmtime(file_path)

                    # Jeśli plik został zmodyfikowany
                    if file_times[file_path] < mtime:
                        print(f"Plik {file_path} został zmodyfikowany. Przeładowywanie...")
                        file_times[file_path] = mtime
                        changed = True
                except:
                    pass

            # Jeśli jakiś plik został zmodyfikowany, przeładowujemy serwery
            if changed:
                # Zatrzymujemy wszystkie adaptery
                for adapter in adapters.values():
                    adapter.stop()

                # Restartujemy proces
                os.execv(sys.executable, [sys.executable] + sys.argv)

            time.sleep(1)

    thread = threading.Thread(target=watch_files, daemon=True)
    thread.start()


# Funkcja do załadowania modułu z pliku
def load_module_from_file(file_path):
    """Ładuje moduł z pliku."""
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module