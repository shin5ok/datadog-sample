# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a FastAPI application with Datadog APM monitoring and tracing. The project uses:

- **FastAPI**: Web framework for the API server
- **Datadog APM**: Application performance monitoring with custom spans and tracing
- **uv**: Python package manager for dependency management
- **Docker**: Containerized deployment with separate containers for app and Datadog agent

## Key Components

- `fastapi-app/main.py`: Main FastAPI application with two endpoints:
  - `/env`: Returns all environment variables and request headers
  - `/env/{key}`: Returns specific environment variable or header by key (case-insensitive)
- Both endpoints include detailed Datadog tracing with custom spans for performance monitoring

## Development Commands

```bash
# Install dependencies
cd fastapi-app && uv sync

# Run the application locally
cd fastapi-app && uv run main.py

# Run with Docker Compose (includes Datadog agent)
docker-compose up --build

# Build Docker image
docker build -f fastapi-app/Dockerfile -t fastapi-app .
```

## Docker Setup

The project uses two Docker containers:
- `app`: FastAPI application (port 8000)
- `datadog`: Datadog agent for APM collection

Environment variables required:
- `DD_API_KEY`: Datadog API key for agent authentication

## Datadog Tracing

The application includes comprehensive APM tracing:
- Service name: `fastapi-app`
- Custom spans for environment variable collection, header parsing, and search operations
- Detailed tagging including operation names, counts, and search results
- Uses `ddtrace.trace.tracer` for span creation and `ddtrace.ext.http` for HTTP-specific tags