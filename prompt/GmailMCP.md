**Role:**
You are a Senior Python Software Engineer specializing in the Model Context Protocol (MCP), Docker containerization, and Google APIs.

**Objective:**
Build a production-grade MCP Server for Gmail functionality using Python's `fastmcp` framework. The project must support both local Stdio transport and Docker-based HTTP/SSE transport.

**Tech Stack:**
*   **Language:** Python 3.12+
*   **Framework:** `fastmcp`
*   **HTTP Client:** `httpx` (Async)
*   **Auth:** `google-auth`, `google-auth-oauthlib`
*   **Containerization:** Docker & Docker Compose (using Secrets)

**Project Structure:**
Please generate the code for the following file structure:
```text
.
├── Dockerfile
├── docker-compose.yaml
├── http-config.json
├── README.md
└── src
    ├── core
    │   ├── http_transport.py
    │   ├── server.py
    │   └── stdio_transport.py
    ├── tools
    │   └── handlers.py
    └── utils
        ├── requirements.txt
        └── utils.py
```

**Detailed Requirements per File:**

1.  **`src/utils/requirements.txt`**:
    *   Include: `fastmcp`, `httpx`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `pydantic`.

2.  **`src/utils/utils.py` (Authentication)**:
    *   Define OAuth scopes: `['https://www.googleapis.com/auth/gmail.modify']`.
    *   Logic to check for secrets in `~/run/secrets` (local dev) or `/run/secrets` (Docker standard).
    *   Implement `generate_token()`: Use `InstalledAppFlow` to create `token.json` from `credentials.json`.
    *   Implement `get_oauth_token()`: Return a valid token string. Handle token refreshing automatically.
    *   **Crucial:** Handle `OSError` when saving the refreshed token, as Docker secrets are read-only filesystem mounts. Do not crash if save fails.

3.  **`src/tools/handlers.py` (Business Logic)**:
    *   Use `httpx.AsyncClient`.
    *   Implement 4 async functions:
        *   `handle_get_gmail_message(client, message_id)`: GET `/messages/{id}`.
        *   `handle_list_gmail_messages(client, count)`: GET `/messages` with `maxResults`.
        *   `handle_send_gmail_message(client, to, subject, body, cc, bcc)`: POST `/messages/send`. **Important:** Create MIME message and encode as `base64url` string in a JSON payload `{'raw': ...}`.
        *   `handle_download_gmail_attachment(client, message_id, attachment_id)`: GET `/messages/{message_id}/attachments/{attachment_id}`.
    *   Include robust error handling with `logging`.

4.  **`src/core/server.py` (MCP Application)**:
    *   Initialize `FastMCP("gmail-mcp")`.
    *   Global `httpx.AsyncClient` setup in `@mcp.on_startup`. Base URL: `https://gmail.googleapis.com/gmail/v1/users/me`.
    *   Inject the OAuth token from `utils` into the Authorization header (`Bearer ...`).
    *   Define tools corresponding to the handlers. Use `pydantic.Field` for rich descriptions.
    *   Ensure resource cleanup (client close) in `@mcp.on_shutdown`.

5.  **Transports**:
    *   **`src/core/stdio_transport.py`**: Run `mcp.run(transport='stdio')` for local desktop integration.
    *   **`src/core/http_transport.py`**: Run `mcp.run(transport='sse')`. Load host/port from a `http-config.json` file (default 0.0.0.0:3085).

6.  **Infrastructure**:
    *   **`Dockerfile`**: Use `python:3.12-slim`. Create a non-root user `mcp_gmail_assist`. **Optimization:** Copy `requirements.txt` and install dependencies *before* copying the rest of the source code to leverage caching. Expose port 3085.
    *   **`docker-compose.yaml`**: Define service `gmail-mcp`. Map port 3085. **Security:** Use Docker Secrets to mount `token_json` and `credentials_json` into `/home/mcp_gmail_assist/run/secrets/`.

7.  **`http-config.json`**:
    *   JSON config setting host to `0.0.0.0` and port to `3085`.

Please generate the complete, ready-to-run code for these files.