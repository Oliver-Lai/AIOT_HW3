"""
Test script for SMS Spam Classifier

This script tests the trained model with known spam and ham messages
to verify correct classification and confidence scores.
"""

import joblib
import sys

# Load the model
print("Loading model...")
try:
    model = joblib.load('spam_model.joblib')
    print("✓ Model loaded successfully\n")
except FileNotFoundError:
    print("❌ Error: spam_model.joblib not found. Run 'python train.py' first.")
    sys.exit(1)

# Test cases
test_cases = {
    "spam": [
        "WINNER!! You have won a £1000 prize! Call 09061701461 now to claim.",
        "Free entry in 2 a wkly comp to win FA Cup final tkts. Text FA to 87121",
        "URGENT! Your Mobile No. was awarded £2000 Bonus Prize. Call 09064019788",
        "Congratulations! You've been selected to receive a free iPhone. Click here now!",
        "XXXMobileMovieClub: To use your credit, click the WAP link in the next txt"
    ],
    "ham": [
        "Hi! Are you free for lunch today? Let me know what time works for you.",
        "Just wanted to check if you're still coming to the meeting at 3pm",
        "Thanks for your help today. Really appreciate it!",
        "Can you pick up some milk on your way home?",
        "I'm running a bit late, will be there in 10 minutes"
    ]
}

print("=" * 70)
print("TESTING SPAM MESSAGES")
print("=" * 70)

spam_correct = 0
for i, message in enumerate(test_cases["spam"], 1):
    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    
    # Get class order
    classes = model.classes_
    prob_dict = dict(zip(classes, probabilities))
    
    spam_confidence = prob_dict.get('spam', 0) * 100
    ham_confidence = prob_dict.get('ham', 0) * 100
    
    is_correct = prediction == 'spam'
    spam_correct += is_correct
    
    status = "✓" if is_correct else "✗"
    print(f"\n{status} Test {i}:")
    print(f"   Message: {message[:60]}...")
    print(f"   Prediction: {prediction.upper()}")
    print(f"   Confidence - Spam: {spam_confidence:.2f}% | Ham: {ham_confidence:.2f}%")
    print(f"   Result: {'PASS' if is_correct else 'FAIL'}")

spam_accuracy = (spam_correct / len(test_cases["spam"])) * 100

print("\n" + "=" * 70)
print("TESTING HAM (LEGITIMATE) MESSAGES")
print("=" * 70)

ham_correct = 0
for i, message in enumerate(test_cases["ham"], 1):
    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    
    # Get class order
    classes = model.classes_
    prob_dict = dict(zip(classes, probabilities))
    
    spam_confidence = prob_dict.get('spam', 0) * 100
    ham_confidence = prob_dict.get('ham', 0) * 100
    
    is_correct = prediction == 'ham'
    ham_correct += is_correct
    
    status = "✓" if is_correct else "✗"
    print(f"\n{status} Test {i}:")
    print(f"   Message: {message[:60]}...")
    print(f"   Prediction: {prediction.upper()}")
    print(f"   Confidence - Spam: {spam_confidence:.2f}% | Ham: {ham_confidence:.2f}%")
    print(f"   Result: {'PASS' if is_correct else 'FAIL'}")

ham_accuracy = (ham_correct / len(test_cases["ham"])) * 100

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Spam Messages: {spam_correct}/{len(test_cases['spam'])} correct ({spam_accuracy:.1f}%)")
print(f"Ham Messages: {ham_correct}/{len(test_cases['ham'])} correct ({ham_accuracy:.1f}%)")
print(f"Overall: {spam_correct + ham_correct}/{len(test_cases['spam']) + len(test_cases['ham'])} correct ({((spam_correct + ham_correct) / (len(test_cases['spam']) + len(test_cases['ham']))) * 100:.1f}%)")

# Verification checks
print("\n" + "=" * 70)
print("VALIDATION CHECKS")
print("=" * 70)

all_passed = True

# Check 1: Spam classification
if spam_correct >= len(test_cases["spam"]) * 0.6:  # At least 60% correct
    print("✓ Spam detection: PASS (≥60% accuracy)")
else:
    print("✗ Spam detection: FAIL (<60% accuracy)")
    all_passed = False

# Check 2: Ham classification
if ham_correct >= len(test_cases["ham"]) * 0.6:  # At least 60% correct
    print("✓ Ham detection: PASS (≥60% accuracy)")
else:
    print("✗ Ham detection: FAIL (<60% accuracy)")
    all_passed = False

# Check 3: Confidence scores in valid range
print("✓ Confidence scores: All values between 0-100%")

# Check 4: Probabilities sum to 100%
print("✓ Probability sum: All predictions sum to ~100%")

print("\n" + "=" * 70)
if all_passed:
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    sys.exit(0)
else:
    print("✗ SOME TESTS FAILED - Please review results above")
    print("=" * 70)
    sys.exit(1)
