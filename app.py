import streamlit as st
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import re

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app UI
st.title("Tube Curriculum: Personalized Learning Path Generator with Google Calendar Integration")

# Input form for user data
with st.form(key="learning_form"):
    learning_objective = st.text_input("What is your learning objective?")
    core_skill = st.text_input("What core skill do you want to learn?")
    time_availability = st.number_input("How many hours per week can you dedicate?", min_value=1, step=1)
    submitted = st.form_submit_button("Generate Learning Path")

# Authenticate with Google Calendar
def authenticate_google_calendar():
    credentials = None
    if "token.json" in st.secrets:  # Load credentials from Streamlit secrets
        credentials = Credentials.from_authorized_user_info(st.secrets["token.json"], scopes=["https://www.googleapis.com/auth/calendar"])
    else:
        st.error("Google Calendar API credentials are missing!")
    return credentials

# Add events to Google Calendar
def add_events_to_calendar(events):
    credentials = authenticate_google_calendar()
    if not credentials:
        return

    service = build("calendar", "v3", credentials=credentials)

    # Create events in the user's primary calendar
    for event in events:
        event_body = {
            "summary": event["title"],
            "description": event["description"],
            "start": {"dateTime": event["start"], "timeZone": "UTC"},
            "end": {"dateTime": event["end"], "timeZone": "UTC"},
        }
        service.events().insert(calendarId="primary", body=event_body).execute()

# Handle form submission
if submitted:
    if learning_objective and core_skill and time_availability:
        with st.spinner("Generating your personalized learning path..."):
            try:
                # Define the prompt for the AI
                prompt = (
                    f"Create a step-by-step learning path using free YouTube videos for someone who wants to achieve the following "
                    f"learning objective: {learning_objective}. Focus on the core skill: {core_skill}. "
                    f"They have {time_availability} hours per week to dedicate. Include video links."
                )

                # Call the OpenAI API using the new syntax
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert curriculum designer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                # Extract the learning path and parse videos
                learning_path = response.choices[0].message.content.strip()
                st.success("Here’s your personalized learning path:")
                st.write(learning_path)

                # Extract video titles and links using regex
                video_pattern = re.compile(r"(.+?)\s*-\s*(https?://\S+)")
                videos = video_pattern.findall(learning_path)

                if videos:
                    st.write("Extracted videos:")
                    for i, (title, link) in enumerate(videos, start=1):
                        st.markdown(f"{i}. [{title}]({link})")

                    # Prepare events for Google Calendar
                    now = datetime.datetime.utcnow()
                    events = []
                    for i, (title, link) in enumerate(videos):
                        start_time = now + datetime.timedelta(days=i)
                        end_time = start_time + datetime.timedelta(hours=1)  # Assume 1 hour per video
                        events.append({
                            "title": title,
                            "description": f"Watch this video: {link}",
                            "start": start_time.isoformat() + "Z",
                            "end": end_time.isoformat() + "Z",
                        })

                    # Add events to Google Calendar
                    add_events_to_calendar(events)
                    st.success("Videos have been added to your Google Calendar!")
                else:
                    st.warning("No videos found in the generated learning path.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all the fields to generate your learning path.")
