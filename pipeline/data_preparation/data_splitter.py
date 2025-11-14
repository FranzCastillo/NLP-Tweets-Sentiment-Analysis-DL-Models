import os
import pandas as pd
from sklearn.model_selection import train_test_split


class DataSplitter:
    def __init__(self, test_size=0.3, random_state=21562):
        """
        Initialize data splitter.

        Args:
            test_size (float): Proportion of test data
            random_state (int): Random seed for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.X_train_raw = None
        self.X_test_raw = None
        self.y_train = None
        self.y_test = None

    def split(self, X, y):
        """
        Split data into train and test sets.

        Args:
            X: Features (text data)
            y: Labels

        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        self.X_train_raw, self.X_test_raw, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state
        )

        print(f"Train size: {len(self.X_train_raw)}")
        print(f"Test size: {len(self.X_test_raw)}")

        return self.X_train_raw, self.X_test_raw, self.y_train, self.y_test

