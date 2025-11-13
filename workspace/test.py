import os
import re
import nltk
import spacy
import contractions
from unidecode import unidecode
from nltk.corpus import stopwords
import joblib
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Download required NLTK data
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except:
    print("SpaCy model not found. Please run: python -m spacy download en_core_web_sm")
    exit(1)

def preprocess_text(text, remove_stopwords=True):
    """Preprocess text using the same pipeline as training"""
    # Normalize encoding
    text = unidecode(text)

    # Lowercase
    text = text.lower()

    # Expand contractions
    text = contractions.fix(text)

    # Remove HTML tags and URLs
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove punctuation (keep ! and ? as they can carry sentiment)
    text = re.sub(r"[^a-zA-Z0-9!?']", " ", text)

    # Tokenize and Lemmatize using SpaCy
    doc = nlp(text)
    tokens = []
    for token in doc:
        lemma = token.lemma_.strip()
        if not lemma:
            continue
        if remove_stopwords and lemma in stop_words:
            continue
        tokens.append(lemma)

    # Remove extra whitespace and join back
    clean_text = " ".join(tokens)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return clean_text

def load_models():
    """Load all trained models and the vectorizer"""
    models = {}

    # Load TF-IDF vectorizer
    vectorizer_path = 'models/tfidf_vectorizer.joblib'
    if not os.path.exists(vectorizer_path):
        print(f"Error: Vectorizer not found at {vectorizer_path}")
        return None, None

    vectorizer = joblib.load(vectorizer_path)
    print(f"✓ Loaded TF-IDF vectorizer")

    # Define model paths
    model_paths = {
        'Baseline': 'models/baseline.h5',
        'Model 1': 'models/model1.h5',
        'Model 2': 'models/model2.h5',
        'Best Baseline': 'models/checkpoint/best_baseline.h5',
        'Best Model 1': 'models/checkpoint/best_model1.h5',
        'Best Model 2': 'models/checkpoint/best_model2.h5',
        'Best Model 3': 'models/checkpoint/best_model3.h5',
        'Model 3 (Final)': 'models/final/model3.h5',
    }

    # Load each model
    for name, path in model_paths.items():
        if os.path.exists(path):
            try:
                models[name] = keras.models.load_model(path)
                print(f"✓ Loaded {name}")
            except Exception as e:
                print(f"✗ Failed to load {name}: {e}")
        else:
            print(f"✗ Model not found: {name} at {path}")

    return vectorizer, models

def predict_sentiment(text, vectorizer, models):
    """Preprocess text and predict sentiment using all models"""
    # Preprocess
    processed_text = preprocess_text(text, remove_stopwords=True)

    # Vectorize
    vectorized = vectorizer.transform([processed_text])

    # Make predictions with all models
    predictions = {}
    for name, model in models.items():
        pred_prob = model.predict(vectorized.toarray(), verbose=0)[0][0]
        sentiment = "POSITIVE" if pred_prob >= 0.5 else "NEGATIVE"
        predictions[name] = {
            'probability': pred_prob,
            'sentiment': sentiment,
            'confidence': abs(pred_prob - 0.5) * 2  # 0 to 1 scale
        }

    return predictions, processed_text

def main():
    """Main function to read reviews and make predictions"""
    print("=" * 80)
    print("SENTIMENT ANALYSIS - MODEL PREDICTIONS")
    print("=" * 80)
    print()

    # Load models
    print("Loading models...")
    vectorizer, models = load_models()

    if vectorizer is None or not models:
        print("\nError: Could not load models. Please ensure models are trained first.")
        return

    print(f"\nSuccessfully loaded {len(models)} model(s)\n")
    print("=" * 80)

    # Read user reviews
    reviews_file = 'user_test_reviews.txt'
    if not os.path.exists(reviews_file):
        print(f"Error: {reviews_file} not found")
        return

    with open(reviews_file, 'r', encoding='utf-8') as f:
        reviews = [line.strip() for line in f if line.strip()]

    print(f"\nAnalyzing {len(reviews)} review(s)...\n")

    # Process each review
    for idx, review in enumerate(reviews, 1):
        print("=" * 80)
        print(f"REVIEW #{idx}")
        print("=" * 80)
        print(f"Original: {review}")

        # Get predictions
        predictions, processed = predict_sentiment(review, vectorizer, models)

        print(f"Preprocessed: {processed}")
        print()
        print("Model Predictions:")
        print("-" * 80)

        # Sort by model name for consistent display
        for model_name in sorted(predictions.keys()):
            pred = predictions[model_name]
            confidence_bar = "█" * int(pred['confidence'] * 20)
            print(f"{model_name:20s} | {pred['sentiment']:8s} | "
                  f"Prob: {pred['probability']:.4f} | "
                  f"Confidence: {confidence_bar} {pred['confidence']:.2%}")

        # Calculate consensus
        positive_count = sum(1 for p in predictions.values() if p['sentiment'] == 'POSITIVE')
        negative_count = len(predictions) - positive_count
        consensus = "POSITIVE" if positive_count > negative_count else "NEGATIVE"

        print("-" * 80)
        print(f"CONSENSUS: {consensus} ({positive_count} positive, {negative_count} negative)")
        print()

    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()

