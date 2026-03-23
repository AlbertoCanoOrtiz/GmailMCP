import logging
import httpx
import base64
from email.mime.text import MIMEText

log = logging.getLogger(__name__)


async def handle_get_gmail_message(client: httpx.AsyncClient, message_id: str) -> dict:
    try:
        # Google API: /users/me/messages/{id} (Base URL handles prefix)
        response = await client.get(f'/messages/{message_id}')
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while fetching Gmail message: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to fetch Gmail message: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while fetching Gmail message: {e}")
        raise RuntimeError(f"Unexpected error: {e}")


async def handle_list_gmail_messages(client: httpx.AsyncClient, count: int) -> dict:
    try:
        # Google API: /users/me/messages?maxResults={count}
        response = await client.get('/messages', params={'maxResults': count})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while listing Gmail messages: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to list Gmail messages: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while listing Gmail messages: {e}")
        raise RuntimeError(f"Unexpected error: {e}")

    
async def handle_send_gmail_message(client: httpx.AsyncClient, to: str, subject: str, body: str, cc: str | None, bcc: str | None) -> dict:
    # Create the email message using MIME
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    if cc: message['cc'] = cc
    if bcc: message['bcc'] = bcc

    # Google API requires raw base64url encoded string
    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()
    payload = {'raw': raw_string}

    try:
        # Google API: /users/me/messages/send
        response = await client.post('/messages/send', json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while sending Gmail message: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to send Gmail message: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while sending Gmail message: {e}")
        raise RuntimeError(f"Unexpected error: {e}")


async def handle_download_gmail_attachment(client: httpx.AsyncClient, message_id: str, attachment_id: str) -> dict:
    try:
        # Correct Google API path for attachments
        response = await client.get(f'/messages/{message_id}/attachments/{attachment_id}')
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while downloading Gmail attachment: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to download Gmail attachment: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while downloading Gmail attachment: {e}")
        raise RuntimeError(f"Unexpected error: {e}")