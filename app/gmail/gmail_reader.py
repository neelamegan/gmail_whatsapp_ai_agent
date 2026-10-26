
import base64
from email.utils import parseaddr
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Read-only Gmail permission
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_gmail_service():
    """Authenticate and create the Gmail API client."""

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"Missing OAuth credentials: {CREDENTIALS_FILE}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def decode_body(data):
    """Decode a Gmail API Base64URL-encoded body."""

    decoded = base64.urlsafe_b64decode(data + "===")
    return decoded.decode("utf-8", errors="replace")


def extract_plain_text(payload):
    """Extract plain-text content from nested MIME parts."""

    mime_type = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data")

    if mime_type == "text/plain" and body_data:
        return decode_body(body_data)

    text_parts = []

    for part in payload.get("parts", []):
        text = extract_plain_text(part)
        if text:
            text_parts.append(text)

    return "\n".join(text_parts)


def get_new_emails(max_results=5):
    """
    Return unread messages in the inbox.
    This function does not mark messages as read.
    """

    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results,
    ).execute()

    messages = result.get("messages", [])
    emails = []

    for message in messages:
        details = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full",
        ).execute()

        payload = details.get("payload", {})
        headers = payload.get("headers", [])

        header_map = {
            header["name"].lower(): header["value"]
            for header in headers
        }

        sender_name, sender_address = parseaddr(
            header_map.get("from", "")
        )

        emails.append({
            "id": details["id"],
            "thread_id": details.get("threadId", ""),
            "sender_name": sender_name,
            "sender_email": sender_address,
            "subject": header_map.get("subject", "(No subject)"),
            "date": header_map.get("date", ""),
            "body": extract_plain_text(payload),
        })

    return emails


if __name__ == "__main__":
    for email in get_new_emails():
        print("\n" + "=" * 60)
        print("Message ID:", email["id"])
        print("From:", email["sender_email"])
        print("Subject:", email["subject"])
        print("Date:", email["date"])
        print("Body:", email["body"][:1000])
