# Project Context

## Purpose
The primary purpose of this project is to develop and deploy a machine learning model capable of accurately classifying text messages (SMS) as "Spam" or "Ham."

The project uses the `sms_spam_no_header.csv` dataset for training. Key goals include:

- Training an accurate classifier
- Providing a simple web interface, powered by Streamlit, for users to input text and get real-time predictions
- (Future Goal) Defining an OpenAPI specification to package this model as an API service

## Tech Stack
- **Primary Language:** Python
- **Machine Learning:** Scikit-learn (sklearn)
- **Web App Framework:** Streamlit
- **Data Handling (Training):** Pandas
- **Model Serialization:** Joblib

## Project Conventions

### Code Style
- Follows standard Python PEP 8 style guidelines
- Variable names are descriptive (e.g., `vectorizer`, `model`, `user_input`)
- Clear project structure separation:
  - `train.py`: For model training, evaluation, and serialization
  - `app.py`: For the Streamlit application logic and interface
  - `spam_model.joblib`: The saved, pre-trained model pipeline

### Architecture Patterns
This project uses a **Pre-trained Model** architecture:

**Offline Training** (`train.py`):
- Loads `sms_spam_no_header.csv` data
- Performs feature engineering using TfidfVectorizer
- Trains a classifier using the MultinomialNB algorithm
- The TfidfVectorizer and MultinomialNB are packaged (using joblib) and serialized into a single `spam_model.joblib` file

**Online Inference** (`app.py`):
- The Streamlit application loads this `spam_model.joblib` file on startup
- When a user submits text via the interface, the app calls the loaded model's `.predict()` and `.predict_proba()` methods for inference
- The prediction (Spam/Ham) and confidence score are displayed in real-time on the web page

This approach cleanly separates the complex training process from the lightweight inference service.

### Testing Strategy
**Model Testing** (`train.py`):
- In the training script, data is split into training and testing sets (e.g., 80/20 split)
- Model performance is evaluated using Accuracy, Confusion Matrix, and a Classification Report, with results printed to the console

**Application Testing** (Manual):
- `app.py` is verified through manual testing
- Method: Input known spam and ham strings into the Streamlit interface to confirm the UI correctly displays the prediction and corresponding confidence score

### Git Workflow
- Currently uses a single-branch (`main`) workflow
- All development, training scripts, and application code are committed directly to the `main` branch

## Domain Context
- **Spam vs. Ham:** In this context, "Spam" refers to unsolicited junk messages. "Ham" is the technical term for legitimate, non-spam messages.
- **TF-IDF (Term Frequency-Inverse Document Frequency):** The core feature extraction technique. It converts raw text into a numerical matrix, reflecting the importance of each word within a message and across the entire dataset.
- **Multinomial Naive Bayes (MultinomialNB):** The chosen classification algorithm. It is highly efficient and effective for text classification tasks, especially with TF-IDF features, and serves as a strong baseline.

## Important Constraints
- **Model Scope:** The model is trained only on the `sms_spam_no_header.csv` dataset. Its effectiveness on other types of text (e.g., emails, social media posts) is not guaranteed.
- **Deployment Environment:** The application (`app.py`) is designed to run in a Streamlit environment. The model file (`.joblib`) is loaded directly into the application's memory on startup.

## External Dependencies
- **Python Packages** (via `requirements.txt`): The project relies on `scikit-learn`, `pandas`, `streamlit`, and `joblib`
- **Application Hosting:** The public web app is hosted and served by Streamlit Community Cloud
- **Code Hosting:** The project source code and dataset are hosted on GitHub
