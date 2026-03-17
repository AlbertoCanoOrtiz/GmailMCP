import os
import logging
from typing import Literal

import httpx
from pydantic import Field
from fastmcp import FastMCP, Context

# Tool handlers
from ..tools.handlers import handle_get_gmail_message, handle_list_gmail_messages, handle_send_gmail_message, handle_download_gmail_attachment

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    "dogjgp-server",
    dependencies=["httpx"]
)

# Global API Client
http_client: httpx.AsyncClient | None = None
BASE_URL = os.getenv('DOGSJGP_API_URL', 'https://dogjgp.mx/api')
API_KEY = os.getenv('DOGSJGP_API_KEY')

@mcp.on_startup
async def on_startup(ctx: Context):
    """Initialize API client and verify connection on startup."""
    global http_client
    
    log.info('API Configuration:')
    log.info(f'Base URL: {BASE_URL}')
    log.info(f'API Key: {"Available" if API_KEY else "Not available"}')

    if not API_KEY:
        log.warning('Warning: DOGSJGP_API_KEY environment variable not set')

    http_client = httpx.AsyncClient(
        base_url=BASE_URL,
        headers={
            'Authorization': API_KEY or "",
            'Content-Type': 'application/json',
            'User-Agent': 'DOGSJGP-MCP-Server/1.0.0'
        },
        timeout=30.0
    )

    try:
        response = await http_client.get('/public/v1/integrations')
        if response.status_code == 401:
            log.error('Invalid API key')
        elif response.status_code == 404:
            log.error('API endpoint not found')
        elif response.is_error:
            log.error(f"API connection test failed: {response.status_code}")
        else:
            log.info('API connection test successful')
    except Exception as e:
        log.error(f'Failed to connect to API: {e}')
        # We don't raise here to allow the server to start even if the API is temporarily down,
        # but in strict mode you might want to raise.

@mcp.on_shutdown
async def on_shutdown():
    """Cleanup resources."""
    if http_client:
        await http_client.aclose()

# --- Tools ---

@mcp.tool(description="Fetch a Gmail message by ID using Gmail API.")
async def get_gmail_message(message_id: str = Field(..., description="The ID of the Gmail message to retrieve") ) -> dict:
    if not http_client:
        raise RuntimeError("API client not initialized")
    return await handle_get_gmail_message(http_client, message_id)


@mcp.tool(description="Fetch a list of recent Gmail messages using Gmail API.")
async def list_gmail_messages(count: int = Field(10, ge=1, le=100, description="Number of messages to retrieve")) -> dict:
    if not http_client:
        raise RuntimeError("API client not initialized")    
    return await handle_list_gmail_messages(http_client, count)


@mcp.tool(description="Send an email using Gmail API.")
async def send_gmail_message(
    to: str = Field(..., description="Recipient email address"),
    subject: str = Field(..., description="Email subject"),
    body: str = Field(..., description="Email body"),
    cc: str | None = Field(None, description="CC email address"),
    bcc: str | None = Field(None, description="BCC email address")
) -> dict:
    if not http_client:
        raise RuntimeError("API client not initialized")    
    return await handle_send_gmail_message(http_client, to, subject, body, cc, bcc)

    
@mcp.tool(description="Download an attachment from a Gmail message.")
async def download_gmail_attachment(attachment_id: str = Field(..., description="The ID of the attachment to download")) -> dict:
    if not http_client:
        raise RuntimeError("API client not initialized")
    return await handle_download_gmail_attachment(http_client, attachment_id)
