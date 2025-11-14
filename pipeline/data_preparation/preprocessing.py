import os
import re
import pandas as pd
import nltk
import spacy
import contractions
from unidecode import unidecode
from nltk.corpus import stopwords
from tqdm import tqdm
import gc


class TextPreprocessor:
    def __init__(self, remove_stopwords=True):
        """
        Initialize the text preprocessor.

        Args:
            remove_stopwords (bool): Whether to remove stopwords during preprocessing
        """
        self.remove_stopwords = remove_stopwords

        # Download and load resources
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

        # Optimize spacy for memory
        self.nlp.max_length = 2000000  # Reduce max length if needed

    def preprocess_text(self, text):
        """
        Preprocess a single text string.

        Args:
            text (str): Input text to preprocess

        Returns:
            str: Cleaned and preprocessed text
        """
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
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            lemma = token.lemma_.strip()
            if not lemma:
                continue
            if self.remove_stopwords and lemma in self.stop_words:
                continue
            tokens.append(lemma)

        # Remove extra whitespace and join back
        clean_text = " ".join(tokens)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        clean_text = re.sub(r"[!?]{2,}", lambda m: m.group(0)[0], clean_text)

        return clean_text

    def preprocess_dataframe(self, df, text_column='text', batch_size=500, chunk_size=5000):
        """
        Preprocess all texts in a DataFrame using batch processing with chunking for memory efficiency.

        Args:
            df (pd.DataFrame): Input DataFrame
            text_column (str): Name of the column containing text
            batch_size (int): Batch size for SpaCy processing (reduced from 1000 to 500)
            chunk_size (int): Process data in chunks to reduce memory usage

        Returns:
            pd.DataFrame: DataFrame with preprocessed text
        """
        texts = df[text_column].tolist()
        processed_texts = []

        # Process in chunks to reduce memory usage
        total_chunks = (len(texts) + chunk_size - 1) // chunk_size

        for chunk_idx in range(total_chunks):
            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, len(texts))
            chunk_texts = texts[start_idx:end_idx]

            print(f"Processing chunk {chunk_idx + 1}/{total_chunks} ({start_idx} to {end_idx})")

            for doc in tqdm(self.nlp.pipe(chunk_texts, batch_size=batch_size),
                          total=len(chunk_texts),
                          desc=f"Chunk {chunk_idx + 1}/{total_chunks}"):
                tokens = [token.lemma_ for token in doc
                         if token.lemma_ and (not self.remove_stopwords or token.lemma_ not in self.stop_words)]
                clean_text = " ".join(tokens)
                processed_texts.append(clean_text)

            # Force garbage collection after each chunk
            gc.collect()

        df[text_column] = processed_texts
        return df

    def process_and_save(self, input_path, output_path, text_column='text', chunk_size=5000):
        """
        Load, preprocess, and save a dataset with chunked processing.

        Args:
            input_path (str): Path to input CSV file
            output_path (str): Path to save processed CSV file
            text_column (str): Name of the column containing text
            chunk_size (int): Size of chunks for processing

        Returns:
            pd.DataFrame: Preprocessed DataFrame
        """
        if os.path.exists(output_path):
            print(f"Processed data loaded from {output_path}")
            return pd.read_csv(output_path)

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Load and process data
        print(f"Loading data from {input_path}")
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} rows")

        df = self.preprocess_dataframe(df, text_column=text_column, chunk_size=chunk_size)

        # Save processed data
        df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")

        return df

