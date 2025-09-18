import argparse
from datetime import date
from pathlib import Path

from models import Assignment, Attending
import db
import parser as schedule_parser
from emailer import send_email

SIMPL_BASE_URL = "https://app.simpl.org/"  # TODO: replace if SIMPL has a more direct feedback deep link

def pull_emails_and_save_csvs() -> list[Path]:
    """
    Placeholder where you'd use Gmail API to read new emails, download CSV attachments
    that match your naming convention (e.g., 'OR_schedule_YYYY-MM-DD.csv'),
    save them to a temp folder, and return the file paths.

    For now, returns an empty list and you can specify --ingest path manually.
    """
    return []

def ingest_csv(path: Path):
    assignments = schedule_parser.parse_csv(str(path))
    for a in assignments:
        db.upsert_assignment(a)

def load_attendings_from_csv(path: Path):
    import pandas as pd
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        att = Attending(attending_name=row['attending_name'], email=row['email'], phone=row.get('phone') if 'phone' in df.columns else None)
        db.upsert_attending(att)

def build_email(attending_name: str, resident_name: str, for_date: date) -> tuple[str, str]:
    subject = f"Quick SIMPL feedback for {resident_name} – {for_date.isoformat()}"
    body = (
        f"Hi {attending_name},\n\n"
        f"Thanks for teaching in the OR today. Please take 30 seconds to leave SIMPL feedback for "
        f"{resident_name} ({for_date.isoformat()}).\n\n"
        f"Open SIMPL: {SIMPL_BASE_URL}\n\n"
        f"If there was a swap, feel free to reply to this email with the correct resident name and we'll update the log.\n\n"
        f"— Automated reminder"
    )
    return subject, body

def send_todays_reminders(for_date: date, dry_run: bool = True):
    rows = db.get_assignments_for_date(for_date.isoformat())
    for (_date, attending_name, resident_name, service, room) in rows:
        email = db.get_attending_email(attending_name)
        if not email:
            print(f"[WARN] No email on file for attending '{attending_name}'. Skipping.")
            continue
        subject, body = build_email(attending_name, resident_name, for_date)
        send_email(email, subject, body, dry_run=dry_run)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", type=str, help="ISO date to send reminders for (YYYY-MM-DD). Default: today.", default=None)
    ap.add_argument("--ingest", type=str, help="Path to a schedule CSV to ingest.", default=None)
    ap.add_argument("--load-attendings", type=str, help="Path to attendings.csv to (re)load.", default=None)
    ap.add_argument("--dry-run", action="store_true", help="Print emails instead of sending.")
    args = ap.parse_args()

    db.init_db()

    if args.load_attendings:
        load_attendings_from_csv(Path(args.load_attendings))

    # Option A: Pull new emails and save CSVs (TODO – implement Gmail API here)
    for csv_path in pull_emails_and_save_csvs():
        ingest_csv(csv_path)

    # Option B: Manually ingest a provided CSV path
    if args.ingest:
        ingest_csv(Path(args.ingest))

    # Send today's reminders
    run_date = date.fromisoformat(args.today) if args.today else date.today()
    send_todays_reminders(run_date, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
