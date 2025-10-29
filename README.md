# SMS Spam Classifier

A machine learning-powered SMS spam classification system with a user-friendly web interface built using Streamlit.

## Project Overview

This project implements a complete spam detection pipeline that:
- Trains a machine learning model to classify SMS messages as "Spam" or "Ham" (legitimate)
- Uses TF-IDF (Term Frequency-Inverse Document Frequency) for feature extraction
- Employs Multinomial Naive Bayes algorithm for classification
- Provides a real-time web interface for spam detection

## Features

- **High Accuracy**: Achieves ≥95% accuracy on test data
- **Real-time Predictions**: Instant classification with confidence scores
- **User-friendly Interface**: Simple Streamlit web app for non-technical users
- **Dataset Visualizations**: Interactive charts showing data distribution and message length analysis
- **Lightweight Model**: Compact model size suitable for cloud deployment

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. Clone this repository or download the project files

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

The required packages are:
- `scikit-learn` - Machine learning library
- `pandas` - Data manipulation and analysis
- `streamlit` - Web application framework
- `plotly` - Interactive data visualization library
- `joblib` - Model serialization

## Usage

### Step 1: Train the Model

Before using the web application, you need to train the spam classifier:

```bash
python train.py
```

This will:
- Load the SMS dataset (`sms_spam_no_header.csv`)
- Split data into training (80%) and testing (20%) sets
- Train a TF-IDF + Multinomial Naive Bayes classifier
- Evaluate model performance and print metrics
- Save the trained model as `spam_model.joblib`

**Expected Output:**
- Dataset statistics (number of messages)
- Training/testing set sizes
- Model accuracy (typically >95%)
- Confusion matrix
- Classification report (precision, recall, F1-score)

### Step 2: Run the Web Application

After training the model, launch the Streamlit web app:

```bash
streamlit run app.py
```

The application will:
- Open automatically in your default web browser
- Display at `http://localhost:8501`
- Provide a text input field for entering SMS messages
- Show real-time predictions with confidence scores

### Using the Web Interface

1. Enter an SMS message in the text area
2. Click the "Classify" button (or the app may predict automatically)
3. View the prediction result:
   - **Spam**: Message classified as unsolicited/junk
   - **Ham**: Message classified as legitimate
4. Check the confidence score to assess prediction reliability
5. Explore the dataset overview section to understand:
   - Distribution of spam vs. ham messages in the training data
   - Message length patterns and statistics
   - Visual insights through interactive charts (pie chart, bar chart, box plot)

## Dataset

The project uses the `sms_spam_no_header.csv` dataset containing approximately 5,500 SMS messages labeled as either "spam" or "ham". 

**Dataset Format:**
- Two columns: label (spam/ham) and message text
- No header row
- CSV format with quoted strings

**Dataset Distribution:**
- Total messages: 5,574
- Ham (legitimate) messages: 4,827 (86.6%)
- Spam messages: 747 (13.4%)

## Example Usage

### Example 1: Spam Message Detection
**Input:**
```
Congratulations! You've won a $1000 gift card. Click here to claim now!
```

**Expected Output:**
- Classification: **🚨 SPAM**
- Confidence: ~95-99%
- Visual: Red background indicating spam

### Example 2: Legitimate Message Detection
**Input:**
```
Hey, are we still meeting for coffee at 3pm today?
```

**Expected Output:**
- Classification: **✅ HAM (Legitimate)**
- Confidence: ~98-100%
- Visual: Green background indicating legitimate message

### Example 3: Dataset Visualization Features

When you open the web app, you'll see:

1. **Dataset Statistics Section**
   - Total message count
   - Number and percentage of spam messages
   - Number and percentage of ham messages

2. **Distribution Pie Chart**
   - Visual representation of spam vs. ham ratio
   - Interactive hover showing exact counts
   - Color-coded: Green (Ham), Red (Spam)

3. **Message Count Bar Chart**
   - Side-by-side comparison of message types
   - Displays exact counts on bars
   - Clear visual comparison

4. **Message Length Box Plot**
   - Shows distribution of message lengths for both types
   - Displays median, quartiles, and outliers
   - Includes mean and standard deviation
   - Reveals that spam messages tend to be longer on average

5. **Statistical Summary**
   - Average message length (Ham vs. Spam)
   - Median message length
   - Maximum message length
   - Helps understand dataset characteristics

## Architecture

### Training Pipeline (`train.py`)
```
Load CSV → Train/Test Split → TF-IDF Vectorization → 
Naive Bayes Classifier → Evaluation → Model Serialization
```

