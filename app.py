import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit App Title
st.title("Tube Curriculum: Personalized Learning Paths from YouTube")

# Input Form for User Details
st.header("Tell us about your learning goals")
with st.form(key="learning_form"):
    learning_objective = st.text_input("What is your learning objective?", placeholder="e.g., Learn Python for Data Science")
    core_skill = st.text_input("What is the core skill you'd like to focus on?", placeholder="e.g., Python programming")
    time_availability = st.number_input("How many hours per week can you dedicate?", min_value=1, step=1)
    submitted = st.form_submit_button("Generate Learning Path")

# Handle Form Submission
if submitted:
    # Ensure all fields are filled
    if not learning_objective or not core_skill or not time_availability:
        st.error("Please fill out all fields before submitting.")
    else:
        # Construct OpenAI prompt
        prompt = f"""
        Create a structured learning path and YouTube playlist for someone who wants to achieve the following learning objective: {learning_objective}.
        Focus on the core skill: {core_skill}. They have {time_availability} hours per week to dedicate.
        Provide step-by-step guidance and suggest high-quality YouTube videos for each step.
        """
        
        # Try to get a response from OpenAI
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7,
            )
            # Extract the learning path from the response
            learning_path = response.choices[0].text.strip()

            # Display the generated learning path
            st.subheader("Your Personalized Learning Path")
            st.write(learning_path)
        except Exception as e:
            st.error(f"An error occurred while generating the learning path: {e}")
