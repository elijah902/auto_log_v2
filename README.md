# auto-log

Automatically log daily Garmin stats (resting heart rate, running distance, and running time) to a Google Sheet.

## What it does

1. Logs in to Garmin Connect, reusing saved tokens when available.
2. Fetches today's resting heart rate, total running distance, and moving time.
3. Writes those values into today's row of a Google Sheets spreadsheet.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- A Garmin Connect account
- A Google Cloud project with the Google Sheets API enabled

## Setup

1. Install dependencies:

   ```sh
   uv sync
   ```

2. Add your Google OAuth client secret as `credentials.json` in the project root. The OAuth flow requests the `https://www.googleapis.com/auth/spreadsheets` scope.

3. Set your Garmin credentials (optional — you'll be prompted if unset):

   ```sh
   export GARMIN_EMAIL="you@example.com"
   export GARMIN_PASSWORD="your-password"
   ```

   Garmin tokens are stored in `~/.garminconnect` by default. Override this with the `GARMINTOKENS` environment variable.

4. Run the script once and complete the Google OAuth flow in your browser. A `token.json` file is created and reused on later runs.

## Usage

```sh
uv run write_cells.py
```

This writes today's stats to the `2026-2027` sheet:

- column `K` — running distance (miles)
- column `L` — running time
- column `P` — resting heart rate

## Notes

- `credentials.json` and `token.json` contain secrets and are git-ignored.
- The spreadsheet ID is currently hard-coded in `write_cells.py`.
- `main.py` (FastAPI) and `flow.py` are early experiments. The working entry point is `write_cells.py`.
