# Spam Detection System - Flask Backend Application
# This is the main Flask application that handles predictions and stores history

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import sqlite3
import os
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ml_model', 'spam_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'ml_model', 'vectorizer.pkl')
DB_PATH = os.path.join(BASE_DIR, 'database', 'spam_detection.db')

# Global variables to store model and vectorizer
model = None
vectorizer = None

def load_model():
    """Load the trained ML model and vectorizer"""
    global model, vectorizer
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        print("✓ Model and vectorizer loaded successfully!")
    except FileNotFoundError:
        print("✗ Model files not found! Please run train_model.py first.")
        return False
    return True

def initialize_database():
    """Initialize SQLite database for storing prediction history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                prediction INTEGER NOT NULL,
                confidence REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Database error: {str(e)}")

def save_prediction(message, prediction, confidence):
    """Save prediction to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (message, prediction, confidence)
            VALUES (?, ?, ?)
        ''', (message, prediction, confidence))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error saving prediction: {str(e)}")
        return False

def get_prediction_history(limit=10):
    """Retrieve prediction history from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, message, prediction, confidence, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'message': row[1],
                'prediction': 'Spam' if row[2] == 1 else 'Not Spam',
                'confidence': round(row[3] * 100, 2),
                'created_at': row[4]
            })
        
        return history
    except Exception as e:
        print(f"✗ Error retrieving history: {str(e)}")
        return []

def validate_input(text):
    """Validate user input"""
    if not text or len(text.strip()) == 0:
        return False, "Message cannot be empty!"
    
    if len(text) > 5000:
        return False, "Message is too long (max 5000 characters)"
    
    return True, "Valid"

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict if a message is spam or not
    Expected JSON: {"message": "text to check"}
    """
    try:
        # Get data from request
        data = request.get_json()
        message = data.get('message', '').strip()
        
        # Validate input
        is_valid, validation_msg = validate_input(message)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': validation_msg
            }), 400
        
        # Make prediction
        message_vec = vectorizer.transform([message])
        prediction = model.predict(message_vec)[0]
        
        # Get confidence score (probability of the predicted class)
        probabilities = model.predict_proba(message_vec)[0]
        confidence = max(probabilities)  # Maximum probability
        
        # Convert prediction to readable format
        result = 'Spam' if prediction == 1 else 'Not Spam'
        
        # Save to database
        save_prediction(message, prediction, confidence)
        
        return jsonify({
            'success': True,
            'message': message,
            'prediction': result,
            'confidence': round(confidence * 100, 2),
            'is_spam': bool(prediction)
        }), 200
        
    except Exception as e:
        print(f"✗ Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/api/history', methods=['GET'])
def history():
    """
    Get prediction history
    Query params: limit (default: 10)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Validate limit
        if limit < 1 or limit > 100:
            limit = 10
        
        history_data = get_prediction_history(limit)
        
        return jsonify({
            'success': True,
            'history': history_data,
            'count': len(history_data)
        }), 200
        
    except Exception as e:
        print(f"✗ History error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve history: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get statistics about predictions"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total = cursor.fetchone()[0]
        
        # Spam count
        cursor.execute('SELECT COUNT(*) FROM predictions WHERE prediction = 1')
        spam_count = cursor.fetchone()[0]
        
        # Not spam count
        not_spam_count = total - spam_count
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) FROM predictions')
        avg_confidence = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_predictions': total,
            'spam_count': spam_count,
            'not_spam_count': not_spam_count,
            'average_confidence': round(avg_confidence * 100, 2)
        }), 200
        
    except Exception as e:
        print(f"✗ Stats error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to get stats: {str(e)}'
        }), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear all prediction history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM predictions')
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'History cleared successfully'
        }), 200
        
    except Exception as e:
        print(f"✗ Clear history error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to clear history: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize application
    print("=" * 50)
    print("SPAM DETECTION SYSTEM - FLASK BACKEND")
    print("=" * 50)
    
    # Load model
    if not load_model():
        print("Exiting: Model loading failed!")
        exit(1)
    
    # Initialize database
    initialize_database()
    
    print("\n✓ Starting Flask server...")
    print("=" * 50)
    print("Server running at http://localhost:5000")
    print("=" * 50 + "\n")
    
    # Run the Flask app (debug=True for development, set to False for production)
    app.run(debug=True, host='localhost', port=5000)
