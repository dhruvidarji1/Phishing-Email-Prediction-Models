import streamlit as st

st.title("Phishing Email Detection")

st.markdown(
    "**Dataset:** [Hugging Face - Phishing Email Dataset](https://huggingface.co/datasets/simlab-vs/meajor_cleaned_preprocessed)  \n"
)

model = st.selectbox(
    "Select a model and enter an email to classify it as phishing or legitimate.",
    ["Logistic Regression", "Multinomial Naive Bayes", "BERT"]
)

sender = st.text_input("Sender Email")
receiver = st.text_input("Receiver Email")
subject = st.text_input("Subject")
body = st.text_area("Email Body")


if st.button("Predict"):
    st.write("Prediction coming soon...")
