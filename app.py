import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (for local dev purposes)
load_dotenv()

# Fetch API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit app UI
import streamlit as st
st.title("Tube Curriculum: Personalized Learning Path Generator")

# Input form for user data
with st.form(key="learning_form"):
    learning_objective = st.text_input("What is your learning objective?")
    core_skill = st.text_input("What core skill do you want to learn?")
    time_availability = st.number_input("How many hours per week can you dedicate?", min_value=1, step=1)
    submitted = st.form_submit_button("Generate Learning Path")

# Handle form submission
if submitted:
    if learning_objective and core_skill and time_availability:
        with st.spinner("Generating your personalized learning path..."):
            # Define the prompt for the AI
            prompt = f"Create a step-by-step learning path using free YouTube videos for someone who wants to achieve the following learning objective: {learning_objective}. Focus on the core skill: {core_skill}. They have {time_availability} hours per week to dedicate."
            
            # Use the OpenAI client to generate a response
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4",  # or "gpt-3.5-turbo"
                max_tokens=300,
                temperature=0.7
            )

            # Extract and display the learning path
            learning_path = response.choices[0].message["content"].strip()
            st.success("Here’s your personalized learning path:")
            st.write(learning_path)

    else:
        st.warning("Please fill in all the fields to generate your learning path.")
