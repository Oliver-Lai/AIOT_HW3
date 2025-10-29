"""
SMS Spam Classifier - Training Script

This script trains a machine learning model to classify SMS messages as spam or ham.
It uses TF-IDF vectorization and Multinomial Naive Bayes classification.

Usage:
    python train.py

Output:
    - Prints training progress and evaluation metrics
    - Saves trained model to 'spam_model.joblib'
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os
import sys


def load_dataset(file_path='sms_spam_no_header.csv'):
    """
    Load SMS dataset from CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: Loaded dataset with 'label' and 'text' columns
        
    Raises:
        FileNotFoundError: If the dataset file doesn't exist
    """
    print("=" * 60)
    print("SMS SPAM CLASSIFIER - TRAINING")
    print("=" * 60)
    print()
    
    print(f"[1/6] Loading dataset from '{file_path}'...")
    
    if not os.path.exists(file_path):
        error_msg = f"Dataset file '{file_path}' not found. Please ensure the file exists in the current directory."
        print(f"ERROR: {error_msg}")
        raise FileNotFoundError(error_msg)
    
    try:
        # Load CSV with no header, two columns: label and text
        df = pd.read_csv(file_path, header=None, names=['label', 'text'])
        
        # Validate that we have the expected columns
        if len(df.columns) != 2:
            raise ValueError(f"Expected 2 columns, but found {len(df.columns)}")
        
        # Validate that we have data
        if len(df) == 0:
            raise ValueError("Dataset is empty")
        
        print(f"✓ Successfully loaded {len(df)} messages")
        print(f"  - Spam messages: {len(df[df['label'] == 'spam'])}")
        print(f"  - Ham messages: {len(df[df['label'] == 'ham'])}")
        print()
        
        return df
        
    except Exception as e:
        print(f"ERROR: Failed to load dataset: {e}")
        raise


def split_data(df, test_size=0.2, random_state=42):
    """
    Split dataset into training and testing sets.
    
    Args:
        df (pandas.DataFrame): Dataset to split
        test_size (float): Proportion of data to use for testing (default: 0.2)
        random_state (int): Random seed for reproducibility (default: 42)
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    print(f"[2/6] Splitting data into train/test sets (80/20 split)...")
    
    X = df['text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y  # Maintain class distribution
    )
    
    print(f"✓ Data split complete")
    print(f"  - Training set: {len(X_train)} messages")
    print(f"  - Testing set: {len(X_test)} messages")
    print()
    
    return X_train, X_test, y_train, y_test


def create_and_train_model(X_train, y_train):
    """
    Create a TF-IDF + Multinomial Naive Bayes pipeline and train it.
    
    Args:
        X_train: Training text data
        y_train: Training labels
        
    Returns:
        sklearn.pipeline.Pipeline: Trained model pipeline
    """
    print("[3/6] Creating and training model...")
    print("  - Vectorizer: TF-IDF (Term Frequency-Inverse Document Frequency)")
    print("  - Classifier: Multinomial Naive Bayes")
    print()
    
    # Create pipeline: TF-IDF vectorization + Multinomial Naive Bayes
    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    
    # Train the model
    print("  Training in progress...")
    model.fit(X_train, y_train)
    
    print("✓ Model training complete")
    print()
    
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance on test set.
    
    Args:
        model: Trained model pipeline
        X_test: Testing text data
        y_test: Testing labels
        
    Returns:
        dict: Evaluation metrics
    """
    print("[4/6] Evaluating model performance...")
    print()
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=['ham', 'spam'])
    
    # Generate classification report
    report = classification_report(y_test, y_pred, target_names=['ham', 'spam'])
    
    # Print results
    print("=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print()
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print()
    print("Confusion Matrix:")
    print("                  Predicted")
    print("                  Ham    Spam")
    print(f"Actual   Ham     {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"         Spam    {cm[1][0]:5d}  {cm[1][1]:5d}")
    print()
    print("Classification Report:")
    print(report)
    print("=" * 60)
    print()
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'classification_report': report
    }


def save_model(model, file_path='spam_model.joblib'):
    """
    Serialize and save the trained model to disk.
    
    Args:
        model: Trained model pipeline
        file_path (str): Path where model will be saved
    """
    print(f"[5/6] Saving trained model to '{file_path}'...")
    
    # Save model using joblib
    joblib.dump(model, file_path)
    
    # Verify file was created
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        print(f"✓ Model saved successfully")
        print(f"  - File: {file_path}")
        print(f"  - Size: {file_size_kb:.2f} KB")
    else:
        raise IOError(f"Failed to create model file: {file_path}")
    
    print()


def main():
    """
    Main training pipeline execution.
    """
    try:
        # Step 1: Load dataset
        df = load_dataset('sms_spam_no_header.csv')
        
        # Step 2: Split data
        X_train, X_test, y_train, y_test = split_data(df)
        
        # Step 3: Create and train model
        model = create_and_train_model(X_train, y_train)
        
        # Step 4: Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        
        # Step 5: Save model
        save_model(model, 'spam_model.joblib')
        
        # Final summary
        print("[6/6] Training pipeline complete!")
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"✓ Model trained and saved successfully")
        print(f"✓ Test accuracy: {metrics['accuracy']*100:.2f}%")
        print()
        print("Next steps:")
        print("  1. Run the web app: streamlit run app.py")
        print("  2. Test predictions with your own SMS messages")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print("TRAINING FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Please check the error message above and try again.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
