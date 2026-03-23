from .server import mcp

def run_stdio():
    """
    Run the server using FastMCP's stdio transport.
    This is used for local integration with MCP clients like Claude Desktop
    running on the same machine (not via Docker/HTTP).
    """
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run_stdio()