#!/bin/bash

curl -X POST http://localhost:8083/api/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'

# {"result":8}

curl -X POST http://localhost:8083/api/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 20}'

# {"result":30}