# 📧 Gmail MCP Server

A Model Context Protocol (MCP) server that provides Gmail capabilities to AI assistants like Claude Desktop or IDEs like Cursor. This server enables your AI to read messages, list emails, send emails, and download attachments using the Gmail API.

## ✨ Features

- **List Messages**: Retrieve recent emails from your inbox.
- **Get Message**: Read the full content of specific emails.
- **Send Message**: Compose and send emails to recipients.
- **Download Attachments**: Access files attached to emails.
- **Dual Transport**: Supports both HTTP (SSE) and Stdio (Standard Input/Output) transports.
- **Docker Support**: Fully containerized for easy deployment.

## 📋 Prerequisites

- **Python 3.12+** installed.
- **Docker** (optional, recommended for isolation).
- **Google Cloud Platform (GCP) Account** with the Gmail API enabled.

## ⚙️ Setup & Configuration

### 1. Google Cloud Credentials
1.  Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2.  Enable the **Gmail API**.
3.  Configure the **OAuth Consent Screen** (add your email as a test user if in Testing mode).
4.  Go to **Credentials** -> **Create Credentials** -> **OAuth Client ID** (Application type: Desktop App).
5.  Download the JSON credential file.

### 2. Configure Local Secrets
The application looks for secrets in `~/run/secrets`. You need to create this directory and place your credentials there.

```bash
# Create the directory
mkdir -p ~/run/secrets

# Move and rename your downloaded JSON file
mv /path/to/downloaded-credentials.json ~/run/secrets/dogsjgp_dev_gcp_gmail_mcp_server.json
```

### 3. Generate OAuth Token
Before running the server (locally or in Docker), you must authenticate once to generate the `token.json`.

```bash
# Install dependencies
pip install -r src/utils/requirements.txt

# Run the authentication script (this will open your browser)
python -m src.utils.utils
```
*This generates `~/run/secrets/token.json`.*

## Running the Server

### Option A: Using Docker Compose (Recommended)

This method uses Docker Secrets to securely mount your credentials.

1.  **Start the Service:**
    ```bash
    docker-compose up --build
    ```
    The server will be available at `http://localhost:3085/sse`.

### Option B: Using Docker (Manual)

1.  **Build the Image:**
    ```bash
    docker build -t gmail-mcp .
    ```

2.  **Run the Container:**
    You must mount your local secrets directory so the container can access the `token.json` you generated.
    ```bash
    docker run -p 3085:3085 \
      -v ~/run/secrets:/home/mcp_gmail_assist/run/secrets \
      gmail-mcp
    ```
    The server will be available at `http://localhost:3085/sse`.

### Option C: Running with Docker Swarm (Service)

To use proper Docker Secrets in a production-like environment using `docker service`:

1.  **Initialize Swarm** (if not already active):
    ```bash
    docker swarm init
    ```

2.  **Create Secrets:**
    ```bash
    docker secret create token_json ~/run/secrets/token.json
    docker secret create credentials_json ~/run/secrets/dogsjgp_dev_gcp_gmail_mcp_server.json
    ```

3.  **Create Service:**
    ```bash
    docker service create --name gmail-mcp \
      --secret source=token_json,target=token.json \
      --secret source=credentials_json,target=dogsjgp_dev_gcp_gmail_mcp_server.json \
      --publish 3085:3085 \
      gmail-mcp
    ```

### Option D: Running Locally (Python)

1.  **Install Dependencies:**
    ```bash
    pip install -r src/utils/requirements.txt
    ```

2.  **Start HTTP Server:**
    ```bash
    python -m src.core.http_transport
    ```
    *You can configure the host and port in `http-config.json`.*

3.  **Start Stdio Mode:** (For direct piping)
    ```bash
    python -m src.core.stdio_transport
    ```

## Connecting to Claude Desktop

To use this server with Claude Desktop, you need to edit your configuration file.

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the following entry under `mcpServers`.

**If running via Docker (HTTP):**
```json
{
  "mcpServers": {
    "gmail-mcp": {
      "url": "http://localhost:3085/sse",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Project Structure

*   **`src/core/`**: Contains the main server logic (`server.py`) and transport layers (`http_transport.py`, `stdio_transport.py`).
*   **`src/tools/`**: Contains specific handlers for Gmail API operations.
*   **`src/utils/`**: Utilities for authentication and token generation.
*   **`http-config.json`**: Configuration file for the HTTP server port and host.
*   **`Dockerfile`**: Instructions for building the Docker image.

---
*Built with FastMCP*
*Improved using Gemini Code Assist*
