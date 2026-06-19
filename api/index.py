import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from datetime import datetime

# Define base path to ensure relative paths work on Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Download NLTK data to a writable temporary directory in Vercel
nltk.data.path.append('/tmp')
nltk.download('stopwords', download_dir='/tmp', quiet=True)
nltk.download('wordnet', download_dir='/tmp', quiet=True)

app = Flask(__name__)
CORS(app)

# Load model and vectorizer using absolute paths
model_path = os.path.join(BASE_DIR, 'best_sentiment_model_tuned.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'best_tfidf_vectorizer.pkl')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None

# Preprocessing setup
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    stop_words = set()
    lemmatizer = None

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    if lemmatizer and stop_words:
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

def predict_sentiment(text):
    if not model or not vectorizer:
        raise Exception("Model not loaded properly")
        
    processed = preprocess_text(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    
    labels = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
    
    return {
        'sentiment': labels[prediction],
        'confidence': float(max(probability)),
        'probabilities': {
            'Negative': float(probability[0]),
            'Neutral': float(probability[1]),
            'Positive': float(probability[2])
        }
    }

# Routes
@app.route('/<path:path>')
def send_static(path):
    if os.path.exists(os.path.join(BASE_DIR, path)):
        return send_from_directory(BASE_DIR, path)
    return jsonify({"error": "Not found"}), 404

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api', methods=['GET'])
def home():
    return jsonify({
        'message': 'Sentiment Analysis API',
        'version': '1.0',
        'endpoints': {
            'POST /api/predict': 'Predict sentiment for a single text',
            'POST /api/predict-batch': 'Predict sentiment for multiple texts',
            'GET /api/health': 'Check API health',
            'GET /api/model-info': 'Get model information'
        }
    })

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy' if model else 'model_missing',
        'timestamp': datetime.now().isoformat(),
        'model': 'Sentiment Analysis Model v1.0'
    })

@app.route('/api/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'Text must be a non-empty string'}), 400
        
        result = predict_sentiment(text)
        
        return jsonify({
            'success': True,
            'input_text': text,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict-batch', methods=['POST'])
@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'Missing "texts" field'}), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({'error': '"texts" must be a list'}), 400
        
        if len(texts) == 0:
            return jsonify({'error': 'Texts list cannot be empty'}), 400
        
        results = []
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                results.append({
                    'text': text,
                    'error': 'Invalid text'
                })
            else:
                try:
                    result = predict_sentiment(text)
                    results.append({
                        'text': text,
                        'sentiment': result['sentiment'],
                        'confidence': result['confidence'],
                        'probabilities': result['probabilities']
                    })
                except Exception as e:
                     results.append({
                        'text': text,
                        'error': str(e)
                    })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
@app.route('/model-info', methods=['GET'])
def model_info():
    return jsonify({
        'model_name': 'Sentiment Analysis Model',
        'version': '1.0',
        'algorithm': 'Logistic Regression (Tuned)',
        'accuracy': 0.8246,
        'parameters': {
            'C': 1,
            'penalty': 'l1',
            'solver': 'saga'
        },
        'performance_metrics': {
            'negative': {'precision': 0.85, 'recall': 0.68, 'f1-score': 0.76},
            'neutral': {'precision': 0.76, 'recall': 0.96, 'f1-score': 0.85},
            'positive': {'precision': 0.88, 'recall': 0.79, 'f1-score': 0.84}
        },
        'categories': ['Negative', 'Neutral', 'Positive'],
        'preprocessing': [
            'Lowercasing',
            'Special character removal',
            'Stopword removal',
            'Lemmatization',
            'TF-IDF vectorization (5000 features, unigrams + bigrams)'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Vercel needs the application instance named 'app' exported
# which is done automatically since 'app' is at the top level

if __name__ == '__main__':
    print("Starting local development server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
