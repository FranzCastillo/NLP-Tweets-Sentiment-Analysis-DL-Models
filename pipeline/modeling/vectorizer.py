import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfVectorizerWrapper:
    def __init__(self, max_features=5000, vectorizer_path='models/tfidf_vectorizer.joblib'):
        """
        Initialize TF-IDF Vectorizer wrapper.

        Args:
            max_features (int): Maximum number of features for TF-IDF
            vectorizer_path (str): Path to save/load the vectorizer
        """
        self.max_features = max_features
        self.vectorizer_path = vectorizer_path
        self.vectorizer = None
        self.X_train = None
        self.X_test = None

    def fit_transform(self, X_train_raw, X_test_raw):
        """
        Fit and transform training data, transform test data.

        Args:
            X_train_raw: Raw training text data
            X_test_raw: Raw test text data

        Returns:
            tuple: (X_train_tfidf, X_test_tfidf)
        """
        if os.path.exists(self.vectorizer_path):
            self.vectorizer = joblib.load(self.vectorizer_path)
            self.X_train = self.vectorizer.transform(X_train_raw)
            self.X_test = self.vectorizer.transform(X_test_raw)
            print(f"TF-IDF Vectorizer loaded from {self.vectorizer_path}")
        else:
            self.vectorizer = TfidfVectorizer(max_features=self.max_features)
            self.X_train = self.vectorizer.fit_transform(X_train_raw)
            self.X_test = self.vectorizer.transform(X_test_raw)

            # Save vectorizer
            os.makedirs(os.path.dirname(self.vectorizer_path), exist_ok=True)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            print(f"TF-IDF Vectorizer saved to {self.vectorizer_path}")

        print(f"Train shape: {self.X_train.shape}, Test shape: {self.X_test.shape}")
        return self.X_train, self.X_test

    def transform(self, X_raw):
        """
        Transform new data using the fitted vectorizer.

        Args:
            X_raw: Raw text data to transform

        Returns:
            Transformed data
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit_transform first.")
        return self.vectorizer.transform(X_raw)

