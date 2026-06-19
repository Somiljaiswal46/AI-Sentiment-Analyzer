from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from datetime import datetime

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
model = joblib.load('best_sentiment_model_tuned.pkl')
vectorizer = joblib.load('best_tfidf_vectorizer.pkl')

# Preprocessing setup
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

def predict_sentiment(text):
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
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Sentiment Analysis API',
        'version': '1.0',
        'endpoints': {
            'POST /predict': 'Predict sentiment for a single text',
            'POST /predict-batch': 'Predict sentiment for multiple texts',
            'GET /health': 'Check API health',
            'GET /model-info': 'Get model information'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model': 'Sentiment Analysis Model v1.0'
    })

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
                result = predict_sentiment(text)
                results.append({
                    'text': text,
                    'sentiment': result['sentiment'],
                    'confidence': result['confidence'],
                    'probabilities': result['probabilities']
                })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        ],
        'training_data': {
            'total_samples': 14331,
            'training_set': 11464,
            'test_set': 2867,
            'domain': 'Twitter data about politics'
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
