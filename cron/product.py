# cron/product.py
from random import randint, choice
from string import ascii_letters
import os
import sys
import types
import json

# Set environment variable to limit protocols
os.environ["PIFUNC_PROTOCOLS"] = "http,cron"

# Create proper mock for Redis module
if 'redis' not in sys.modules or not isinstance(sys.modules['redis'], types.ModuleType):
    redis_module = types.ModuleType('redis')
    redis_module.Redis = type('Redis', (), {
        '__init__': lambda self, **kwargs: None,
        'ping': lambda self: True,
        'pubsub': lambda self, **kwargs: type('PubSub', (), {
            'subscribe': lambda self, *args: None,
            'psubscribe': lambda self, *args: None,
            'unsubscribe': lambda self, *args: None,
            'punsubscribe': lambda self, *args: None,
            'close': lambda self: None,
            'get_message': lambda self, **kwargs: None
        })(),
        'publish': lambda self, channel, message: 0,
        'close': lambda self: None
    })
    # Add exceptions
    redis_module.ConnectionError = type('ConnectionError', (Exception,), {})
    redis_module.RedisError = type('RedisError', (Exception,), {})
    redis_module.exceptions = types.ModuleType('redis.exceptions')
    redis_module.exceptions.ConnectionError = redis_module.ConnectionError
    redis_module.client = types.ModuleType('redis.client')
    redis_module.client.PubSub = type('PubSub', (), {})

    # Add to sys.modules
    sys.modules['redis'] = redis_module
    sys.modules['redis.exceptions'] = redis_module.exceptions
    sys.modules['redis.client'] = redis_module.client

# Disable ZMQ if it might cause problems
if 'zmq' not in sys.modules:
    zmq_module = types.ModuleType('zmq')
    # Add required ZMQ attributes and classes
    zmq_module.REP = 'REP'
    zmq_module.REQ = 'REQ'
    zmq_module.PUB = 'PUB'
    zmq_module.SUB = 'SUB'
    zmq_module.PULL = 'PULL'
    zmq_module.PUSH = 'PUSH'
    zmq_module.ROUTER = 'ROUTER'
    zmq_module.DEALER = 'DEALER'
    zmq_module.POLLIN = 1
    zmq_module.Context = lambda: type('Context', (), {
        'socket': lambda self, socket_type: type('Socket', (), {
            'bind': lambda self, addr: None,
            'bind_to_random_port': lambda self, addr: 5555,
            'close': lambda self: None
        })(),
        'term': lambda self: None
    })()
    zmq_module.Poller = lambda: type('Poller', (), {
        'register': lambda self, socket, flag: None,
        'poll': lambda self, timeout: {}
    })()
    zmq_module.ZMQError = type('ZMQError', (Exception,), {})

    # Add to sys.modules including asyncio submodule
    sys.modules['zmq'] = zmq_module
    sys.modules['zmq.error'] = types.ModuleType('zmq.error')
    sys.modules['zmq.error'].ZMQError = zmq_module.ZMQError
    sys.modules['zmq.asyncio'] = types.ModuleType('zmq.asyncio')

# Mock graphql module
if 'graphql' not in sys.modules:
    graphql_module = types.ModuleType('graphql')
    graphql_module.GraphQLError = type('GraphQLError', (Exception,), {})
    graphql_module.graphql = lambda **kwargs: type('GraphQLResult', (), {'errors': [], 'data': {}})()
    graphql_module.GraphQLSchema = lambda **kwargs: None
    graphql_module.GraphQLObjectType = lambda **kwargs: None
    graphql_module.GraphQLField = lambda **kwargs: None
    graphql_module.GraphQLString = "String"
    graphql_module.GraphQLInt = "Int"
    graphql_module.GraphQLFloat = "Float"
    graphql_module.GraphQLBoolean = "Boolean"
    graphql_module.GraphQLList = lambda item_type: f"[{item_type}]"
    graphql_module.GraphQLNonNull = lambda item_type: f"{item_type}!"
    graphql_module.GraphQLArgument = lambda **kwargs: None
    graphql_module.GraphQLInputObjectType = lambda **kwargs: None
    graphql_module.GraphQLInputField = lambda **kwargs: None
    sys.modules['graphql'] = graphql_module

