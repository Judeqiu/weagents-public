---
name: google-workspace
description: Interact with Google Workspace (Sheets, Docs, Drive) using the gws CLI and helper scripts. Use when creating, reading, or modifying Google Sheets, Google Docs, or managing Google Drive files. Supports spreadsheet creation with formulas, document editing, file uploads, and sharing.
---

# Google Workspace Integration

This skill enables interaction with Google Workspace services (Sheets, Docs, Drive) using the `gws` CLI tool and helper scripts.

## Prerequisites

1. **Install gws CLI**: `npm install -g @googleworkspace/cli`
2. **Authentication**: Run `gws auth setup` and complete OAuth flow
3. **Service Account** (optional): For automated access, create a service account and share files with it

## Quick Reference

### Common Operations

**Create a Google Sheet:**
```bash
gws sheets spreadsheets create --json '{"properties":{"title":"My Sheet"}}'
```

**Write data to a Sheet:**
```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"ID","range":"A1:C3","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["A","B","C"],[1,2,3]]}'
```

**Create a Google Doc:**
```bash
gws docs documents create --json '{"title":"My Document"}'
```

**List Drive files:**
```bash
gws drive files list --params '{"pageSize":10}'
```

**Upload a file:**
```bash
gws drive files create --upload /path/to/file --upload-content-type text/csv
```

## Using the Helper Script

For complex operations, use the provided helper script at `scripts/gws-helper.py`:

### Available Commands

```bash
# Create a spreadsheet with data
python3 scripts/gws-helper.py create-sheet "Portfolio" data.json

# Write data to existing sheet
python3 scripts/gws-helper.py write-sheet SPREADSHEET_ID "A1:J10" data.json

# Read data from sheet
python3 scripts/gws-helper.py read-sheet SPREADSHEET_ID "A1:J10"

# Create a document
python3 scripts/gws-helper.py create-doc "Report" content.txt

# List Drive files
python3 scripts/gws-helper.py list-files 20

# Upload file
python3 scripts/gws-helper.py upload file.csv text/csv

# Share file
python3 scripts/gws-helper.py share FILE_ID user@example.com writer
```

### Data Format for Sheets

JSON array of arrays (rows and columns):
```json
[
  ["Header1", "Header2", "Header3"],
  ["Row1Col1", "Row1Col2", "=A2+B2"],
  ["Row2Col1", "Row2Col2", "=A3+B3"]
]
```

Formulas are supported when using `USER_ENTERED` input option.

## Authentication Methods

### Method 1: User OAuth (Interactive)
```bash
gws auth login
```
Opens browser for user authentication. Best for interactive use.

### Method 2: Service Account (Automated)
1. Create service account in Google Cloud Console
2. Download JSON key file
3. Set environment variable: `export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE="/path/to/key.json"`
4. Share Google files with the service account email

## Common Patterns

### Stock Portfolio Sheet
```python
values = [
    ["Ticker", "Shares", "Price", "Value"],
    ["AAPL", 100, 150, "=B2*C2"],
    ["MSFT", 50, 380, "=B3*C3"],
    ["TOTAL", "", "", "=SUM(D2:D3)"]
]
```

### Formatting Headers
Use `batchUpdate` with `repeatCell` request to format header rows with colors and bold text.

### Working with Existing Files
1. Get file ID from URL (e.g., `.../d/FILE_ID/edit`)
2. Share file with service account if using service account auth
3. Use ID in API calls

### Creating New Sheets/Tabs Within a Spreadsheet

To add a new worksheet/tab to an existing spreadsheet:

```bash
# Create a new sheet/tab using batchUpdate
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE="/path/to/service-account.json"
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"YOUR_SPREADSHEET_ID"}' \
  --json '{"requests":[{"addSheet":{"properties":{"title":"New_Tab_Name"}}}]}'
```

**Then write data to the new tab:**
```bash
python3 scripts/gws-helper.py write-sheet SPREADSHEET_ID "New_Tab_Name!A1:Z50" data.json
```

**Key learnings:**
- Use `batchUpdate` (not `batch-update`) - case sensitive
- Tab names with spaces work but underscores are safer
- The helper script works with new tabs once created
- Always set `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` environment variable

## Troubleshooting

**403 Permission Error:**
- Ensure file is shared with service account (for service account auth)
- Check that user has granted necessary OAuth scopes
- Verify API is enabled in Google Cloud Console

**401 Authentication Error:**
- Run `gws auth login` to refresh credentials
- Check that `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` is set correctly

**Rate Limiting:**
- Add delays between requests
- Use batch operations when possible

**Creating New Tabs Returns "Unable to parse range":**
- The tab doesn't exist yet - create it first using `batchUpdate`
- Then write data using the helper script
- Example workflow: See "Creating New Sheets/Tabs Within a Spreadsheet" section above

## Resources

- gws CLI documentation: Run `gws --help`
- Google Sheets API: https://developers.google.com/sheets/api
- Google Docs API: https://developers.google.com/docs/api
- Google Drive API: https://developers.google.com/drive/api
