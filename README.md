<div align="center">
  <h1>✨ SentimentAI - Pro Text Intelligence</h1>
  <p>A premium, SaaS-level machine learning web application that performs real-time sentiment analysis with calibrated confidence scores.</p>

  [![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-Serverless-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)](https://scikit-learn.org/)
  [![Deployed on Vercel](https://img.shields.io/badge/Deployed_on-Vercel-black.svg)](https://vercel.com/)
</div>

<br />

## 🚀 Live Demo
**👉 [Experience the live application here](https://ai-sentiment-analyzer.vercel.app/)** *(Vercel par deploy hone ke baad apna asli link yahan daal dein)*

## 📸 Preview
*(Is folder mein apne app ki ek screenshot save karein jiska naam `preview.png` ho, wo yahan automatic show hogi)*

![App Preview](preview.png)

---

## 💡 About The Project
SentimentAI is an end-to-end Machine Learning web application designed to instantly decode the emotional tone of text. Moving beyond simple positive/negative labels, this model uses a **Calibrated Linear Support Vector Machine (LinearSVC)** with balanced class weights to accurately detect nuanced Neutral statements alongside high-confidence Positive and Negative sentiment probabilities.

The frontend has been meticulously crafted to mimic a modern SaaS interface, featuring glassmorphism, fluid animations, and real-time processing capabilities powered by Vercel Serverless Functions.

## 🌟 Key Features
- **Real-Time Inference:** Toggle the "Real-time" switch to get live sentiment analysis as you type (debounced for optimized API calls).
- **Calibrated Confidence:** See the exact probability distribution across Positive, Neutral, and Negative sentiments via animated progress bars.
- **Premium UI/UX:** Complete with Dark/Light mode toggles, glassmorphic panels, animated gradient backgrounds, and responsive grids.
- **Visual Keyword Highlighting:** Text input is parsed to visually highlight context keywords.
- **Data Persistence & Export:** Your prediction history is securely stored in your browser's LocalStorage. You can export your session history to a CSV file at any time.
- **Serverless Architecture:** The Python backend is optimized to run as a serverless function on Vercel, ensuring zero cold-start bottlenecks.

---

## 🛠️ Tech Stack
**Frontend:**
- Semantic HTML5
- Vanilla CSS3 (CSS Variables, Flexbox, CSS Grid, Keyframe Animations, Backdrop Filters)
- Vanilla JavaScript (Async/Await, LocalStorage, Clipboard API)

**Backend / Machine Learning:**
- Python 3
- Flask & Flask-CORS (API Routing)
- Scikit-Learn (TF-IDF Vectorization, LinearSVC, CalibratedClassifierCV)
- NLTK (Text Lemmatization, Stopword removal)
- Pandas & NumPy (Data Processing)

---

## 💻 Local Setup & Installation

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Somiljaiswal46/AI-Sentiment-Analyzer.git
   cd AI-Sentiment-Analyzer
