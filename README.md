# Payment Reminder Automation

An end-to-end automation that reads pending client payments from a Google Sheet, generates a PDF reminder notice, writes a personalized message using AI, and sends it via email or WhatsApp — automatically, on a schedule.

Built two ways: as a standalone Python script and as a visual n8n workflow.

## How it works

```
Google Sheet (clients + payment status)
        ↓
Filter rows where Status is "Pending" or "Overdue"
        ↓
For each client:
   → Generate a PDF payment reminder
   → AI writes a personalized reminder message
   → Send via Email or WhatsApp
   → Mark the row as "Reminded" in the sheet
```

## Python Version

```
payment-reminder/
├── main.py            # orchestrates the workflow, runs on a schedule
├── sheets.py           # reads/filters/updates the Google Sheet
├── pdf_generator.py    # generates the payment reminder PDF
├── emailer.py          # AI-generated message + email sending
├── whatsapp.py         # sends reminders via WhatsApp (Twilio)
└── output/             # generated PDFs
```

### Tech Stack
- Python
- Google Sheets API (`gspread`)
- Google Gemini API (`google-genai`)
- `fpdf2` for PDF generation
- Gmail SMTP for email
- Twilio for WhatsApp messaging
- `schedule` for automated runs

### Setup

1. Clone the repo
```bash
git clone https://github.com/TurboGlitch/payment-reminder
cd payment-reminder
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up Google Sheets API
   - Create a project on [Google Cloud Console](https://console.cloud.google.com)
   - Enable the Google Sheets API and Google Drive API
   - Create a Service Account, download the JSON key, save it as `service_account.json`
   - Share your Google Sheet with the service account's email (Editor access)

4. Create a `.env` file
```
GEMINI_API_KEY=your_key_here
EMAIL=your_gmail@gmail.com
APP_PASSWORD=your_gmail_app_password
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

5. Run it
```bash
python main.py
```

### Google Sheet format

| Client Name | Contact | Contact Type | Business Name | Service/Item | Amount | Due Date | Status |
|---|---|---|---|---|---|---|---|
| Ali Khan | ali@example.com | Email | Pixel Studio | Logo Design | 15000 | 2026-06-20 | Pending |

`Contact Type` determines whether the reminder is sent via Email or WhatsApp — set it to `Email` or `WhatsApp` accordingly, with the matching value in `Contact`.

## n8n Version

A visual workflow that mirrors the Python script — Google Sheets trigger, AI message generation, conditional routing between Email and WhatsApp, and writing back the reminder status.

The exported workflow is available in [`/n8n`](./n8n) — import it into your own n8n instance via **Workflows → Import from File**.