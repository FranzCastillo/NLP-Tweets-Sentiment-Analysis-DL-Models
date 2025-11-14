import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import matplotlib.pyplot as plt


class BaselineModel:
    def __init__(self, input_dim, model_path='models/baseline.h5', checkpoint_path='models/checkpoint/best_baseline.h5'):
        """
        Initialize Baseline Model.

        Args:
            input_dim (int): Input dimension (number of features)
            model_path (str): Path to save the final model
            checkpoint_path (str): Path to save checkpoints
        """
        self.input_dim = input_dim
        self.model_path = model_path
        self.checkpoint_path = checkpoint_path
        self.model = None
        self.history = None

    def build(self):
        """Build the baseline model architecture."""
        self.model = keras.Sequential([
            layers.Input(shape=(self.input_dim,)),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])

        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        print("Baseline Model Architecture:")
        self.model.summary()
        return self.model

    def train(self, X_train, y_train, validation_split=0.2, epochs=20, batch_size=32):
        """
        Train the baseline model.

        Args:
            X_train: Training features
            y_train: Training labels
            validation_split (float): Validation split ratio
            epochs (int): Number of epochs
            batch_size (int): Batch size

        Returns:
            History object
        """
        if self.model is None:
            self.build()

        # Create checkpoint directory
        os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)

        # Define callbacks
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True,
            verbose=1
        )

        model_checkpoint = callbacks.ModelCheckpoint(
            self.checkpoint_path,
            save_best_only=True,
            monitor='val_loss',
            verbose=1
        )

        # Convert sparse matrix to dense array
        X_train_array = X_train.toarray() if hasattr(X_train, 'toarray') else X_train

        print("\nTraining Baseline Model...")
        self.history = self.model.fit(
            X_train_array, y_train,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, model_checkpoint],
            verbose=1
        )

        return self.history

    def save(self):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("Model not built. Call build() or train() first.")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"\nBaseline model saved to {self.model_path}")

    def load(self):
        """Load a saved model."""
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            print(f"Baseline model loaded from {self.model_path}")
            return self.model
        else:
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

    def predict(self, X):
        """
        Make predictions.

        Args:
            X: Input features

        Returns:
            Predictions
        """
        if self.model is None:
            raise ValueError("Model not built or loaded.")

        X_array = X.toarray() if hasattr(X, 'toarray') else X
        return self.model.predict(X_array)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model.

        Args:
            X_test: Test features
            y_test: Test labels

        Returns:
            tuple: (loss, accuracy)
        """
        if self.model is None:
            raise ValueError("Model not built or loaded.")

        X_test_array = X_test.toarray() if hasattr(X_test, 'toarray') else X_test
        loss, accuracy = self.model.evaluate(X_test_array, y_test, verbose=0)
        print(f"\nBaseline Model Evaluation:")
        print(f"Loss: {loss:.4f}")
        print(f"Accuracy: {accuracy:.4f}")

        return loss, accuracy


def plot_history(history, metrics=('loss', 'accuracy'), figsize=(12, 4)):
    """
    Plot training history.

    Args:
        history: Keras History object or dict
        metrics: Tuple of metrics to plot
        figsize: Figure size
    """
    if hasattr(history, 'history'):
        h = history.history
    elif isinstance(history, dict):
        h = history
    else:
        raise ValueError("`history` must be a Keras History object or a dict")

    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=figsize if n > 1 else (figsize[0] / 2, figsize[1]))
    if n == 1:
        axes = [axes]

    for ax, metric in zip(axes, metrics):
        train_key = metric
        val_key = f"val_{metric}"

        plotted = False
        if train_key in h:
            ax.plot(h[train_key], label=f"train_{metric}")
            plotted = True
        if val_key in h:
            ax.plot(h[val_key], label=f"val_{metric}")
            plotted = True

        if not plotted:
            ax.text(0.5, 0.5, f"No data for '{metric}'", ha='center', va='center')
        ax.set_xlabel('Epochs')
        ax.set_ylabel(metric.capitalize())
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.savefig('models/baseline_training_history.png')
    print("Training history plot saved to models/baseline_training_history.png")
    plt.close()

