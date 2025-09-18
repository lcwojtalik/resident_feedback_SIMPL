# OR Feedback Reminder – Starter Kit

A lightweight starter project to:
1) ingest weekly OR schedules emailed by chief residents (recommended as CSV attachment),
2) store assignments (attending↔resident by date) in a small SQLite DB,
3) send a daily reminder to each attending with a link to submit feedback in SIMPL for the resident they worked with that day.

> This is a **minimal, hackable starting point**. Swap stubs for real Gmail API reads and real email/SMS sending when ready.

---

## Why start here?

Parsing arbitrary emails is brittle. Asking chiefs to send a **simple, standard CSV** keeps parsing deterministic and maintainable. You can add more parsers later (e.g., for common exports from your OR system).

---

## Project layout

```
or_feedback_reminders/
├─ app.py                # orchestrates: ingest -> upsert -> send reminders
├─ db.py                 # SQLite helpers
├─ models.py             # Pydantic models for validation
├─ parser.py             # CSV parser (simple, explicit schema)
├─ emailer.py            # stubbed email sender (prints); swap for SMTP/Gmail API/Twilio
├─ requirements.txt
├─ README.md
└─ sample_data/
   ├─ attendings.csv     # Attending name→email map (add phone if using SMS)
   └─ schedule_week.csv  # Example of the CSV chiefs should send
```

---

## Expected CSV schema (weekly schedule)

One row per {"date","attending_name","resident_name"}, optionally with "service" and "room".

**Columns (exact spelling):**
- `date` (YYYY-MM-DD) — the operative date
- `attending_name` — as it appears in `attendings.csv`
- `resident_name` — free text (you can normalize later)
- `service` (optional) — e.g., Vascular, Colorectal
- `room` (optional) — OR room/number

See `sample_data/schedule_week.csv`.

---

## Quickstart

1. **Python 3.10+** recommended.
2. Create and activate a venv, then:
   ```bash
   pip install -r requirements.txt
   ```
3. Edit `sample_data/attendings.csv` with your attendings and emails.
4. Drop a weekly CSV into `sample_data/schedule_week.csv` (or point `app.py` to another path).
5. Run a **dry run** for today:
   ```bash
   python app.py --today 2025-09-18 --dry-run
   ```
   You should see “emails” printed to stdout.

---

## Deploying a daily reminder

Use any scheduler:
- macOS/Linux: cron (e.g., run at 6am daily)
- GitHub Actions: cron workflow
- Cloud: AWS Lambda + EventBridge, or GCP Cloud Run + Cloud Scheduler

Example cron (6:30am daily):
```
30 6 * * * /usr/bin/python /path/to/app.py --today $(date +\%F) >> /var/log/or_reminders.log 2>&1
```

---

## Reading emails automatically

This starter keeps parsing simple. To automate ingestion:
- **Gmail API**: fetch messages with a subject like `[OR Schedule] 2025-09-18` and download CSV attachments to a temp folder, then call `parser.parse_csv()`.
- **Google Apps Script** (low-code): label incoming schedule emails, save attachments to Drive, and hit a webhook (or Cloud Run) to ingest.

Integrate at TODOs in `app.py` (see `pull_emails_and_save_csvs()` placeholder).

---

## SIMPL link

If SIMPL supports a universal link or app link, set `SIMPL_BASE_URL` in `app.py`. If not, include a friendly nudge:
> “Open SIMPL → Daily Feedback → Select resident: {resident_name} ({date}).”

---

## PHI / Compliance Notes

- Avoid PHI in emails. You only need names and dates, not case details.
- Use institution-approved email and storage. SQLite is fine for a pilot; move to Postgres + SSL at scale.
- Log minimally; never log patient info.

---

## Extending

- Auto-detect split days (attending with AM/PM residents)
- Handle last-minute swaps (update the DB with a “versioned” table or overwrite same-date rows by attending)
- Export “completion” dashboard by week
- Add SMS fallback for attendings who prefer text
- Build an admin UI (e.g., Streamlit) to view assignments and reminder status

---

## Commands

- Dry run today:
  ```bash
  python app.py --today 2025-09-18 --dry-run
  ```

- Ingest a CSV manually:
  ```bash
  python app.py --ingest sample_data/schedule_week.csv
  ```

---

*Made as a starting point; customize freely.*
