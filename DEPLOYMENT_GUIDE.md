# 🚀 Sentiment Analysis Model - Deployment Guide

## Overview
This is a production-ready sentiment analysis model that classifies Twitter text into three categories: **Negative**, **Neutral**, and **Positive**.

**Model Performance:** 82.46% Accuracy

---

## 📁 Project Files

### Core Files
- `analysis.ipynb` - Complete model development and training notebook
- `best_sentiment_model_tuned.pkl` - Trained tuned model
- `best_tfidf_vectorizer.pkl` - TF-IDF vectorizer
- `Twitter_Data.csv` - Original dataset (14,331 samples)

### Deployment Files
- `streamlit_app.py` - Web interface using Streamlit
- `flask_api.py` - REST API using Flask
- `requirements.txt` - Python dependencies
- `README.md` - This file

---

## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Model Files
Ensure these files exist in the project directory:
```bash
ls -la best_sentiment_model_tuned.pkl
ls -la best_tfidf_vectorizer.pkl
```

---

## 🌐 Deployment Options

### Option 1: Streamlit Web App (Easy & Interactive)

#### Local Deployment
```bash
streamlit run streamlit_app.py
```

The app will open at: `http://localhost:8501`

#### Features:
- Single text analysis
- Batch analysis (multiple texts)
- Real-time probability visualization
- Model information dashboard
- Beautiful UI with Plotly charts

#### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Create new app and select your repository
5. Point to `streamlit_app.py`

---

### Option 2: Flask REST API

#### Local Deployment
```bash
python flask_api.py
```

The API will run at: `http://localhost:5000`


#### API Endpoints

##### 1. Health Check
```bash
curl http://localhost:5000/health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-10T10:30:00.123456",
  "model": "Sentiment Analysis Model v1.0"
}
```

##### 2. Predict Single Text
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this policy, it is amazing!"}'
```
Response:
```json
{
  "success": true,
  "input_text": "I love this policy, it is amazing!",
  "result": {
    "sentiment": "Positive",
    "confidence": 0.9998,
    "probabilities": {
      "Negative": 0.0001,
      "Neutral": 0.0001,
      "Positive": 0.9998
    }
  },
  "timestamp": "2026-04-10T10:30:00.123456"
}
```

##### 3. Batch Prediction
```bash
curl -X POST http://localhost:5000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "I love this!",
      "This is okay",
      "I hate this!"
    ]
  }'
```

##### 4. Model Information
```bash
curl http://localhost:5000/model-info
```

#### Deploy to Production

##### Using Gunicorn (Recommended for Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_api:app
```

##### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_api:app"]
```

Build and run:
```bash
docker build -t sentiment-api .
docker run -p 5000:5000 sentiment-api
```

##### Deploy to Cloud Platforms

**Heroku:**
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
```

**AWS EC2:**
1. Launch EC2 instance
2. Install Python and dependencies
3. Run: `gunicorn -w 4 -b 0.0.0.0:5000 flask_api:app`
4. Use load balancer for scaling

**Google Cloud Run:**
```bash
gcloud run deploy sentiment-api --source . --platform managed
```

**Azure App Service:**
```bash
az appservice plan create --name myplan --sku B1 --is-linux
az webapp create --plan myplan --name sentiment-app --runtime "PYTHON:3.9"
```

---

## 📊 Model Performance

### Accuracy: 82.46%

### Classification Metrics by Sentiment:

| Metric | Negative | Neutral | Positive |
|--------|----------|---------|----------|
| Precision | 0.85 | 0.76 | 0.88 |
| Recall | 0.68 | 0.96 | 0.79 |
| F1-Score | 0.76 | 0.85 | 0.84 |
| Support | 685 | 995 | 1,187 |

### Training Data
- **Total Samples:** 14,331 (after cleaning)
- **Training Set:** 11,464 (80%)
- **Test Set:** 2,867 (20%)
- **Categories:** Negative (-1), Neutral (0), Positive (1)
- **Domain:** Twitter data about politics

---

## 🔧 Model Architecture

### Algorithm
**Logistic Regression (Tuned)**

### Hyperparameters
- **C:** 1
- **Penalty:** L1
- **Solver:** SAGA
- **Max Iterations:** 1000

### Feature Engineering
- **Vectorization:** TF-IDF
- **Features:** 5,000
- **N-grams:** Unigrams and Bigrams (1-2)

### Preprocessing Pipeline
1. Lowercasing
2. Special character removal
3. Stopword removal (English)
4. Lemmatization
5. TF-IDF vectorization

---

## 🧪 Testing the Model

### Example Predictions

**Text:** "I love this new policy by Modi, it's amazing!"
- **Sentiment:** Positive
- **Confidence:** 99.98%

**Text:** "The government is doing nothing, very disappointed."
- **Sentiment:** Negative
- **Confidence:** 98.85%

**Text:** "Just another day in politics, nothing special."
- **Sentiment:** Positive
- **Confidence:** 90.97%

---

## 📝 Usage Examples

### Python (Direct)
```python
import joblib
from preprocessing import preprocess_text

model = joblib.load('best_sentiment_model_tuned.pkl')
vectorizer = joblib.load('best_tfidf_vectorizer.pkl')

text = "I love this!"
processed = preprocess_text(text)
vectorized = vectorizer.transform([processed])
prediction = model.predict(vectorized)[0]
print(f"Sentiment: {['Negative', 'Neutral', 'Positive'][prediction + 1]}")
```

### Using curl (Flask API)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Great product!"}'
```

### Using Python requests
```python
import requests

response = requests.post('http://localhost:5000/predict', 
    json={'text': 'Great product!'})
print(response.json())
```

---

## 🔒 Security Considerations

1. **Input Validation:** Both APIs validate input
2. **Error Handling:** Graceful error responses
3. **CORS:** Flask API configured with CORS for cross-origin requests
4. **Rate Limiting:** Implement for production
5. **Authentication:** Add API keys for production deployments

---

## 📈 Monitoring & Maintenance

### Metrics to Monitor
- Response time
- Prediction accuracy
- Error rate
- API uptime

### Model Updates
- Retrain quarterly with new data
- Monitor performance drift
- Update hyperparameters if needed
- Version control all models

---

## 🐛 Troubleshooting

### Issue: Model files not found
**Solution:** Ensure `.pkl` files are in the same directory as the app

### Issue: NLTK data missing
**Solution:** Run NLTK downloads (handled automatically in apps)

### Issue: Port already in use
**Solution:** Change port: `streamlit run streamlit_app.py --server.port 8502`

### Issue: Out of memory
**Solution:** Increase server RAM or reduce batch size

---

## 📞 Support & Contact

For issues or improvements, please refer to the project documentation or contact the development team.

---

## 📄 License

This project is for educational and commercial use.

---

**Last Updated:** April 10, 2026
**Model Version:** 1.0
**Status:** Production Ready ✅
