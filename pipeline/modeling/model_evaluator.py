import os
from .evaluator import evaluate_model, print_evaluation_results
from .baseline import plot_history


class ModelEvaluator:
    def __init__(self, model, model_name="Model", models_dir='models'):
        """
        Initialize model evaluator.

        Args:
            model: Trained model instance
            model_name (str): Name of the model
            models_dir (str): Directory to save plots
        """
        self.model = model
        self.model_name = model_name
        self.models_dir = models_dir
        self.results = None
        self.history = None

    def set_history(self, history):
        """
        Set training history for plotting.

        Args:
            history: Keras History object
        """
        self.history = history

    def plot_training_history(self, metrics=('loss', 'accuracy'), figsize=(12, 4)):
        """
        Plot training history.

        Args:
            metrics: Tuple of metrics to plot
            figsize: Figure size
        """
        if self.history is None:
            print("No training history available to plot.")
            return

        plot_history(self.history, metrics=metrics, figsize=figsize)
        print(f"Training history plot saved to {self.models_dir}/")

    def evaluate_on_test(self, X_test, y_test, threshold=0.5, return_report=True):
        """
        Evaluate model on test data.

        Args:
            X_test: Test features
            y_test: Test labels
            threshold (float): Classification threshold
            return_report (bool): Whether to include classification report

        Returns:
            dict: Evaluation results
        """
        print(f"\n{'=' * 60}")
        print(f"Evaluating {self.model_name}")
        print(f"{'=' * 60}")

        # Use the model's evaluate method if available
        if hasattr(self.model, 'evaluate'):
            self.model.evaluate(X_test, y_test)

        # Get comprehensive metrics
        self.results = evaluate_model(
            self.model.model if hasattr(self.model, 'model') else self.model,
            X_test,
            y_test,
            threshold=threshold,
            return_report=return_report
        )

        # Print results
        print_evaluation_results(self.results, model_name=self.model_name)

        return self.results

    def get_metrics_summary(self):
        """
        Get a summary of key metrics.

        Returns:
            dict: Summary of metrics
        """
        if self.results is None:
            raise ValueError("No evaluation results available. Call evaluate_on_test first.")

        summary = {
            'model': self.model_name,
            'accuracy': self.results.get('accuracy'),
            'precision': self.results.get('precision'),
            'recall': self.results.get('recall'),
            'f1': self.results.get('f1'),
            'auc': self.results.get('auc')
        }

        return summary

    def save_results(self, filepath=None):
        """
        Save evaluation results to a file.

        Args:
            filepath (str): Path to save results
        """
        if self.results is None:
            raise ValueError("No evaluation results available. Call evaluate_on_test first.")

        if filepath is None:
            os.makedirs(self.models_dir, exist_ok=True)
            filepath = os.path.join(self.models_dir, f"{self.model_name.lower().replace(' ', '_')}_results.txt")

        with open(filepath, 'w') as f:
            f.write(f"Evaluation Results for {self.model_name}\n")
            f.write("=" * 60 + "\n\n")

            if self.results.get('accuracy') is not None:
                f.write(f"Accuracy:  {self.results['accuracy']:.4f}\n")
            if self.results.get('precision') is not None:
                f.write(f"Precision: {self.results['precision']:.4f}\n")
            if self.results.get('recall') is not None:
                f.write(f"Recall:    {self.results['recall']:.4f}\n")
            if self.results.get('f1') is not None:
                f.write(f"F1 Score:  {self.results['f1']:.4f}\n")
            if self.results.get('auc') is not None:
                f.write(f"AUC:       {self.results['auc']:.4f}\n")

            if self.results.get('confusion_matrix') is not None:
                cm = self.results['confusion_matrix']
                f.write(f"\nConfusion Matrix:\n")
                f.write(f"  TN: {cm[0][0]}  FP: {cm[0][1]}\n")
                f.write(f"  FN: {cm[1][0]}  TP: {cm[1][1]}\n")

            if self.results.get('report') is not None:
                f.write(f"\nClassification Report:\n")
                f.write(self.results['report'])

        print(f"Results saved to {filepath}")

