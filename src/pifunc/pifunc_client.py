# pifunc/pifunc_client.py
import json
import requests


class PiFuncClient:
    """Klient do komunikacji z usługami pifunc."""

    def __init__(self, base_url: str = "http://localhost:8080", protocol: str = "http"):
        """
        Inicjalizuje klienta pifunc.

        Args:
            base_url: Bazowy URL serwera dla protokołu HTTP
            protocol: Domyślny protokół komunikacji ('http', 'grpc', 'zeromq', 'amqp', 'graphql')
        """
        self.base_url = base_url
        self.protocol = protocol.lower()

        # Inicjalizujemy sesję HTTP
        self._http_session = requests.Session()

    def call(self, service_name: str, args=None, **kwargs):
        """
        Wywołuje zdalną usługę.

        Args:
            service_name: Nazwa usługi do wywołania
            args: Argumenty do przekazania usłudze
            **kwargs: Dodatkowa konfiguracja specyficzna dla protokołu

        Returns:
            Wynik wywołania usługi
        """
        if args is None:
            args = {}

        # Określamy protokół
        protocol = kwargs.get('protocol', self.protocol)

        # Wywołujemy usługę według wybranego protokołu
        if protocol == "http":
            path = kwargs.get("path", f"/api/{service_name}")
            method = kwargs.get("method", "POST")

            url = f"{self.base_url}{path}"

            if method.upper() == "GET":
                response = self._http_session.get(url, params=args)
            else:
                response = self._http_session.post(url, json=args)

            response.raise_for_status()
            return response.json()
        else:
            raise ValueError(f"Protokół {protocol} nie jest jeszcze obsługiwany")

    def close(self):
        """Zamyka wszystkie połączenia."""
        # Zamykamy sesję HTTP
        self._http_session.close()