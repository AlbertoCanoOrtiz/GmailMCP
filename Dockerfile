# Use a slim python image for efficiency
FROM python:3.12-slim-bookworm

# Prevent python from buffering stdout/stderr so logs show immediately
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies if necessary (git is sometimes needed for dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m mcp_gmail_assist

# Copy only requirements to leverage Docker cache
COPY src/utils/requirements.txt ./
RUN pip install --no-cache-dir -r src/utils/requirements.txt

# Copy the rest of the application source code
COPY src/ ./src/

USER mcp_gmail_assist

# Expose the port (matching http_transport.py)
EXPOSE 3085

CMD ["python", "-m", "src.core.http_transport"]