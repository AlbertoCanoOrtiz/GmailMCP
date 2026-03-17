from .server import mcp

def run_http(port: int = 3084):
    """
    Run the server using FastMCP's built-in HTTP capabilities.
    FastMCP handles the FastAPI application setup and SSE transport automatically.
    """
    print(f"HTTP server starting on http://localhost:{port}")
    # FastMCP automatically creates the FastAPI app and Uvicorn server
    mcp.run(transport="sse", port=port, host="0.0.0.0")
