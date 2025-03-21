# pifunc/adapters/zeromq_adapter.py
import json
import asyncio
import threading
import time
import inspect
from typing import Any, Callable, Dict, List, Optional
import zmq
import zmq.asyncio
from pifunc.adapters import ProtocolAdapter


class ZeroMQAdapter(ProtocolAdapter):
    """Adapter protokołu ZeroMQ."""

    def __init__(self):
        self.context = None
        self.functions = {}
        self.config = {}
        self.sockets = {}
        self.running = False
        self.server_threads = []

    def setup(self, config: Dict[str, Any]) -> None:
        """Konfiguruje adapter ZeroMQ."""
        self.config = config

        # Tworzymy kontekst ZeroMQ
        self.context = zmq.Context()

    def register_function(self, func: Callable, metadata: Dict[str, Any]) -> None:
        """Rejestruje funkcję jako endpoint ZeroMQ."""
        service_name = metadata.get("name", func.__name__)

        # Pobieramy konfigurację ZeroMQ
        zmq_config = metadata.get("zeromq", {})

        # Określamy typ wzorca komunikacji
        pattern = zmq_config.get("pattern", "REQ_REP")
        port = zmq_config.get("port", 0)  # 0 oznacza automatyczne przydzielenie portu
        bind_address = zmq_config.get("bind_address", "tcp://*")
        topic = zmq_config.get("topic", service_name)

        # Zapisujemy informacje o funkcji
        self.functions[service_name] = {
            "function": func,
            "metadata": metadata,
            "pattern": pattern,
            "port": port,
            "bind_address": bind_address,
            "topic": topic,
            "socket": None,
            "thread": None
        }

    def _create_socket(self, pattern: str) -> zmq.Socket:
        """Tworzy socket ZeroMQ odpowiedniego typu."""
        if pattern == "REQ_REP":
            return self.context.socket(zmq.REP)
        elif pattern == "PUB_SUB":
            return self.context.socket(zmq.PUB)
        elif pattern == "PUSH_PULL":
            return self.context.socket(zmq.PULL)
        elif pattern == "ROUTER_DEALER":
            return self.context.socket(zmq.ROUTER)
        else:
            raise ValueError(f"Nieobsługiwany wzorzec ZeroMQ: {pattern}")

    def _req_rep_server(self, service_name: str, function_info: Dict[str, Any]):
        """Serwer dla wzorca REQ/REP."""
        socket = self._create_socket("REQ_REP")

        # Bindujemy socket
        if function_info["port"] > 0:
            bind_address = f"{function_info['bind_address']}:{function_info['port']}"
            socket.bind(bind_address)
            actual_port = function_info["port"]
        else:
            # Automatyczne przydzielenie portu
            bind_address = f"{function_info['bind_address']}:*"
            actual_port = socket.bind_to_random_port(bind_address)

        print(f"ZeroMQ REQ/REP serwer dla {service_name} uruchomiony na porcie {actual_port}")

        # Aktualizujemy informację o porcie
        function_info["port"] = actual_port
        function_info["socket"] = socket

        # Główna pętla
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        func = function_info["function"]

        while self.running:
            try:
                # Czekamy na wiadomość z timeoutem
                socks = dict(poller.poll(1000))  # Timeout 1s

                if socket in socks and socks[socket] == zmq.POLLIN:
                    # Odbieramy wiadomość
                    message = socket.recv()

                    try:
                        # Parsujemy JSON
                        kwargs = json.loads(message.decode('utf-8'))

                        # Wywołujemy funkcję
                        result = func(**kwargs)

                        # Obsługujemy coroutines
                        if asyncio.iscoroutine(result):
                            # Tworzymy nową pętlę asyncio
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result = loop.run_until_complete(result)
                            loop.close()

                        # Serializujemy wynik
                        response = json.dumps({
                            "result": result,
                            "service": service_name,
                            "timestamp": time.time()
                        })

                        # Wysyłamy odpowiedź
                        socket.send(response.encode('utf-8'))

                    except json.JSONDecodeError:
                        # Wysyłamy informację o błędzie
                        error_response = json.dumps({
                            "error": "Invalid JSON format",
                            "service": service_name,
                            "timestamp": time.time()
                        })
                        socket.send(error_response.encode('utf-8'))
                    except Exception as e:
                        # Wysyłamy informację o błędzie
                        error_response = json.dumps({
                            "error": str(e),
                            "service": service_name,
                            "timestamp": time.time()
                        })
                        socket.send(error_response.encode('utf-8'))
                        print(f"Błąd podczas przetwarzania wiadomości: {e}")

            except zmq.ZMQError as e:
                print(f"Błąd ZeroMQ: {e}")
                time.sleep(1.0)
            except Exception as e:
                print(f"Nieoczekiwany błąd: {e}")
                time.sleep(1.0)

        # Zamykamy sockety
        socket.close()
        push_socket.close()

    def _router_dealer_server(self, service_name: str, function_info: Dict[str, Any]):
        """Serwer dla wzorca ROUTER/DEALER."""
        socket = self._create_socket("ROUTER_DEALER")

        # Bindujemy socket
        if function_info["port"] > 0:
            bind_address = f"{function_info['bind_address']}:{function_info['port']}"
            socket.bind(bind_address)
            actual_port = function_info["port"]
        else:
            # Automatyczne przydzielenie portu
            bind_address = f"{function_info['bind_address']}:*"
            actual_port = socket.bind_to_random_port(bind_address)

        print(f"ZeroMQ ROUTER serwer dla {service_name} uruchomiony na porcie {actual_port}")

        # Aktualizujemy informację o porcie
        function_info["port"] = actual_port
        function_info["socket"] = socket

        # Główna pętla
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        func = function_info["function"]

        while self.running:
            try:
                # Czekamy na wiadomość z timeoutem
                socks = dict(poller.poll(1000))  # Timeout 1s

                if socket in socks and socks[socket] == zmq.POLLIN:
                    # Odbieramy wiadomość (identyfikator klienta + pusta ramka + dane)
                    client_id, empty, message = socket.recv_multipart()

                    try:
                        # Parsujemy JSON
                        kwargs = json.loads(message.decode('utf-8'))

                        # Wywołujemy funkcję
                        result = func(**kwargs)

                        # Obsługujemy coroutines
                        if asyncio.iscoroutine(result):
                            # Tworzymy nową pętlę asyncio
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result = loop.run_until_complete(result)
                            loop.close()

                        # Serializujemy wynik
                        response = json.dumps({
                            "result": result,
                            "service": service_name,
                            "timestamp": time.time()
                        })

                        # Wysyłamy odpowiedź z zachowaniem formatu multipart
                        socket.send_multipart([client_id, empty, response.encode('utf-8')])

                    except json.JSONDecodeError:
                        # Wysyłamy informację o błędzie
                        error_response = json.dumps({
                            "error": "Invalid JSON format",
                            "service": service_name,
                            "timestamp": time.time()
                        })
                        socket.send_multipart([client_id, empty, error_response.encode('utf-8')])
                    except Exception as e:
                        # Wysyłamy informację o błędzie
                        error_response = json.dumps({
                            "error": str(e),
                            "service": service_name,
                            "timestamp": time.time()
                        })
                        socket.send_multipart([client_id, empty, error_response.encode('utf-8')])
                        print(f"Błąd podczas przetwarzania wiadomości: {e}")

            except zmq.ZMQError as e:
                print(f"Błąd ZeroMQ: {e}")
                time.sleep(1.0)
            except Exception as e:
                print(f"Nieoczekiwany błąd: {e}")
                time.sleep(1.0)

        # Zamykamy socket
        socket.close()

    def start(self) -> None:
        """Uruchamia adapter ZeroMQ."""
        if self.running:
            return

        self.running = True

        # Uruchamiamy serwery dla wszystkich zarejestrowanych funkcji
        for service_name, function_info in self.functions.items():
            pattern = function_info["pattern"]

            # Wybieramy odpowiedni typ serwera
            if pattern == "REQ_REP":
                thread = threading.Thread(
                    target=self._req_rep_server,
                    args=(service_name, function_info)
                )
            elif pattern == "PUB_SUB":
                thread = threading.Thread(
                    target=self._pub_sub_server,
                    args=(service_name, function_info)
                )
            elif pattern == "PUSH_PULL":
                thread = threading.Thread(
                    target=self._push_pull_server,
                    args=(service_name, function_info)
                )
            elif pattern == "ROUTER_DEALER":
                thread = threading.Thread(
                    target=self._router_dealer_server,
                    args=(service_name, function_info)
                )
            else:
                print(f"Nieobsługiwany wzorzec ZeroMQ: {pattern}")
                continue

            # Uruchamiamy wątek serwera
            thread.daemon = True
            thread.start()

            # Zapisujemy wątek
            function_info["thread"] = thread
            self.server_threads.append(thread)

        print(f"Adapter ZeroMQ uruchomiony z {len(self.server_threads)} serwerami")

    def stop(self) -> None:
        """Zatrzymuje adapter ZeroMQ."""
        if not self.running:
            return

        self.running = False

        # Czekamy na zakończenie wątków
        for thread in self.server_threads:
            thread.join(timeout=2.0)

        # Zamykamy wszystkie sockety
        for service_name, function_info in self.functions.items():
            socket = function_info.get("socket")
            if socket:
                try:
                    socket.close()
                except:
                    pass

        # Zamykamy kontekst ZeroMQ
        try:
            self.context.term()
        except:
            pass

        self.server_threads = []
        print("Adapter ZeroMQ zatrzymany")
        eroMQ: {e}
        ")
        time.sleep(1.0)

    except Exception as e:
    print(f"Nieoczekiwany błąd: {e}")
    time.sleep(1.0)


