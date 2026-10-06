import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("hotel_cancellation_model.pkl")

# Page settings
st.set_page_config(
    page_title="Hotel Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
)

# Title
st.title("🏨 Hotel Booking Cancellation Predictor")
st.write(
    "Analyze a hotel booking and estimate its probability of cancellation."
)

st.divider()

# Sidebar
st.sidebar.header("🎯 Quick Demo")

demo = st.sidebar.selectbox(
    "Choose a booking example",
    [
        "Custom Booking",
        "Low Risk Booking",
        "High Risk Booking"
    ]
)

# Default values
hotel_default = "City Hotel"
lead_default = 30
nights_default = 2
guests_default = 2
meal_default = "BB"
segment_default = "Direct"
repeat_default = 0
previous_default = 0
deposit_default = "No Deposit"
requests_default = 1

# Demo values
if demo == "Low Risk Booking":
    hotel_default = "Resort Hotel"
    lead_default = 5
    nights_default = 2
    guests_default = 2
    meal_default = "BB"
    segment_default = "Direct"
    repeat_default = 1
    previous_default = 0
    deposit_default = "No Deposit"
    requests_default = 3

elif demo == "High Risk Booking":
    hotel_default = "City Hotel"
    lead_default = 180
    nights_default = 7
    guests_default = 2
    meal_default = "SC"
    segment_default = "Online TA"
    repeat_default = 0
    previous_default = 3
    deposit_default = "No Deposit"
    requests_default = 0

# Booking details
st.subheader("📋 Booking Details")

col1, col2 = st.columns(2)

with col1:

    hotel = st.selectbox(
        "Hotel Type",
        ["City Hotel", "Resort Hotel"],
        index=["City Hotel", "Resort Hotel"].index(hotel_default)
    )

    lead_time = st.number_input(
        "Lead Time (days)",
        min_value=0,
        max_value=1000,
        value=lead_default
    )

    total_nights = st.number_input(
        "Total Nights",
        min_value=0,
        max_value=100,
        value=nights_default
    )

    total_guests = st.number_input(
        "Total Guests",
        min_value=1,
        max_value=20,
        value=guests_default
    )

    meal = st.selectbox(
        "Meal Plan",
        ["BB", "HB", "FB", "SC", "Undefined"],
        index=["BB", "HB", "FB", "SC", "Undefined"].index(meal_default)
    )

with col2:

    market_segment = st.selectbox(
        "Market Segment",
        [
            "Direct",
            "Corporate",
            "Online TA",
            "Offline TA/TO",
            "Complementary",
            "Groups",
            "Undefined",
            "Aviation"
        ],
        index=[
            "Direct",
            "Corporate",
            "Online TA",
            "Offline TA/TO",
            "Complementary",
            "Groups",
            "Undefined",
            "Aviation"
        ].index(segment_default)
    )

    is_repeated_guest = st.selectbox(
        "Repeated Guest?",
        [0, 1],
        index=repeat_default,
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    previous_cancellations = st.number_input(
        "Previous Cancellations",
        min_value=0,
        max_value=50,
        value=previous_default
    )

    deposit_type = st.selectbox(
        "Deposit Type",
        ["No Deposit", "Refundable", "Non Refund"],
        index=[
            "No Deposit",
            "Refundable",
            "Non Refund"
        ].index(deposit_default)
    )

    total_of_special_requests = st.number_input(
        "Special Requests",
        min_value=0,
        max_value=5,
        value=requests_default
    )

# Booking summary
st.divider()
st.subheader("📌 Booking Summary")

summary1, summary2, summary3, summary4 = st.columns(4)

summary1.metric("🏨 Hotel", hotel)
summary2.metric("📅 Lead Time", f"{lead_time} days")
summary3.metric("🌙 Stay", f"{total_nights} nights")
summary4.metric("👥 Guests", total_guests)

st.divider()

# Prediction button
if st.button(
    "🔮 Analyze Booking",
    use_container_width=True
):

    # Prepare input
    input_data = pd.DataFrame([{
        "hotel": hotel,
        "lead_time": lead_time,
        "total_nights": total_nights,
        "total_guests": total_guests,
        "meal": meal,
        "market_segment": market_segment,
        "is_repeated_guest": is_repeated_guest,
        "previous_cancellations": previous_cancellations,
        "deposit_type": deposit_type,
        "total_of_special_requests": total_of_special_requests
    }])

    # Prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    percentage = probability * 100

    st.divider()
    st.subheader("📊 Prediction Result")

    # Result columns
    result1, result2, result3 = st.columns(3)

    with result1:
        st.metric(
            "Cancellation Probability",
            f"{percentage:.2f}%"
        )

    with result2:
        if prediction == 1:
            st.metric("Risk Level", "HIGH")
        else:
            st.metric("Risk Level", "LOW")

    with result3:
        if prediction == 1:
            st.metric("Decision", "Likely Cancel")
        else:
            st.metric("Decision", "Likely Stay")

    # Risk message
    if prediction == 1:

        st.error("⚠️ High Risk of Cancellation")

        st.write(
            "This booking has a higher predicted probability "
            "of being cancelled."
        )

        st.info(
            "💡 Suggested Action: Consider confirmation follow-up "
            "or additional reservation monitoring."
        )

    else:

        st.success("✅ Low Risk of Cancellation")

        st.write(
            "This booking has a lower predicted probability "
            "of being cancelled."
        )

        st.info(
            "💡 Suggested Action: Booking can be monitored normally."
        )

    # Probability meter
    st.write("### Cancellation Risk Meter")
    st.progress(float(probability))

    # Input factors
    st.write("### 🔍 Booking Factors")

    factor1, factor2, factor3 = st.columns(3)

    with factor1:
        st.write("**Lead Time**")
        st.write(f"{lead_time} days")

    with factor2:
        st.write("**Previous Cancellations**")
        st.write(previous_cancellations)

    with factor3:
        st.write("**Special Requests**")
        st.write(total_of_special_requests)