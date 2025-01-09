import streamlit as st
import openai
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
import datetime

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google API setup
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CREDENTIALS = json.loads(st.secrets["GOOGLE_CREDENTIALS"])["web"]

# Function to authenticate the user with Google
def google_auth_flow():
    flow = Flow.from_client_config(CREDENTIALS, scopes=SCOPES)
    flow.redirect_uri = st.experimental_get_query_params().get("redirect_uri", [None])[0]
    auth_url, _ = flow.authorization_url(prompt="consent")
    return auth_url

def google_auth_callback():
    flow = Flow.from_client_config(CREDENTIALS, scopes=SCOPES)
    flow.redirect_uri = st.experimental_get_query_params()["redirect_uri"][0]
    flow.fetch_token(authorization_response=st.experimental_get_query_params()["url"][0])
    return flow.credentials

# Function to add events to Google Calendar
def add_video_to_calendar(credentials, video_title, video_link, start_time):
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': video_title,
        'description': f'Watch this video: {video_link}',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (start_time + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result

# Streamlit UI
st.title("YouTube Curriculum Organizer with Calendar Integration")

# Step 1: Enter the topic
topic = st.text_input("Enter the topic you want to learn about:", "")

if topic:
    # Step 2: Generate YouTube video recommendations
    st.write("Generating video recommendations...")

    # Prompt OpenAI to recommend videos
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that recommends YouTube videos."},
            {"role": "user", "content": f"Recommend 5 YouTube videos about {topic}, each with a title, description, and link."}
        ],
        max_tokens=500,
    )

    video_recommendations = json.loads(response['choices'][0]['message']['content'])
    st.write("Here are the recommended videos:")
    for idx, video in enumerate(video_recommendations, start=1):
        st.write(f"**{idx}. {video['title']}**")
        st.write(f"Description: {video['description']}")
        st.write(f"Link: [Watch Video]({video['link']})")

    # Step 3: Authenticate Google Calendar
    st.write("---")
    st.write("### Add Videos to Your Google Calendar")
    if "google_credentials" not in st.session_state:
        auth_url = google_auth_flow()
        st.markdown(f"[Authenticate with Google]({auth_url})")
    else:
        credentials = google.oauth2.credentials.Credentials(**st.session_state["google_credentials"])
        video_to_add = st.selectbox("Select a video to add to your calendar:", [f"{video['title']} - {video['link']}" for video in video_recommendations])
        selected_video = video_recommendations[[f"{video['title']} - {video['link']}" for video in video_recommendations].index(video_to_add)]
        start_time = st.date_input("Select a date and time for the event:", value=datetime.datetime.now())
        if st.button("Add to Calendar"):
            result = add_video_to_calendar(credentials, selected_video['title'], selected_video['link'], start_time)
            st.success(f"Event added to Google Calendar: {result.get('htmlLink')}")

# Handle OAuth callback
if "url" in st.experimental_get_query_params():
    try:
        credentials = google_auth_callback()
        st.session_state["google_credentials"] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        st.success("Google authentication successful! Refresh the page to continue.")
    except Exception as e:
        st.error(f"Error during Google authentication: {e}")
