# Patch-Notes-from-Jira & OpenAI

Generate human-readable patch notes (Markdown) **and/or** a raw CSV export straight from a Jira board in one command-line call.  
The script pulls issues from the column you specify, optionally feeds them to OpenAI to create natural-language release notes, and saves the results in the folders you configure.

---

## Table of contents
1. Features  
2. Installation  
3. Configuration  
4. Usage  
5. Examples  
6. Troubleshooting  
7. Contributing & Licence

---

## Features
* One-shot export – fetch all issues in *one* Jira board column and save them as CSV.  
* Auto-generated patch notes – hand the same list to OpenAI and receive well-formatted Markdown release notes.  
* Credential test mode – quickly verify both APIs before you run anything heavy.  
* Minimal setup – just edit `settings.py` and `credentials.py`. No DBs, no servers.

---

## Installation
git clone https://github.com/your-org/patch-notes-from-jira.git
cd patch-notes-from-jira
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

(Python 3.9+ is recommended – tested up to 3.12.)

---

## Configuration

### 1. settings.py

BOARD            int    Numeric Jira board ID              e.g. 42
JIRACOLUMN       str    Exact column name to pull from      "Done"
OUTPUTFOLDERcsv  str    Folder path for CSV files          "exports/csv"
OUTPUTFOLDERmd   str    Folder path for Markdown files     "exports/md"

(All four are required. Folders are created automatically if missing.)

### 2. credentials.py

JIRA_API_TOKEN = "..."          # create at id.atlassian.com/manage-profile/security/api-tokens
JIRA_EMAIL     = "you@example.com"
JIRA_DOMAIN    = "yourcompany.atlassian.net"
OPENAI_API_KEY = "sk-..."

The helper in credentials.CheckCredentials() will hit both APIs and print a success code (200/201/202) if everything works.

Tip: prefer environment variables in CI—just read them inside credentials.py.

---

## Usage
python main.py [options]

Options:
  --csv, -c <filename>           Save issues to <filename>.csv
  --openai, --md, -o, -m <name>  Generate Markdown patch notes (filename *.md)
  --apiTest, --test, -t          Only validate Jira & OpenAI credentials
  -h, --help                     Show built-in help

Argument rules
* You may pass either --csv or --openai or both.  
* If neither is given, the script prints help and exits.  
* --csv / --openai expect bare filenames (folders come from settings.py).  
* When -t is passed, nothing is written—just credential checks.


## Examples

1. Happy path – create both CSV and Markdown  
   python main.py -c sprint28.csv -o sprint28_notes.md

   exports/csv/sprint28.csv  – raw issue data  
   exports/md/sprint28_notes.md – chat-style release notes ready for a PR description

2. API smoke test  
   python main.py -t

3. CSV only  
   python main.py --csv backlog_snapshot.csv

---

## Troubleshooting

Invalid JIRA credentials!    → Check JIRA_EMAIL, token, and JIRA_DOMAIN. Token must belong to the same Atlassian account.  
Invalid OpenAI credentials!  → Key revoked/expired, or your org blocked the model-list endpoint.  
“Please add Jira credentials…” → Empty strings in credentials.py.  
Permission errors writing files → Verify OUTPUTFOLDERcsv / OUTPUTFOLDERmd paths exist or are creatable.  
No issues found              → Column name in settings.JIRACOLUMN is case-sensitive—copy it exactly from the board.

---

## Contributing & Licence
Pull requests and issue reports are welcome! Please open a discussion first if you plan big changes.

Licence: TBD – defaulting to “All rights reserved” until we pick OSS terms (MIT, Apache 2, etc.). Feel free to suggest.

---

Happy shipping!
