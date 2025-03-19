"""
Calculator example demonstrating multiple protocols with pifunc.
"""
import os
from typing import Dict, Union
from pifunc import http, websocket, run_services

@http("/calculator")
def serve_calculator() -> Dict[str, Union[str, bytes]]:
    """Serve the calculator HTML interface."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "static", "index.html")
    
    with open(html_path, 'rb') as f:
        content = f.read()
    
    return {
        "content": content,
        "content_type": "text/html"
    }

@http("/api/calculator/add")
def add_http(a: float, b: float) -> Dict[str, float]:
    """Add two numbers via HTTP."""
    return {"result": a + b}

@websocket("calculator.add")
def add_websocket(a: float, b: float) -> float:
    """Add two numbers via WebSocket."""
    return a + b

@http("/api/calculator/multiply")
@websocket("calculator.multiply")
def multiply(a: float, b: float) -> float:
    """Multiply two numbers - available via both HTTP and WebSocket."""
    return a * b

@http("/api/calculator/divide")
@websocket("calculator.divide")
def divide(a: float, b: float) -> float:
    """Divide two numbers - available via both HTTP and WebSocket."""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

@http("/api/calculator/subtract")
@websocket("calculator.subtract")
def subtract(a: float, b: float) -> float:
    """Subtract two numbers - available via both HTTP and WebSocket."""
    return a - b

if __name__ == "__main__":
    run_services(
        http={"port": 8080},
        websocket={"port": 8081}
    )
