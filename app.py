# app.py
import streamlit as st
import pandas as pd
import joblib

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="SUNWISE",
    layout="centered"
)

# -----------------------
# HEADER IMAGE / LOGO
# -----------------------
st.image("sunrise final logo.jpg",
    width=100
)
st.markdown(
    "<h1 style='text-align: center;'> SUNWISE</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: white;'><b>Solar Power Prediction using Atmospheric Conditions</b></p>",
    unsafe_allow_html=True
)

st.divider()


# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("About the App")
st.sidebar.write(
    """
    This app uses a trained **Random Forest model** to predict solar power output (kW).  
    Enter values for the required features in text fields.  
    Click **Predict Solar Power** to see the output.  
    """
)

# -----------------------
# LOAD MODEL FEATURES
# -----------------------
features_path = "model_features.pkl"
features = joblib.load("model_features.pkl")

# -----------------------
# LOAD TRAINED MODEL
# -----------------------
model_path = r"C:\Users\Aditya Dwivedi\OneDrive\Desktop\SOLAR POWER PREDICTION\solar_power_rf_model.pkl"
model = joblib.load("solar_power_rf_model.pkl")




# -----------------------
# FRIENDLY NAMES
# -----------------------
friendly_names = {
    'temperature_2_m_above_gnd': 'TEMPERATURE',
    'relative_humidity_2_m_above_gnd': 'HUMIDITY',
    'mean_sea_level_pressure_MSL': 'PRESSURE',
    'total_precipitation_sfc': 'PRECIPITATION',
    'snowfall_amount_sfc': 'SNOWFALL',
    'total_cloud_cover_sfc': 'TOTAL CLOUD COVER',
    'high_cloud_cover_high_cld_lay': 'HIGH CLOUD COVER',
    'medium_cloud_cover_mid_cld_lay': 'MEDIUM CLOUD COVER',
    'low_cloud_cover_low_cld_lay': 'LOW CLOUD COVER',
    'shortwave_radiation_backwards_sfc': 'SOLAR RADIATION',
    'wind_speed_10_m_above_gnd': 'WIND SPEED 10M',
    'wind_direction_10_m_above_gnd': 'WIND DIRECTION 10M',
    'wind_speed_80_m_above_gnd': 'WIND SPEED 80M',
    'wind_direction_80_m_above_gnd': 'WIND DIRECTION 80M',
    'wind_speed_900_mb': 'WIND SPEED 900MB',
    'wind_direction_900_mb': 'WIND DIRECTION 900MB',
    'wind_gust_10_m_above_gnd': 'WIND GUST 10M',
    'angle_of_incidence': 'ANGLE OF INCIDENCE',
    'zenith': 'ZENITH ANGLE',
    'azimuth': 'AZIMUTH ANGLE'
}

# -----------------------
# USER INPUT (TEXT FIELDS IN MULTI-COLUMNS)
# -----------------------
st.header("Set Parameters")

input_data = {}
cols = st.columns(3)

for i, feature in enumerate(features):
    friendly_name = friendly_names.get(feature, feature)
    col = cols[i % 3]

    val = col.text_input(friendly_name, value="0")
    try:
        input_data[feature] = float(val)
    except ValueError:
        input_data[feature] = 0.0  # fallback if invalid input

# Convert to DataFrame
input_df = pd.DataFrame([input_data])

# -----------------------
# PREDICTION
# -----------------------
st.header("Estimate Solar Power")

if st.button("Compute Solar Power"):
    prediction = model.predict(input_df)[0]
    prediction_value = round(prediction, 2)

    st.metric(label="Predicted Solar Power (kW)", value=prediction_value)

    if prediction_value > 50:
        st.success(f"High Power Output: {prediction_value} kW")
    elif prediction_value > 20:
        st.warning(f"Moderate Power Output: {prediction_value} kW")
    else:
        st.error(f"Low Power Output: {prediction_value} kW")
