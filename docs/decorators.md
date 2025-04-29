Oto zestaw praktycznych przykładów dekoratorów:

1. **Pomiar wydajności**:
```python
import time
from functools import wraps

def performance_measure(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Czas wykonania {func.__name__}: {end_time - start_time:.4f} sekund")
        return result
    return wrapper

@performance_measure
def complex_calculation(n):
    return sum(i**2 for i in range(n))
```

2. **Walidacja argumentów**:
```python
def validate_arguments(**validations):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Sprawdzanie typów i wartości argumentów
            for param, validation in validations.items():
                value = kwargs.get(param)
                if not validation(value):
                    raise ValueError(f"Nieprawidłowa wartość dla {param}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_arguments(
    email=lambda x: '@' in x,
    age=lambda x: 18 <= x <= 120
)
def register_user(email, age, username):
    print(f"Rejestracja użytkownika: {username}")
```

3. **Ponowne próby wykonania (retry)**:
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(f"Próba {attempts} nie powiodła się: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unstable_network_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Błąd połączenia")
    return "Sukces!"
```

4. **Cache z timeoutem**:
```python
from functools import wraps
import time

def timed_cache(timeout=60):
    def decorator(func):
        cache = {}
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            # Sprawdzenie cache
            if (key in cache and 
                current_time - cache[key]['timestamp'] < timeout):
                return cache[key]['result']
            
            # Wywołanie funkcji
            result = func(*args, **kwargs)
            
            # Aktualizacja cache
            cache[key] = {
                'result': result,
                'timestamp': current_time
            }
            
            return result
        return wrapper
    return decorator

@timed_cache(timeout=10)
def expensive_calculation(x, y):
    time.sleep(2)  # Symulacja długotrwałego obliczenia
    return x * y
```

5. **Kontrola dostępu/autoryzacja**:
```python
def authorize(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get('role') != required_role:
                raise PermissionError("Brak uprawnień")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

@authorize(required_role='admin')
def delete_user(user, user_id):
    print(f"Usuwanie użytkownika {user_id}")

# Użycie
admin = User('Admin', 'admin')
user = User('Regular', 'user')

delete_user(admin, 123)  # Powiedzie się
# delete_user(user, 123)  # Zgłosi PermissionError
```

6. **Logowanie zdarzeń**:
```python
import logging
from functools import wraps

def log_event(event_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Zdarzenie {event_type}: Rozpoczęcie")
            try:
                result = func(*args, **kwargs)
                logging.info(f"Zdarzenie {event_type}: Zakończenie sukcesem")
                return result
            except Exception as e:
                logging.error(f"Zdarzenie {event_type}: Błąd - {e}")
                raise
        return wrapper
    return decorator

@log_event('user_registration')
def register_new_user(username, email):
    # Logika rejestracji
    print(f"Rejestracja: {username}")
```

7. **Synchronizacja wielowątkowa**:
```python
import threading
from functools import wraps

def thread_safe(func):
    lock = threading.Lock()
    @wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper

class Counter:
    def __init__(self):
        self._value = 0
    
    @thread_safe
    def increment(self):
        self._value += 1
```

Te przykłady pokazują różnorodność zastosowań dekoratorów:
- Pomiar wydajności
- Walidacja danych
- Ponowne próby wykonania
- Cachowanie
- Kontrola dostępu
- Logowanie
- Synchronizacja

Każdy z nich dodaje dodatkową funkcjonalność bez ingerencji w oryginalny kod funkcji.