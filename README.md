# Phishing Email Prediction Models
- This project uses machine learning to classify emails as either phishing or legitimate.
- The goal was to compare multiple models and determine which one provided the best balance of accuracy, precision, recall, and F1 score.

# Models Used
- Logistic Regression
- Multinomial Naive Bayes
- BERT

# Dataset
- The project uses the MeAJOR Email Corpus dataset, which contains approximately 108,685 labeled emails.
- Main features include: email subject and body, sender information, URLs and attachments, email length, punctuation and typo patterns

# Results
- Logistic Regression: Accuracy: 99.28% / F1 Score: 99.38%
- BERT: Accuracy: 98.00% / F1 Score: 99.00%
- Multinomial Naive Bayes: Accuracy: 96.03% / F1 Score: 95.38%

# Streamlit Application
- The repository includes a Streamlit application where users can enter email information, view extracted features, and receive a phishing or legitimate prediction.
  
