import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual OpenAI API key

# Title of the app
st.title("Tube Curriculum: Personalized Learning Path Generator")

# App description
st.write(
    """
    Welcome to Tube Curriculum! Fill out the form below, and we will generate a personalized 
    learning path and YouTube playlist to help you master a core skill.
    """
)

# Input form
with st.form(key="learning_form"):
    learning_objective = st.text_input("What is your learning objective?")
    core_skill = st.text_input("What core skill do you want to learn?")
    time_availability = st.number_input("How many hours per week can you dedicate?", min_value=1, step=1)
    submitted = st.form_submit_button("Generate Learning Path")

# Handle form submission
if submitted:
    if learning_objective and core_skill and time_availability:
        with st.spinner("Generating your personalized learning path..."):
            # Define the prompt
            prompt = (
                f"Create a step-by-step learning path using free YouTube videos for someone who wants to achieve the "
                f"following learning objective: {learning_objective}. Focus on the core skill: {core_skill}. "
                f"They have {time_availability} hours per week to dedicate."
            )

            # Call OpenAI API
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=1500,
                    temperature=0.7,
                )
                learning_path = response["choices"][0]["text"]
                st.success("Here’s your personalized learning path:")
                st.write(learning_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all the fields to generate your learning path.")
