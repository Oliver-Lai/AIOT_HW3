# Design: SMS Spam Classifier System

## Context
This is the initial implementation of an SMS spam classification system. The project currently has only the dataset (`sms_spam_no_header.csv`) and needs a complete end-to-end machine learning pipeline with a user-friendly interface.

**Background:**
- Dataset: ~5,500 SMS messages labeled as "spam" or "ham"
- Target users: End users who want to check if a message is spam
- Deployment: Streamlit Community Cloud for easy public access

**Constraints:**
- Must use existing dataset format (CSV with label and text columns, no header)
- Must be deployable on Streamlit Community Cloud (memory and performance constraints)
- Must provide real-time inference (<1 second response time)

## Goals / Non-Goals

**Goals:**
- ✅ Accurate spam classification (target: ≥95% accuracy on test set)
- ✅ Simple, intuitive web interface for non-technical users
- ✅ Fast inference time for real-time predictions
- ✅ Clear separation between training and inference code
- ✅ Easy deployment to Streamlit Community Cloud

**Non-Goals:**
- ❌ Real-time model retraining (model is pre-trained offline)
- ❌ User authentication or session management
- ❌ Database storage of predictions
- ❌ Support for multiple languages (dataset is English-only)
- ❌ API endpoints (future work, noted in project.md)

## Decisions

### Decision 1: TF-IDF + Multinomial Naive Bayes
**Rationale:**
- TF-IDF captures word importance effectively for short text messages
- Multinomial Naive Bayes is proven effective for text classification
- Fast training and inference (critical for Streamlit deployment)
- Interpretable results (can explain predictions if needed)
- Small model size (fits in memory constraints)

**Alternatives considered:**
- Word2Vec + LSTM: Rejected due to complexity, training time, and larger model size
- BERT-based models: Rejected due to computational requirements exceeding Streamlit Cloud limits
- Simple keyword matching: Rejected due to poor accuracy and inability to handle variations

### Decision 2: Offline Training + Serialized Model
**Rationale:**
- Training is computationally expensive (done once offline)
- Streamlit app only needs to load pre-trained model (fast startup)
- Model file (<1MB) is easily version controlled
- Simplifies deployment (no training dependencies in production)

**Alternatives considered:**
- Online training: Rejected due to slow app startup and unnecessary complexity
- Train-on-demand: Rejected due to poor user experience (long wait times)

### Decision 3: Joblib for Model Serialization
**Rationale:**
- Standard in scikit-learn ecosystem
- Efficient compression for scikit-learn models
- Simple API (dump/load)
- Cross-platform compatibility

**Alternatives considered:**
- Pickle: Rejected due to potential security issues and less efficient compression
- ONNX: Rejected due to unnecessary complexity for this use case

### Decision 4: Streamlit for Web Interface
**Rationale:**
- Rapid development (minimal boilerplate code)
- Python-native (no separate frontend framework needed)
- Built-in UI components (text input, buttons, layout)
- Easy deployment to Streamlit Community Cloud
- Automatic reactivity and state management

**Alternatives considered:**
- Flask + HTML/CSS: Rejected due to longer development time
- FastAPI + React: Rejected due to complexity and deployment overhead
- Gradio: Considered but Streamlit preferred for richer customization

### Decision 5: Single Pipeline Object (TF-IDF + Classifier)
**Rationale:**
- Ensures vectorizer and classifier are always in sync
- Simplifies serialization (one file instead of two)
- Reduces risk of version mismatches
- Cleaner inference code (single .predict() call)

**Implementation:**
```python
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])
```

## Architecture

### System Overview
```
┌─────────────────────┐
│  train.py           │
│  (Offline)          │
│                     │
│  1. Load CSV        │
│  2. Train/Test Split│
│  3. TF-IDF + NB     │
│  4. Evaluate        │
│  5. Serialize       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ spam_model.joblib   │
│ (Serialized Model)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  app.py             │
│  (Streamlit App)    │
│                     │
│  1. Load Model      │
│  2. Accept Input    │
│  3. Predict         │
│  4. Display Result  │
└─────────────────────┘
```

### File Structure
```
HW3/
├── train.py              # Training script
├── app.py                # Streamlit web app
├── requirements.txt      # Python dependencies
├── spam_model.joblib     # Serialized model (generated)
├── sms_spam_no_header.csv # Dataset
├── README.md             # Documentation
└── openspec/             # OpenSpec files
```

### Data Flow

**Training Flow:**
1. `train.py` reads `sms_spam_no_header.csv`
2. Splits data 80/20 (train/test)
3. Fits TfidfVectorizer on training text
4. Trains MultinomialNB on TF-IDF features
5. Evaluates on test set
6. Serializes pipeline to `spam_model.joblib`

**Inference Flow:**
1. `app.py` loads `spam_model.joblib` at startup
2. User enters text in Streamlit UI
3. Pipeline transforms text → TF-IDF features → prediction
4. App displays "Spam" or "Ham" + confidence score

## Risks / Trade-offs

### Risk 1: Model Drift
**Risk:** Model trained on 2012-era SMS may not generalize to modern messaging patterns
**Mitigation:** 
- Document dataset limitations clearly
- Plan for model retraining with updated data (future work)
- Monitor prediction confidence scores for anomalies

### Risk 2: Adversarial Inputs
**Risk:** Users may craft messages to fool the classifier
**Impact:** Low (educational project, not production security system)
**Mitigation:** Document as known limitation

### Risk 3: Memory Constraints on Streamlit Cloud
**Risk:** Model size or app memory usage exceeds free tier limits
**Mitigation:**
- Keep model compact (TF-IDF + NB < 1MB)
- Avoid loading large libraries unnecessarily
- Test deployment early

### Risk 4: CSV Format Assumptions
**Risk:** Dataset must have exactly 2 columns (label, text) with no header
**Mitigation:**
- Validate data format in `train.py` with assertions
- Document expected format in README

### Trade-off: Accuracy vs. Simplicity
**Decision:** Chose Naive Bayes over deep learning
**Gained:** Fast inference, small model, easy deployment
**Lost:** Potential 2-3% accuracy improvement (acceptable for this use case)

## Migration Plan
N/A - This is the initial implementation (no migration needed)

## Open Questions
1. **Should we add a "Report Mistake" feature?**
   - Decision: No (out of scope for MVP; can be future enhancement)

2. **Should we display model confidence threshold?**
   - Decision: Yes, display probability score to help users assess confidence

3. **Should we log predictions for analysis?**
   - Decision: No (privacy concerns and unnecessary complexity for MVP)

4. **Should we support batch predictions (upload CSV)?**
   - Decision: No (single-message prediction is sufficient for MVP; can add later)
