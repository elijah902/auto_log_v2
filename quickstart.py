from example import fetch_hr, init_api
from datetime import datetime

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1Bc-QPUUAFrdpFK19iSIm1P5DsE7_hy2RpiYpQFDM3Ao"


def get_todays_date():
    now = datetime.now()
    return f"{now.strftime('%m')}/{now.day}"
 
             
  
def read_date(spreadsheet_id, range_name):
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
  try:
    service = build("sheets", "v4", credentials=creds)
    
    result = (service.spreadsheets()
              .values()
              .get(spreadsheetId=spreadsheet_id, range=range_name)
              .execute()
    )
    return result.get("values", [])
  
  except HttpError as error:
    print(f"An error has occured: {error}")
    return error

def update_values(spreadsheet_id, range_name, value_input_option, values, creds):
  # creds, _ = google.auth.default()
  try:
    service = build("sheets", "v4", credentials=creds)
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
  
  
def write_hr(cell):
  """
  The file token.json stores the user's access and refresh tokens, and is
  created automatically when the authorization flow completes for the first
  time.
  """
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    # 62P
  api = init_api()
  update_values(SPREADSHEET_ID, cell, "RAW", [[fetch_hr(api)]], creds)

def fetch_todays_cell():
  columns = read_date(SPREADSHEET_ID, "'2026-2027'!J1:J354")
  target = get_todays_date()
  for i, row in enumerate(columns):
    for cell in row:
      if cell.strip() == target:
        return i +1
          
def main():
  write_hr(f"'2026-2027'!P{fetch_todays_cell()}")

if __name__ == "__main__":
  main()
