"""
Math service demonstrating various mathematical operations through multiple protocols.
"""
from pifunc import http, mqtt, websocket, grpc

@http("/api/math/factorial")
@mqtt("math/factorial")
@websocket("math.factorial")
@grpc("math.factorial")
def factorial(n: int) -> int:
    """Calculate factorial of a number using recursion."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

@http("/api/math/fibonacci")
@mqtt("math/fibonacci")
@websocket("math.fibonacci")
@grpc("math.fibonacci")
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number using dynamic programming."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

@http("/api/math/newton-sqrt")
@mqtt("math/newton-sqrt")
@websocket("math.newton-sqrt")
@grpc("math.newton-sqrt")
def newton_sqrt(n: float, precision: float = 1e-10) -> float:
    """Calculate square root using Newton's method."""
    if n < 0:
        raise ValueError("Square root is not defined for negative numbers")
    if n == 0:
        return 0
    
    x = n
    while True:
        root = 0.5 * (x + n / x)
        if abs(root - x) < precision:
            return root
        x = root

if __name__ == "__main__":
    print("Math Service started. Available protocols:")
    print("- HTTP on port 8001")
    print("- WebSocket on port 8081")
    print("- MQTT on port 1883")
    print("- gRPC on port 50051")
