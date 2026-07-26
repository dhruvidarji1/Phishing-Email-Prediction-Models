import streamlit as st

st.title("Phishing Email Detection")

email = st.text_area("Enter an email")

if st.button("Predict"):
    st.write("Prediction coming soon...")