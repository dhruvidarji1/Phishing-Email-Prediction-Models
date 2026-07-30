import streamlit as st

st.title("Phishing Email Detection")

sender = st.text_input("Sender Email")
receiver = st.text_input("Receiver Email")
subject = st.text_input("Subject")
body = st.text_area("Email Body")


if st.button("Predict"):
    st.write("Prediction coming soon...")