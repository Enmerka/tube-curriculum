import streamlit as st
import openai

# Set up OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]

# Streamlit App Title
st.title("Tube Curriculum MVP")

# Introduction
st.write("""
### Personalized Learning Path Generator
Input your learning goals, core skills, and time availability. We'll create a curated learning path for you!
""")

# User Input Form
with st.form("user_input_form"):
    learning_objective = st.text_input("What do you want to learn? (e.g., Python programming, graphic design)")
    core_skill = st.text_input("What is the core skill you want to focus on? (e.g., coding, design thinking)")
    time_availability = st.number_input("How many hours per week can you dedicate?", min_value=1, step=1)
    submitted = st.form_submit_button("Generate Learning Path")

# Process Input
if submitted:
    if learning_objective and core_skill and time_availability:
        # OpenAI Prompt
        prompt = f"""
        Create a structured learning path and YouTube playlist for someone who wants to achieve the following learning objective: {learning_objective}.
        Focus on the core skill: {core_skill}. They have {time_availability} hours per week to dedicate.
        Provide step-by-step guidance and suggest high-quality YouTube videos for each step.
        """
        try:
    
