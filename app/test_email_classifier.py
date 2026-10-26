
from app.gmail.gmail_reader import get_new_emails
from app.ai.email_classifier import classify_email


def main():
    emails = get_new_emails(max_results=3)

    if not emails:
        print("No unread emails found in the inbox.")
        return

    for email in emails:
        print("\n" + "=" * 50)
        print("Subject:", email["subject"])

        result = classify_email(email)

        print("Importance:", result["importance"])
        print("Category:", result["category"])
        print("Summary:", result["summary"])
        print("Reason:", result["reason"])


if __name__ == "__main__":
    main()
