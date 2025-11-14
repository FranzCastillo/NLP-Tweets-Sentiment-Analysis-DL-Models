import pandas as pd
from datasets import load_dataset


class DataExtractor:
    def __init__(self, split="train"):
        self.split = split
        self.dataset = None
        self.df = None

    def extract(self):
        """Load the IMDB dataset."""
        self.dataset = load_dataset("imdb", split=self.split)
        self.df = pd.DataFrame(self.dataset)
        return self.df

    def save(self, output_path):
        """Save the dataset to CSV."""
        if self.df is None:
            raise ValueError("No data to save. Call extract() first.")
        self.df.to_csv(output_path, index=False)
