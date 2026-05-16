.PHONY: build run stop clean scan help

# Variables
IMAGE_NAME = student-api
IMAGE_TAG = vulnerable
CONTAINER_NAME = student-api-container
PORT = 5000

# Default target
.DEFAULT_GOAL := help

# Build the Docker image
build:
	@echo "Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✅ Image built successfully!"
	@echo "Run 'make run' to start the container"

# Run the Docker container
run:
	@echo "Starting container: $(CONTAINER_NAME)..."
	@docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):5000 \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Container started successfully!"
	@echo "API is running at http://localhost:$(PORT)"
	@echo "Health check: curl http://localhost:$(PORT)/health"

# Stop the running container
stop:
	@echo "Stopping container: $(CONTAINER_NAME)..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✅ Container stopped"

# View container logs
logs:
	@echo "Showing logs for $(CONTAINER_NAME)..."
	docker logs -f $(CONTAINER_NAME)

# Scan image for vulnerabilities using Docker Scout
scan:
	@echo "Scanning image for vulnerabilities..."
	@echo "Using Docker Scout:"
	docker scout cves $(IMAGE_NAME):$(IMAGE_TAG)

# Scan with Trivy (if installed)
scan-trivy:
	@echo "Scanning with Trivy..."
	trivy image $(IMAGE_NAME):$(IMAGE_TAG)

# Clean up containers and images
clean:
	@echo "Cleaning up..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Build and run in one command
up: build run

# Restart the container
restart: stop run

# Show container status
status:
	@echo "Container status:"
	@docker ps -a | grep $(CONTAINER_NAME) || echo "Container not found"

# Test the API
test:
	@echo "Testing API endpoints..."
	@echo "\n1. Health check:"
	@curl -s http://localhost:$(PORT)/health | python3 -m json.tool || echo "API not responding"
	@echo "\n\n2. Get all students:"
	@curl -s http://localhost:$(PORT)/api/students | python3 -m json.tool || echo "API not responding"

# Help command
help:
	@echo "Student API - Makefile Commands"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make build        - Build the Docker image"
	@echo "  make run          - Run the Docker container"
	@echo "  make stop         - Stop and remove the container"
	@echo "  make logs         - View container logs"
	@echo "  make scan         - Scan image for vulnerabilities (Docker Scout)"
	@echo "  make scan-trivy   - Scan image with Trivy"
	@echo "  make clean        - Remove container and image"
	@echo "  make up           - Build and run (build + run)"
	@echo "  make restart      - Restart the container"
	@echo "  make status       - Show container status"
	@echo "  make test         - Test API endpoints"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make build     # Build the image"
	@echo "  2. make run       # Start the container"
	@echo "  3. make scan      # Scan for vulnerabilities"
	@echo ""
	@echo "Or use: make up    # Build and run in one command"