### Inference Pipeline (`app.py`)
```
Load Model → User Input → TF-IDF Transform → 
Prediction → Display Result + Confidence
```

## Model Details

- **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Algorithm**: Multinomial Naive Bayes
- **Training Split**: 80% training, 20% testing
- **Model File**: `spam_model.joblib` (serialized pipeline)

## Known Limitations

1. **Dataset Specificity**: The model is trained on SMS messages from 2012. Performance on modern messaging platforms (social media, instant messaging apps) may vary.

2. **Language Support**: English-only. The model is not trained for multilingual spam detection.

3. **Context Understanding**: The model analyzes text patterns and keywords but doesn't understand context or sarcasm.

4. **Adversarial Resistance**: Sophisticated spam that mimics legitimate messages may not be detected.

5. **No Real-time Learning**: The model requires retraining to adapt to new spam patterns. It does not learn from user feedback.

## Performance Metrics

Expected performance on test set:
- **Accuracy**: ≥95%
- **Precision** (Spam): ~95-98%
- **Recall** (Spam): ~85-90%
- **F1-Score**: ~90-93%

*Note: Actual metrics will be displayed when you run `train.py`*

## Project Structure

```
HW3/
├── train.py                  # Model training script
├── app.py                    # Streamlit web application
├── requirements.txt          # Python dependencies
├── sms_spam_no_header.csv   # Training dataset
├── spam_model.joblib        # Trained model (generated)
├── README.md                # This file
└── openspec/                # OpenSpec documentation
```

## Deployment

### Local Deployment
Follow the installation and usage steps above.

### Cloud Deployment (Streamlit Community Cloud)

#### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

#### Deployment Steps

1. **Prepare Your Repository**
   ```bash
   # Initialize git repository (if not already done)
   git init
   
   # Add all project files
   git add .
   
   # Commit changes
   git commit -m "Add SMS spam classifier application"
   
   # Create a new repository on GitHub and push
   git remote add origin https://github.com/yourusername/sms-spam-classifier.git
   git branch -M main
   git push -u origin main
   ```

2. **Important Files to Include**
   - `app.py` - Main Streamlit application
   - `spam_model.joblib` - Pre-trained model file
   - `requirements.txt` - Python dependencies
   - `sms_spam_no_header.csv` - Dataset (for visualizations)
   - `README.md` - Documentation

3. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Verify Deployment**
   - Wait for the app to build (2-5 minutes)
   - Test the prediction functionality
   - Verify dataset visualizations load correctly
   - Check that the model file loads successfully

#### Deployment Notes
- The free tier of Streamlit Cloud has memory and CPU limitations
- The TF-IDF + Naive Bayes model is lightweight and fits within free tier constraints
- Model loading is cached to improve performance
- Dataset loading is cached for visualization efficiency

#### Troubleshooting Deployment
- **Build fails**: Check that all files are committed to GitHub
- **Model not found**: Ensure `spam_model.joblib` is in the repository (not in `.gitignore`)
- **Import errors**: Verify all dependencies are listed in `requirements.txt`
- **Memory issues**: The current implementation should fit in free tier limits

### Alternative Deployment Options

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t sms-spam-classifier .
docker run -p 8501:8501 sms-spam-classifier
```

#### Heroku Deployment
1. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

2. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Troubleshooting

**Problem**: `FileNotFoundError: sms_spam_no_header.csv not found`
- **Solution**: Ensure the dataset file is in the same directory as `train.py`

**Problem**: `FileNotFoundError: spam_model.joblib not found`
- **Solution**: Run `python train.py` first to generate the model file

**Problem**: Low accuracy (<90%)
- **Solution**: Check dataset quality and ensure proper train/test split

**Problem**: Streamlit app won't start
- **Solution**: Verify all dependencies are installed: `pip install -r requirements.txt`

## Future Enhancements

- REST API endpoints for integration with other services
- Batch prediction mode (upload CSV files)
- Model retraining interface
- Support for additional languages
- Real-time feedback and model improvement
- Advanced deep learning models (LSTM, BERT)

## Technical Stack

- **Python**: 3.8+
- **scikit-learn**: Machine learning algorithms and utilities
- **Pandas**: Data manipulation
- **Streamlit**: Web framework
- **Plotly**: Interactive data visualizations
- **Joblib**: Model persistence

## License

This is an educational project for learning purposes.

## Acknowledgments

- Dataset source: UCI Machine Learning Repository / Kaggle
- Built with scikit-learn and Streamlit frameworks
