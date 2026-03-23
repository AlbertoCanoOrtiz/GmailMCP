import json
from pathlib import Path
from .server import mcp

def run_http():
    """
    Run the server using FastMCP's built-in HTTP capabilities.
    FastMCP handles the FastAPI application setup and SSE transport automatically.
    Configuration is loaded from http-config.json in the project root.
    """
    # Default configuration
    host = "0.0.0.0"
    port = 3085

    # Resolve config file path (Project Root/http-config.json)
    # Path is relative to: src/core/http_transport.py -> parents[2] is root
    config_path = Path(__file__).resolve().parents[2] / "http-config.json"

    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                host = config.get("host", host)
                port = config.get("port", port)
        except Exception as e:
            print(f"Error loading config file: {e}")

    print(f"HTTP server starting on http://{host}:{port}")
    # FastMCP automatically creates the FastAPI app and Uvicorn server
    mcp.run(transport="sse", port=port, host=host)

if __name__ == "__main__":
    run_http()
