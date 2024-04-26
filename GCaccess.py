from datetime import *
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def getTodaysEvents():
  
  Filtered_Events = {}

  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
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

  try:
    service = build("calendar", "v3", credentials=creds)

    page_token = None
    while True:
        
        now = datetime.now()
        #Google Zulu Times, its the standard they use for request for certain dates
        #You can modify to get more than just today's events here
        zulu_stringStart = now.strftime("%Y-%m-%dT00:00:00Z")
        zulu_stringEnd = now.strftime("%Y-%m-%dT11:59:59Z")
        #Retrives all of the data
        events = service.events().list(calendarId='INSERT YOUR CALENDAR ID', pageToken=page_token, timeMin=zulu_stringStart, timeMax=zulu_stringEnd).execute()
  
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    for event in events['items']:
      temp = {}
      try: 
        temp["description"] = event["description"] 
      except:
        temp["description"] = ""
        #I think I owe to explain what is going on here
        #Basically we take out the start and the end time of an event, we convert it using the date time library
        #Into actual word dates (April 26) and save to out temp event(because there could be more than just one event)
      temp["start"] = datetime.strptime(event["start"]["date"], "%Y-%m-%d").strftime("%B %d")
      temp["end"] = datetime.strptime(event["end"]["date"], "%Y-%m-%d").strftime("%B %d")
      Filtered_Events[event["summary"]] = temp
      return (Filtered_Events)
  except HttpError as error:
    print(f"An error occurred: {error}")

    return Filtered_Events
