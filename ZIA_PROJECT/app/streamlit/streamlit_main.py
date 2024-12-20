import streamlit as st
import requests

# Define the FastAPI endpoint
#API_ENDPOINT = "http://127.0.0.1:8000/predict"
API_ENDPOINT = "http://localhost:8000/predict"
# Streamlit app title
st.title("Ridge Classifier Model - Real-Time Prediction")

# User input form
st.header("Enter the Features for Classification")
annual_income = st.number_input("Annual Income ($)", min_value=0.0, step=1000.0)
family_size = st.number_input("Family Size", min_value=0, step=1)
age = st.number_input("Age", min_value=0.0, step=1.0)
work_experience = st.number_input("Work Experience (Years)", min_value=0.0, step=1.0)

# Predict button
if st.button("Predict"):
    # Input validation
    if annual_income <= 0 or family_size < 0 or age <= 0 or work_experience < 0:
        st.error("Please ensure all inputs are valid and greater than zero.")
    else:
        # Perform feature engineering
        income_per_family = annual_income / (family_size + 1)
        age_experience_interaction = float(age * work_experience)

        # Prepare data for API
        payload = {
            "Annual_Income": annual_income,
            "Family_Size": family_size,
            "Age": age,
            "Work_Experience": work_experience,
            "Income_Per_Family": income_per_family,
            "Age_Experience_Interaction": age_experience_interaction
        }

        # Send request to FastAPI
        try:
            response = requests.post(API_ENDPOINT, json=payload)
            response_data = response.json()

            # Display prediction result
            if response.status_code == 200:
                #prediction = response_data["prediction"]
                st.success(f"The predicted class is: {response_data}")
            else:
                st.error(f"Error: {response_data.get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")