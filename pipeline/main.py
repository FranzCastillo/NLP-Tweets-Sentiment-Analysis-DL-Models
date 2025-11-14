import os
import pandas as pd
from data_preparation import DataExtractor, TextPreprocessor


def main():
    """
    Main pipeline for data extraction and preprocessing.
    Replicates the data preparation from app.ipynb using modular code.
    """
    # Define paths - works for both Docker and local execution
    # Docker will use /app/data (mounted volume)
    # Local execution will use ../data
    DATA_DIR = os.getenv('DATA_DIR', '/app/data' if os.path.exists('/app') else '../data')
    PATH_RAW_DATA = os.path.join(DATA_DIR, 'raw.csv')
    PATH_PROCESSED_DATA = os.path.join(DATA_DIR, 'processed.csv')

    # Step 1: Extract IMDB data
    print("=" * 60)
    print("STEP 1: Data Extraction")
    print("=" * 60)

    if not os.path.exists(PATH_RAW_DATA):
        print("Extracting IMDB dataset...")
        os.makedirs(DATA_DIR, exist_ok=True)

        extractor = DataExtractor(split="train")
        df = extractor.extract()
        extractor.save(PATH_RAW_DATA)
        print(f"Raw Data saved to {PATH_RAW_DATA}")
    else:
        df = pd.read_csv(PATH_RAW_DATA)
        print(f"Raw Data loaded from {PATH_RAW_DATA}")

    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head())

    # Step 2: Preprocess the data
    print("\n" + "=" * 60)
    print("STEP 2: Data Preprocessing")
    print("=" * 60)

    preprocessor = TextPreprocessor(remove_stopwords=True)

    if not os.path.exists(PATH_PROCESSED_DATA):
        print("Preprocessing text data with memory-optimized chunking...")

        # Process the dataframe with smaller chunks for Docker memory constraints
        df_processed = preprocessor.preprocess_dataframe(
            df,
            text_column='text',
            batch_size=500,  # Reduced batch size
            chunk_size=5000  # Process 5000 rows at a time
        )
        df_processed.to_csv(PATH_PROCESSED_DATA, index=False)
        print(f"Processed Data saved to {PATH_PROCESSED_DATA}")
    else:
        df_processed = pd.read_csv(PATH_PROCESSED_DATA)
        print(f"Processed Data loaded from {PATH_PROCESSED_DATA}")

    # Show sample of preprocessing results
    print("\n" + "=" * 60)
    print("Sample Preprocessing Results")
    print("=" * 60)

    # Load original data for comparison
    df_original = pd.read_csv(PATH_RAW_DATA)

    for i in range(min(3, len(df_processed))):
        print(f"\nExample {i+1}:")
        print(f"Original: {df_original.loc[i, 'text'][:200]}...")
        print(f"Processed: {df_processed.loc[i, 'text'][:200]}...")

    print("\n" + "=" * 60)
    print("Data Preparation Complete!")
    print("=" * 60)
    print(f"Raw data: {PATH_RAW_DATA}")
    print(f"Processed data: {PATH_PROCESSED_DATA}")
    print(f"Total samples: {len(df_processed)}")

    return df_processed


if __name__ == "__main__":
    main()
