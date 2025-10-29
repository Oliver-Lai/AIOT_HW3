## ADDED Requirements

### Requirement: Data Loading and Preprocessing
The training system SHALL load SMS messages from the CSV dataset and prepare them for model training.

#### Scenario: Load valid CSV dataset
- **WHEN** `train.py` is executed
- **THEN** the system reads `sms_spam_no_header.csv` with two columns (label, text)
- **AND** the system validates that both columns are present
- **AND** the system prints the total number of loaded messages

#### Scenario: Handle missing dataset file
- **WHEN** `train.py` is executed and `sms_spam_no_header.csv` does not exist
- **THEN** the system raises a FileNotFoundError with a clear error message
- **AND** the system exits gracefully without creating a model file

### Requirement: Train-Test Split
The training system SHALL split the dataset into training and testing subsets for model evaluation.

#### Scenario: Split data with 80/20 ratio
- **WHEN** data is loaded successfully
- **THEN** the system splits the data into 80% training and 20% testing sets
- **AND** the system uses a fixed random state for reproducibility
- **AND** the system prints the sizes of training and testing sets

### Requirement: TF-IDF Vectorization
The training system SHALL convert text messages into TF-IDF feature vectors.

#### Scenario: Transform text to TF-IDF features
- **WHEN** training data is available
- **THEN** the system creates a TfidfVectorizer instance
- **AND** the system fits the vectorizer on training text
- **AND** the system transforms both training and testing text into TF-IDF matrices

### Requirement: Multinomial Naive Bayes Classification
The training system SHALL train a Multinomial Naive Bayes classifier on TF-IDF features.

#### Scenario: Train classifier on training data
- **WHEN** TF-IDF features are generated
- **THEN** the system creates a MultinomialNB instance
- **AND** the system trains the classifier on training features and labels
- **AND** the system completes training without errors

### Requirement: Model Evaluation
The training system SHALL evaluate model performance on the test set and report metrics.

#### Scenario: Compute accuracy metrics
- **WHEN** the model is trained
- **THEN** the system predicts labels for the test set
- **AND** the system calculates and prints overall accuracy
- **AND** the accuracy is displayed as a percentage

#### Scenario: Generate confusion matrix
- **WHEN** test predictions are available
- **THEN** the system generates a confusion matrix
- **AND** the system prints the confusion matrix showing true/false positives and negatives

#### Scenario: Generate classification report
- **WHEN** test predictions are available
- **THEN** the system generates a classification report with precision, recall, and F1-score
- **AND** the system prints the report showing metrics for both spam and ham classes

### Requirement: Model Serialization
The training system SHALL serialize the trained model pipeline to a file for later use.

#### Scenario: Save trained model to joblib file
- **WHEN** model training and evaluation are complete
- **THEN** the system creates a Pipeline combining TfidfVectorizer and MultinomialNB
- **AND** the system serializes the pipeline using joblib
- **AND** the system saves the pipeline to `spam_model.joblib`
- **AND** the system prints a confirmation message with the file path

#### Scenario: Verify model file is created
- **WHEN** serialization completes successfully
- **THEN** the file `spam_model.joblib` exists in the project directory
- **AND** the file size is greater than 0 bytes

### Requirement: Console Output and Logging
The training system SHALL provide clear feedback about training progress and results.

#### Scenario: Display training progress
- **WHEN** `train.py` is executed
- **THEN** the system prints status messages for each major step (loading, splitting, training, evaluating, saving)
- **AND** all messages are clearly formatted and easy to read
- **AND** the final output includes model performance metrics
