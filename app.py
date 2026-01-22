import streamlit as st
import pandas as pd
import pickle

with open("flight_delay_model.pkl", "rb") as f:
    model = pickle.load(f)
    
# UI setting
st.set_page_config(page_title="Flight Delay Predictor", page_icon="✈️", layout="centered")

st.title("✈️ Flight Delay Prediction App")
st.write("Predict **Arrival Delay (minutes)** using flight details")

st.markdown("---")

# user input
st.subheader("Enter Flight Details")
col1, col2 = st.columns(2)

with col1:
    DayOfWeek = st.selectbox("Day of the Week (0=Mon, 6=Sun)", [0, 1, 2, 3, 4, 5, 6])
    DepTime = st.number_input("Departure Time (HHMM format)", value=900)
    CRSArrTime = st.number_input("Scheduled Arrival Time (HHMM)", value=1130)
    Distance = st.number_input("Distance (miles)", value=500)

carrier_list = ["WN", "AA", "DL", "UA", "B6", "AS", "NK", "F9"]
airport_list = ["BWI", "MCO", "JFK", "LAX", "ATL", "ORD", "DFW", "DEN", "SFO", "LAS"]

with col2:
    UniqueCarrier = st.selectbox("Carrier Code", carrier_list)
    Origin = st.selectbox("Origin Airport Code", airport_list)
    Dest = st.selectbox("Destination Airport Code", airport_list)
    DepDelay = st.number_input("Departure Delay (minutes)", value=10)

TaxiOut = st.number_input("Taxi Out Time (minutes)", value=7)
TaxiIn = st.number_input("Taxi In Time (minutes)", value=4)

st.markdown("---")

# Predict Button ✅
if st.button("✅ Predict Arrival Delay"):
    sample = pd.DataFrame([{
        "DayOfWeek": DayOfWeek,
        "DepTime": DepTime,
        "CRSArrTime": CRSArrTime,
        "UniqueCarrier": UniqueCarrier.upper(),
        "Origin": Origin.upper(),
        "Dest": Dest.upper(),
        "Distance": Distance,
        "DepDelay": DepDelay,
        "TaxiOut": TaxiOut,
        "TaxiIn": TaxiIn
    }])

    prediction = model.predict(sample)[0]

    # Make output clean
    if prediction < 0:
        prediction = 0

    st.success(f"✈️ Predicted Arrival Delay: **{round(prediction, 2)} minutes** ✅")

    # Conclusion based on delay minutes
    if prediction <= 5:
        st.info("✅ Conclusion: Flight will be **On Time / Very Minor Delay** 🙂")
    elif prediction <= 30:
        st.warning("⚠️ Conclusion: Flight may have a **Slight Delay** ⏳")
    else:
        st.error("❌ Conclusion: Flight is likely to have a **Heavy Delay** 😟")
