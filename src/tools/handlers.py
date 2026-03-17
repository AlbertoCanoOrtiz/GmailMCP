import os
import logging



async def handle_get_gmail_message(client: httpx.AsyncClient, message_id: str) -> dict:
    try:
        response = await client.get(f'/gmail/messages/{message_id}')
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
        response = await client.get('/gmail/messages', params={'count': count})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while listing Gmail messages: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to list Gmail messages: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while listing Gmail messages: {e}")
        raise RuntimeError(f"Unexpected error: {e}")

    
async def handle_send_gmail_message(client: httpx.AsyncClient, to: str, subject: str, body: str, cc: str | None, bcc: str | None) -> dict:
    payload = {
        'to': to,
        'subject': subject,
        'body': body,
        'cc': cc,
        'bcc': bcc
    }
    try:
        response = await client.post('/gmail/send', json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while sending Gmail message: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to send Gmail message: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while sending Gmail message: {e}")
        raise RuntimeError(f"Unexpected error: {e}")


async def handle_download_gmail_attachment(client: httpx.AsyncClient, attachment_id: str) -> dict:
    try:
        response = await client.get(f'/gmail/attachments/{attachment_id}')
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error while downloading Gmail attachment: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Failed to download Gmail attachment: {e.response.status_code}")
    except Exception as e:
        log.error(f"Unexpected error while downloading Gmail attachment: {e}")
        raise RuntimeError(f"Unexpected error: {e}")