# Zamykamy socket
socket.close()


def _pub_sub_server(self, service_name: str, function_info: Dict[str, Any]):
    """Serwer dla wzorca PUB/SUB."""
    # Implementation for PUB/SUB pattern
    # Not fully implemented in this example
    pass


def _push_pull_server(self, service_name: str, function_info: Dict[str, Any]):
    """Serwer dla wzorca PUSH/PULL."""
    socket = self._create_socket("PUSH_PULL")

    # Bindujemy socket
    if function_info["port"] > 0:
        bind_address = f"{function_info['bind_address']}:{function_info['port']}"
        socket.bind(bind_address)
        actual_port = function_info["port"]
    else:
        # Automatyczne przydzielenie portu
        bind_address = f"{function_info['bind_address']}:*"
        actual_port = socket.bind_to_random_port(bind_address)

    print(f"ZeroMQ PULL serwer dla {service_name} uruchomiony na porcie {actual_port}")

    # Aktualizujemy informację o porcie
    function_info["port"] = actual_port
    function_info["socket"] = socket

    # Główna pętla
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    func = function_info["function"]

    # Tworzymy socket do odpowiedzi
    push_socket = self.context.socket(zmq.PUSH)
    push_port = self.config.get("response_port", actual_port + 1)
    push_socket.bind(f"{function_info['bind_address']}:{push_port}")

    while self.running:
        try:
            # Czekamy na wiadomość z timeoutem
            socks = dict(poller.poll(1000))  # Timeout 1s

            if socket in socks and socks[socket] == zmq.POLLIN:
                # Odbieramy wiadomość
                message = socket.recv()

                try:
                    # Parsujemy JSON
                    message_data = json.loads(message.decode('utf-8'))
                    kwargs = message_data.get("data", {})
                    response_id = message_data.get("response_id", None)

                    # Wywołujemy funkcję
                    result = func(**kwargs)

                    # Obsługujemy coroutines
                    if asyncio.iscoroutine(result):
                        # Tworzymy nową pętlę asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(result)
                        loop.close()

                    # Serializujemy wynik
                    response = json.dumps({
                        "result": result,
                        "service": service_name,
                        "timestamp": time.time(),
                        "response_id": response_id
                    })

                    # Wysyłamy odpowiedź
                    push_socket.send(response.encode('utf-8'))

                except json.JSONDecodeError:
                    # Wysyłamy informację o błędzie
                    error_response = json.dumps({
                        "error": "Invalid JSON format",
                        "service": service_name,
                        "timestamp": time.time()
                    })
                    push_socket.send(error_response.encode('utf-8'))
                except Exception as e:
                    # Wysyłamy informację o błędzie
                    error_response = json.dumps({
                        "error": str(e),
                        "service": service_name,
                        "timestamp": time.time()
                    })
                    push_socket.send(error_response.encode('utf-8'))
                    print(f"Błąd podczas przetwarzania wiadomości: {e}")

        except zmq.ZMQError as e:
            print(f"Błąd Z