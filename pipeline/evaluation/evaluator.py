import numpy as np
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def evaluate_model(model, X, y, threshold=0.5, average='binary', return_report=False):
    """
    Evaluate a model with comprehensive metrics.

    Args:
        model: Trained model (Keras or sklearn)
        X: Test features
        y: Test labels
        threshold (float): Classification threshold
        average (str): Averaging method for metrics
        return_report (bool): Whether to include classification report

    Returns:
        dict: Dictionary containing evaluation metrics
    """
    if hasattr(X, "toarray"):
        X_eval = X.toarray()
    else:
        X_eval = np.asarray(X)

    y_true = np.asarray(y)

    y_pred = None
    y_prob = None

    try:
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_eval)
            if y_prob.ndim == 2 and y_prob.shape[1] > 1:
                y_prob_pos = y_prob[:, 1]
            else:
                y_prob_pos = y_prob.ravel()
            y_pred = (y_prob_pos >= threshold).astype(int)
            y_prob = y_prob_pos
        else:
            raw = model.predict(X_eval)
            raw = np.asarray(raw)
            if raw.dtype.kind in ("f",) and raw.ndim >= 1:
                if raw.ndim > 1 and raw.shape[1] == 1:
                    probs = raw.ravel()
                    y_prob = probs
                    y_pred = (probs >= threshold).astype(int)
                elif raw.ndim > 1 and raw.shape[1] > 1:
                    classes = np.argmax(raw, axis=1)
                    y_pred = classes
                    if raw.shape[1] == 2:
                        y_prob = raw[:, 1]
                else:
                    probs = raw.ravel()
                    y_prob = probs
                    y_pred = (probs >= threshold).astype(int)
            else:
                y_pred = raw.ravel().astype(int)
    except Exception:
        y_pred = model.predict(X_eval)
        y_pred = np.asarray(y_pred).ravel().astype(int)

    if y_pred is None:
        raise RuntimeError("Could not obtain predictions from the model.")

    results = {}
    try:
        results["precision"] = float(precision_score(y_true, y_pred, average=average, zero_division=0))
        results["recall"] = float(recall_score(y_true, y_pred, average=average, zero_division=0))
        results["f1"] = float(f1_score(y_true, y_pred, average=average, zero_division=0))
    except Exception:
        results["precision"] = None
        results["recall"] = None
        results["f1"] = None

    results["accuracy"] = float(accuracy_score(y_true, y_pred))
    auc_val = None
    if y_prob is not None:
        try:
            if len(np.unique(y_true)) == 2:
                auc_val = float(roc_auc_score(y_true, y_prob))
        except Exception:
            auc_val = None
    results["auc"] = auc_val

    try:
        results["confusion_matrix"] = confusion_matrix(y_true, y_pred).tolist()
    except Exception:
        results["confusion_matrix"] = None

    if return_report:
        try:
            results["report"] = classification_report(y_true, y_pred, zero_division=0)
        except Exception:
            results["report"] = None

    return results


def print_evaluation_results(results, model_name="Model"):
    """
    Pretty print evaluation results.

    Args:
        results (dict): Results from evaluate_model
        model_name (str): Name of the model
    """
    print(f"\n{'=' * 60}")
    print(f"{model_name} Evaluation Results")
    print(f"{'=' * 60}")

    if results.get("accuracy") is not None:
        print(f"Accuracy:  {results['accuracy']:.4f}")
    if results.get("precision") is not None:
        print(f"Precision: {results['precision']:.4f}")
    if results.get("recall") is not None:
        print(f"Recall:    {results['recall']:.4f}")
    if results.get("f1") is not None:
        print(f"F1 Score:  {results['f1']:.4f}")
    if results.get("auc") is not None:
        print(f"AUC:       {results['auc']:.4f}")

    if results.get("confusion_matrix") is not None:
        print(f"\nConfusion Matrix:")
        cm = results["confusion_matrix"]
        print(f"  TN: {cm[0][0]}  FP: {cm[0][1]}")
        print(f"  FN: {cm[1][0]}  TP: {cm[1][1]}")

    if results.get("report") is not None:
        print(f"\nClassification Report:")
        print(results["report"])

    print(f"{'=' * 60}\n")

