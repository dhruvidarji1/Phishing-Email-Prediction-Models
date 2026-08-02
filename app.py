import re
import string
from collections import Counter

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Phishing Email Detection",
                    page_icon="📧", 
                    layout="wide")

#TBD will be replaced with actual model final values
MODEL_METRICS = {  
    "Logistic Regression": {
        "Accuracy": "TBD",
        "Precision": "TBD",
        "Recall": "TBD",
        "F1 Score": "TBD"
    },
    "Multinomial Naive Bayes": {
        "Accuracy": "TBD",
        "Precision": "TBD",
        "Recall": "TBD",
        "F1 Score": "TBD"
    },
    "BERT": {
        "Accuracy": "TBD",
        "Precision": "TBD",
        "Recall": "TBD",
        "F1 Score": "TBD"
    }
}

FEATURE_COLUMNS = [
    "body_length",
    "email_length",
    "sender_domain_length",
    "subject_length",
    "punctuation_count",
    "word_frequency"
]

def get_sender_domain(sender: str) -> str:
    """Extract the domain from the sender's email address."""
    if "@" not in sender:
        return ""
    return sender.rsplit("@", 1)[1].strip().lower()

def calculate_word_frequency(text: str) -> float:
    """
    Calculate how frequently the most common word appears.

    Example:
    'verify your account verify now'
    Most common word: verify
    Frequency: 2 / 5 = 0.40

    This definition must be checked against the model notebooks.
    """
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    if not words:
        return 0.0

    word_counts = Counter(words)
    most_common_count = word_counts.most_common(1)[0][1]

    return most_common_count / len(words)

def calculate_features(
    sender: str,
    receiver: str,
    subject: str,
    body: str,
) -> dict:
    """Calculate engineered features from the submitted email address."""

    sender = sender.strip()
    receiver = receiver.strip()
    subject = subject.strip()
    body = body.strip()

    sender_domain = get_sender_domain(sender)
    combined_text = f"{subject} {body}".strip()

    features = {
        "body_length": len(body),

        # Confirm this definition with the notebooks.
        "email_length": len(subject) + len(body),

        "sender_domain_length": len(sender_domain),

        "subject_length": len(subject),

        # Counts punctuation in the subject and body.
        "punctuation_count": sum(
            character in string.punctuation
            for character in combined_text
        ),

        # Confirm this definition with the notebooks.
        "word_frequency": round(
            calculate_word_frequency(combined_text),
            4
        )
    }

    return {
        column: features[column]
        for column in FEATURE_COLUMNS
    }

st.title("📧 Phishing Email Detection")

st.write(
    "Select a model and enter an email to classify it as phishing or legitimate."
)

st.markdown(
    "**Dataset:** [Hugging Face - Phishing Email Dataset](https://huggingface.co/datasets/simlab-vs/meajor_cleaned_preprocessed)  \n"
)

st.divider()

#Model dashboard
st.subheader("Model Dashboard")

selected_model = st.selectbox(
    "Select a model to view its metrics.",
    list(MODEL_METRICS.keys())
)

selected_metrics = MODEL_METRICS[selected_model]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", selected_metrics["Accuracy"])
col2.metric("Precision", selected_metrics["Precision"])
col3.metric("Recall", selected_metrics["Recall"])
col4.metric("F1 Score", selected_metrics["F1 Score"])

st.caption("Replace TBD values after corrected models are evaluated")

st.divider()

# Email form
st.subheader("Analyze an Email")

with st.form(key="email_form"):
    sender = st.text_input("Sender Email", 
                        placeholder="sender@example.com")
    receiver = st.text_input("Receiver Email",
                        placeholder="receiver@example.com")
    subject = st.text_input("Subject",
                        placeholder="Enter the email's subject here")
    body = st.text_area("Email Body", 
                        placeholder="Enter the email's body here",
                        height=220)
    
    submitted = st.form_submit_button("Analyze Email", 
                                      type = "primary", 
                                      use_container_width=True)

if submitted:
    if not sender:
        st.warning("Please enter the sender's email address.")

    elif "@" not in sender:
        st.warning("Please enter a valid sender email address.")

    elif not subject and not body:
        st.warning("Please enter either the email's subject or body.")

    else:
        features = calculate_features(
            sender=sender,
            receiver=receiver,
            subject=subject,
            body=body
        )

        st.success("Email features calculated successfully!")

        st.subheader("Engineered Features")
        st.dataframe(pd.DataFrame([features]),
                     hide_index=True, 
                     use_container_width=True)

        st.info(
            f"{selected_model} is selected. "
            "Prediction will be added after the model is connected."
        )
