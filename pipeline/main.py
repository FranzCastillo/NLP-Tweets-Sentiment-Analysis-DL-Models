import os
import pandas as pd
from data_preparation import DataExtractor, TextPreprocessor, DataSplitter
from modeling import BaselineModel, TfidfVectorizerWrapper
from evaluation import ModelEvaluator


def main():
    """
    Main pipeline for data extraction, preprocessing, and model training.
    Replicates the data preparation and baseline model from app.ipynb using modular code.
    """
    # Define paths - works for both Docker and local execution
    # Docker will use /app/data (mounted volume)
    # Local execution will use ../data
    DATA_DIR = os.getenv('DATA_DIR', '/app/data' if os.path.exists('/app') else '../data')
    MODELS_DIR = os.getenv('MODELS_DIR', '/app/models' if os.path.exists('/app') else '../workspace/models')

    PATH_RAW_DATA = os.path.join(DATA_DIR, 'raw.csv')
    PATH_PROCESSED_DATA = os.path.join(DATA_DIR, 'processed.csv')
    VECTORIZER_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib')
    BASELINE_MODEL_PATH = os.path.join(MODELS_DIR, 'baseline.h5')
    BASELINE_CHECKPOINT_PATH = os.path.join(MODELS_DIR, 'checkpoint', 'best_baseline.h5')

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

    df_original = pd.read_csv(PATH_RAW_DATA)
    for i in range(min(3, len(df_processed))):
        print(f"\nExample {i+1}:")
        print(f"Original: {df_original.loc[i, 'text'][:150]}...")
        print(f"Processed: {df_processed.loc[i, 'text'][:150]}...")

    # Step 3: Train/Test Split
    print("\n" + "=" * 60)
    print("STEP 3: Train/Test Split")
    print("=" * 60)

    splitter = DataSplitter(test_size=0.3, random_state=21562)
    X_train_raw, X_test_raw, y_train, y_test = splitter.split(
        df_processed['text'],
        df_processed['label']
    )

    # Step 4: TF-IDF Vectorization
    print("\n" + "=" * 60)
    print("STEP 4: TF-IDF Vectorization")
    print("=" * 60)

    tfidf = TfidfVectorizerWrapper(max_features=5000, vectorizer_path=VECTORIZER_PATH)
    X_train, X_test = tfidf.fit_transform(X_train_raw, X_test_raw)

    # Step 5: Build and Train Baseline Model
    print("\n" + "=" * 60)
    print("STEP 5: Baseline Model Training")
    print("=" * 60)

    baseline = BaselineModel(
        input_dim=X_train.shape[1],
        model_path=BASELINE_MODEL_PATH,
        checkpoint_path=BASELINE_CHECKPOINT_PATH
    )

    # Build the model
    baseline.build()

    # Train the model
    history = baseline.train(
        X_train,
        y_train,
        validation_split=0.2,
        epochs=20,
        batch_size=32
    )

    # Save the model
    baseline.save()

    # Step 6: Model Evaluation
    print("\n" + "=" * 60)
    print("STEP 6: Model Evaluation")
    print("=" * 60)

    # Create evaluator instance from the evaluation package
    evaluator = ModelEvaluator(
        model=baseline,
        model_name="Baseline Model",
        models_dir=MODELS_DIR
    )

    # Set training history and plot
    evaluator.set_history(history)
    evaluator.plot_training_history(metrics=('loss', 'accuracy'))

    # Evaluate on test set
    results = evaluator.evaluate_on_test(X_test, y_test, return_report=True)

    # Save evaluation results
    evaluator.save_results()

    # Get metrics summary
    summary = evaluator.get_metrics_summary()

    # Final Summary
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print(f"Raw data: {PATH_RAW_DATA}")
    print(f"Processed data: {PATH_PROCESSED_DATA}")
    print(f"Vectorizer: {VECTORIZER_PATH}")
    print(f"Baseline model: {BASELINE_MODEL_PATH}")
    print(f"Baseline checkpoint: {BASELINE_CHECKPOINT_PATH}")
    print(f"Total samples: {len(df_processed)}")
    print(f"Training samples: {len(X_train_raw)}")
    print(f"Test samples: {len(X_test_raw)}")
    print(f"\nMetrics Summary:")
    for key, value in summary.items():
        if key != 'model' and value is not None:
            print(f"  {key.capitalize()}: {value:.4f}")

    return baseline, tfidf, evaluator


if __name__ == "__main__":
    main()
