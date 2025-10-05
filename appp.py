import streamlit as st
import joblib
import pandas as pd

# Load the trained model
try:
    model = joblib.load('home_energy_predictor.joblib')
    st.success("Model loaded successfully!")
except FileNotFoundError:
    st.error("Error: 'home_energy_predictor.joblib' not found. Make sure the file is in the same directory.")
    model = None

# --- Streamlit App Interface ---
st.title("Energy Consumption Prediction")
st.write("Adjust the parameters on the sidebar to get a real-time prediction.")

# Sidebar for user input
st.sidebar.header("Input Features")

# Create input widgets for each feature
temp = st.sidebar.slider("Temperature (°C)", min_value=15.0, max_value=35.0, value=25.0, step=0.1)
humidity = st.sidebar.slider("Humidity (%)", min_value=30.0, max_value=60.0, value=45.0, step=0.1)
sq_footage = st.sidebar.slider("Square Footage", min_value=1000, max_value=2000, value=1500, step=10)
occupancy = st.sidebar.slider("Occupancy", min_value=0, max_value=10, value=5, step=1)
renewable_energy = st.sidebar.slider("Renewable Energy (kWh)", min_value=0.0, max_value=30.0, value=15.0, step=0.1)

hvac_usage = st.sidebar.selectbox("HVAC Usage", ["On", "Off"])
lighting_usage = st.sidebar.selectbox("Lighting Usage", ["On", "Off"])
day_of_week = st.sidebar.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
holiday = st.sidebar.checkbox("Is it a Holiday?")

# --- Create the input DataFrame for the model ---
if st.button("Predict"):
    # Create a dictionary to hold the features
    input_data = {
        'Temperature': temp,
        'Humidity': humidity,
        'SquareFootage': sq_footage,
        'Occupancy': occupancy,
        'RenewableEnergy': renewable_energy,
        'HVACUsage_On': 1 if hvac_usage == "On" else 0,
        'LightingUsage_On': 1 if lighting_usage == "On" else 0,
        'DayOfWeek_Monday': 1 if day_of_week == "Monday" else 0,
        'DayOfWeek_Saturday': 1 if day_of_week == "Saturday" else 0,
        'DayOfWeek_Sunday': 1 if day_of_week == "Sunday" else 0,
        'DayOfWeek_Thursday': 1 if day_of_week == "Thursday" else 0,
        'DayOfWeek_Tuesday': 1 if day_of_week == "Tuesday" else 0,
        'DayOfWeek_Wednesday': 1 if day_of_week == "Wednesday" else 0,
        'Holiday_Yes': 1 if holiday else 0
    }

    # Convert to DataFrame with the correct column order
    input_df = pd.DataFrame([input_data])
    
    # Make sure all required columns are present with a value of 0 if not set
    expected_columns = [
        'Temperature', 'Humidity', 'SquareFootage', 'Occupancy', 'RenewableEnergy',
        'HVACUsage_On', 'LightingUsage_On', 'DayOfWeek_Monday', 'DayOfWeek_Saturday', 
        'DayOfWeek_Sunday', 'DayOfWeek_Thursday', 'DayOfWeek_Tuesday', 
        'DayOfWeek_Wednesday', 'Holiday_Yes'
    ]
    
    input_df = input_df.reindex(columns=expected_columns, fill_value=0)

    # Make prediction
    if model:
        prediction = model.predict(input_df)[0]
        st.subheader("Predicted Energy Consumption")
        st.success(f"{prediction:.2f} kWh")