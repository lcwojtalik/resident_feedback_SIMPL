from typing import Optional

# This is a stub. Swap for:
# - Gmail API send (official)
# - SMTP (institution-approved relay)
# - Twilio SMS (if using phone numbers)
#
# For now, we just print so you can see what would be sent.

def send_email(to: str, subject: str, body: str, dry_run: bool = True) -> None:
    if dry_run:
        print(f"""--- DRY RUN EMAIL ---
TO: {to}
SUBJECT: {subject}

{body}
---------------------
""")
    else:
        # TODO: implement a real sender
        raise NotImplementedError("Real email sending not implemented yet.")
