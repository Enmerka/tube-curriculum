import streamlit as st
import openai  # Import the OpenAI library

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
            try:
                # Define the prompt for the AI
                prompt = (
                    f"Create a step-by-step learning path using free YouTube videos for someone who wants to achieve the following "
                    f"learning objective: {learning_objective}. Focus on the core skill: {core_skill}. "
                    f"They have {time_availability} hours per week to dedicate."
                )

                # Call the OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Use GPT-4 or GPT-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are an expert curriculum designer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300,
                )

                # Extract and display the learning path
                learning_path = response["choices"][0]["message"]["content"].strip()
                st.success("Here’s your personalized learning path:")
                st.write(learning_path)

            except openai.error.OpenAIError as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all the fields to generate your learning path.")
