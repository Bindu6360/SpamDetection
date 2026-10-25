# Spam Detection Model Training Script
# This script trains a machine learning model to classify emails/messages as Spam or Not Spam

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import os

# Sample Spam Dataset
# Format: (message, label) where label = 1 for Spam, 0 for Not Spam
SPAM_DATA = [
    ("Click here to claim your free prize now!!!", 1),
    ("Congratulations! You have won a lottery prize", 1),
    ("URGENT: Verify your bank account immediately", 1),
    ("Limited time offer: Get 50% OFF today only", 1),
    ("You have been selected as our grand prize winner", 1),
    ("Call now for FREE consultation on weight loss", 1),
    ("Viagra online - No prescription needed", 1),
    ("Work from home and earn $5000 per week", 1),
    ("ALERT: Your account has been compromised, click here", 1),
    ("You are selected to receive $1,000,000", 1),
    ("Hi, how are you doing today?", 0),
    ("Let's catch up for coffee this weekend", 0),
    ("The meeting is scheduled for tomorrow at 2 PM", 0),
    ("Thanks for your help with the project", 0),
    ("I wanted to follow up on our previous discussion", 0),
    ("Are you free for a quick call?", 0),
    ("Please send me the updated report", 0),
    ("Great work on the presentation yesterday", 0),
    ("Looking forward to hearing from you", 0),
    ("Can we reschedule our meeting?", 0),
    ("Free money waiting for you", 1),
    ("Congratulations you are selected", 1),
    ("Click here to verify account", 1),
    ("Claim your prize money now", 1),
    ("Special offer ends today", 1),
    ("You won $1000 cash prize", 1),
    ("Buy now and save 99%", 1),
    ("Fastest weight loss guaranteed", 1),
    ("Your package has been delivered", 0),
    ("Thank you for your order", 0),
    ("Delivery scheduled for today", 0),
    ("Order confirmation: #12345", 0),
    ("Your subscription has been renewed", 0),
    ("Account statement for December", 0),
    ("Invoice attached for your review", 0),
    ("Welcome to our service", 0),
    ("Password reset request", 0),
    ("New message from support team", 0),
    ("EXCLUSIVE OFFER FOR YOU", 1),
    ("Limited slots available book now", 1),
    ("100% free download", 1),
    ("No credit card required", 1),
    ("Act now before offer expires", 1),
    ("Unbelievable deal", 1),
    ("Take this once in a lifetime opportunity", 1),
    ("Refinance your mortgage today", 1),
    ("Meeting notes from today", 0),
    ("Project deadline extended", 0),
    ("Team lunch tomorrow", 0),
    ("Performance review scheduled", 0),
]

def create_dataset():
    """Create a DataFrame from the spam dataset"""
    messages = [msg for msg, _ in SPAM_DATA]
    labels = [label for _, label in SPAM_DATA]
    return pd.DataFrame({'message': messages, 'label': labels})

def train_spam_detector():
    """Train and save the spam detection model"""
    
    # Print status
    print("=" * 50)
    print("SPAM DETECTION MODEL TRAINING")
    print("=" * 50)
    
    # Create dataset
    df = create_dataset()
    print(f"\n✓ Dataset created with {len(df)} samples")
    print(f"  - Spam messages: {sum(df['label'] == 1)}")
    print(f"  - Not Spam messages: {sum(df['label'] == 0)}")
    
    # Split data into training and testing sets (80-20 split)
    X = df['message']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n✓ Data split into training and testing sets")
    print(f"  - Training samples: {len(X_train)}")
    print(f"  - Testing samples: {len(X_test)}")
    
    # TF-IDF Vectorization: Convert text to numerical features
    print(f"\n✓ Converting text to TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=1000,  # Use top 1000 features
        stop_words='english',
        ngram_range=(1, 2)
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"  - Feature vector size: {X_train_vec.shape[1]} features")
    
    # Train Naive Bayes Classifier
    print(f"\n✓ Training Naive Bayes classifier...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    # Evaluate the model
    print(f"\n✓ Model Performance Metrics:")
    y_pred = model.predict(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"  - Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  - Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"  - Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"  - F1-Score:  {f1:.4f}")
    
    # Save model and vectorizer
    model_path = os.path.join(os.path.dirname(__file__), 'spam_model.pkl')
    vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"\n✓ Model saved successfully!")
    print(f"  - Model path: {model_path}")
    print(f"  - Vectorizer path: {vectorizer_path}")
    print("\n" + "=" * 50)
    print("Training completed!")
    print("=" * 50)

if __name__ == "__main__":
    train_spam_detector()
