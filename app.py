import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key="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")  # Replace with your actual OpenAI API key

# Streamlit app UI
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
            
            # Call the OpenAI API
            response = client.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                prompt=prompt,
                temperature=0.7,
                max_tokens=300,
            )

            # Extract and display the learning path
            learning_path = response.choices[0]["text"].strip()
            st.success("Here’s your personalized learning path:")
            st.write(learning_path)

    else:
        st.warning("Please fill in all the fields to generate your learning path.")
