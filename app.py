import json
import openai
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# Initialize OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Calendar API setup
CREDENTIALS = st.secrets["GOOGLE_CREDENTIALS"]["web"]
CLIENT_ID = CREDENTIALS["client_id"]
CLIENT_SECRET = CREDENTIALS["client_secret"]
PROJECT_ID = CREDENTIALS["project_id"]

# OAuth2 flow for Google Calendar access
def authenticate_google_account():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": ["http://localhost:8501"],
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"],
    )
    credentials = flow.run_local_server(port=0)
    return credentials

# Generate video recommendation function
def generate_video_recommendations():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Provide a list of YouTube video recommendations based on instructional design principles.",
        max_tokens=200,
    )
    video_list = response["choices"][0]["text"].strip().split("\n")
    return video_list

# Embed videos into Google Calendar
def create_google_calendar_event(credentials, video_title, video_link):
    service = build("calendar", "v3", credentials=credentials)
    
    event = {
        "summary": video_title,
        "description": f"Watch this instructional video: {video_link}",
        "start": {
            "dateTime": datetime.datetime.now().isoformat(),
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            "timeZone": "America/Los_Angeles",
        },
    }
    
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event

# Streamlit UI
def main():
    st.title("Video Curriculum & Google Calendar Integration")
    
    if st.button("Generate Video Recommendations"):
        videos = generate_video_recommendations()
        
        for video in videos:
            video_title, video_link = video.split(" - ")  # Assuming the format is "Title - URL"
            
            st.write(f"Title: {video_title}")
            st.write(f"Link: {video_link}")
            
            if st.button(f"Add '{video_title}' to Google Calendar"):
                credentials = authenticate_google_account()
                created_event = create_google_calendar_event(credentials, video_title, video_link)
                st.success(f"Video '{video_title}' added to your Google Calendar!")
                st.write(f"Event Link: {created_event.get('htmlLink')}")

if __name__ == "__main__":
    main()
