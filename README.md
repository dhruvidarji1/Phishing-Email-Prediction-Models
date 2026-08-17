# Phishing Email Prediction Models
- This project uses machine learning to classify emails as either phishing or legitimate.
- The goal was to compare multiple models and determine which one provided the best balance of accuracy, precision, recall, and F1 score.

# Problem Statement

Phishing is one of the most common cybersecurity threats, affecting individuals, businesses, and organizations. Since email remains a primary method of communication, email security matters for everyday users, and phishing messages are becoming increasingly sophisticated and harder to distinguish from legitimate mail. Automated detection helps identify suspicious emails faster and at a larger scale than manual review, reducing human error and giving users a warning before they interact with malicious content. This project explores which machine learning approach best supports that kind of detection.

# Models Used
- Logistic Regression
- Multinomial Naive Bayes
- BERT

# Methodology

We sourced 108,685 labeled emails from the MeAJOR Email Corpus and narrowed the available columns down to a smaller, more comparable feature set (email text, length, punctuation, typos, sender domain, URLs, and attachments) after finding that using every column made fair model comparison difficult. Each model was trained and evaluated independently in its own notebook, then compared using accuracy, precision, recall, and F1 score. 

Logistic Regression used TF-IDF vectorization of the email text and served as a fast, strong baseline.
Multinomial Naive Bayes used word frequency features, offering efficient training on large volumes of text.
BERT was fine tuned to capture contextual and semantic meaning in the email body rather than relying on surface level keyword patterns.

# Dataset
- The project uses the MeAJOR Email Corpus dataset, which contains approximately 108,685 labeled emails.
- Main features include: email subject and body, sender information, URLs and attachments, email length, punctuation and typo patterns

# Results
- Logistic Regression: Accuracy: 99.28% / F1 Score: 99.38%
- BERT: Accuracy: 98.00% / F1 Score: 99.00%
- Multinomial Naive Bayes: Accuracy: 96.03% / F1 Score: 95.38%

# Streamlit Application
- The repository includes a Streamlit application where users can enter email information, view extracted features, and receive a phishing or legitimate prediction.
  
# Technologies Used
- Python
- Streamlit
- Scikit-learn
- Hugging Face Transformers
- PyTorch
- Pandas
- Joblib