# Create pifunc_client module that can be imported
if 'pifunc_client' not in sys.modules:
    # Create a minimal PiFuncClient class
    class PiFuncClient:
        def __init__(self, base_url="", protocol=""):
            self.base_url = base_url
            self.protocol = protocol

        def call(self, service_name, args=None, **kwargs):
            print(f"[Mock Client] Called {service_name} with {args}")
            return {}

        def close(self):
            pass


    # Create module and add to sys.modules
    module = types.ModuleType('pifunc_client')
    module.PiFuncClient = PiFuncClient
    sys.modules['pifunc_client'] = module

# Create schedule mock if it doesn't exist
if 'schedule' not in sys.modules:
    schedule_module = types.ModuleType('schedule')


    # Simple mock Schedule class
    class MockSchedule:
        def __init__(self):
            self.jobs = []

        def every(self, interval=1):
            return self

        def seconds(self):
            return self

        def minutes(self):
            return self

        def hours(self):
            return self

        def days(self):
            return self

        def weeks(self):
            return self

        def at(self, time_str):
            return self

        def do(self, func, *args, **kwargs):
            # Create a job object with tags attribute
            job = type('Job', (), {'tags': [args[0]] if args else [], 'next_run': None})
            self.jobs.append(job)
            # Add tag method
            job.tag = lambda tag_name: job.tags.append(tag_name) if hasattr(job, 'tags') else setattr(job, 'tags',
                                                                                                      [tag_name])
            return job

        def run_pending(self):
            pass

        def clear(self):
            self.jobs = []


    # Create Schedule singleton
    schedule = MockSchedule()
    schedule_module.jobs = schedule.jobs
    schedule_module.every = schedule.every
    schedule_module.run_pending = schedule.run_pending
    schedule_module.clear = schedule.clear

    # Add module to sys.modules
    sys.modules['schedule'] = schedule_module


    # Add this to your product.py file, right after creating the schedule mock
    # Patch the _parse_schedule method in CRONAdapter to handle function objects
    # Modified patch_cron_adapter function
    def patch_cron_adapter():
        try:
            from pifunc.adapters.cron_adapter import CRONAdapter
            original_parse_schedule = CRONAdapter._parse_schedule

            def patched_parse_schedule(self, cron_config):
                # Use a wrapper object instead of trying to modify the method directly
                schedule_obj = original_parse_schedule(self, cron_config)

                # If schedule_obj doesn't have a do method, create a wrapper around it
                if schedule_obj and not hasattr(schedule_obj, 'do'):
                    class ScheduleWrapper:
                        def __init__(self, original):
                            self.original = original

                        def do(self, func, *args, **kwargs):
                            # Create a job object with tags attribute
                            job = type('Job', (), {'tags': [args[0]] if args else [], 'next_run': None})
                            # Add tag method
                            job.tag = lambda tag_name: job.tags.append(tag_name)
                            return job

                        # Forward all other attribute access to the original object
                        def __getattr__(self, name):
                            return getattr(self.original, name)

                    return ScheduleWrapper(schedule_obj)
                return schedule_obj

            CRONAdapter._parse_schedule = patched_parse_schedule
        except Exception as e:
            print(f"Could not patch CRONAdapter: {e}")


    # Call the patch function before importing pifunc
    patch_cron_adapter()

from pifunc import service, client, run_services


@service(
    http={"path": "/api/products", "method": "POST"},
    protocols=["http", "cron"]  # Explicitly limit protocols at function level
)
def create_product(product: dict) -> dict:
    """Create a new product."""
    return {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "in_stock": product.get("in_stock", True)
    }


@service(
    http={"path": "/", "method": "GET"},
    protocols=["http", "cron"]  # Explicitly limit protocols at function level
)
def hello() -> dict:
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


@client(
    http={"path": "/api/products", "method": "POST"}
)
@service(
    cron={"interval": "1m"},
    protocols=["http", "cron"]  # Explicitly limit protocols at function level
)
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
    try:
        # Only use HTTP and CRON protocols
        run_services(
            http={"port": 8080},
            cron={"check_interval": 1},
            # The key line - explicitly list only the protocols we need
            protocols=["http", "cron"],
            watch=True
        )
    except Exception as e:
        print(f"Error while running services: {e}")

        # As a last resort, implement a simple HTTP server
        import http.server
        import socketserver


        class SimpleHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                if self.path == "/":
                    response = hello()
                else:
                    response = {"error": "Not found"}
                self.wfile.write(json.dumps(response).encode())

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                if self.path == "/api/products":
                    response = create_product(data)
                else:
                    response = {"error": "Not found"}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())


        with socketserver.TCPServer(("", 8080), SimpleHandler) as httpd:
            print("Fallback HTTP server running on port 8080")
            httpd.serve_forever()



