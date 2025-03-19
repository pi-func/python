FROM python:3.11-slim

WORKDIR /app

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for HTTP, WebSocket, and gRPC
EXPOSE 8001 8081 50051

# Run the calculator service
CMD ["python", "-m", "service"]
