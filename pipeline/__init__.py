"""
NLP Tweets Sentiment Analysis Pipeline
=======================================

A comprehensive pipeline for sentiment analysis using deep learning models.

Subpackages:
-----------
- data_preparation: Data extraction, preprocessing, and splitting
- modeling: Model definitions and vectorizers
- evaluation: Model evaluation utilities

"""

__version__ = "0.1.0"
__author__ = "Francisco Castillo"
__email__ = "cas21562@uvg.edu.gt"

# Import subpackages to make them available
from . import data_preparation
from . import modeling
from . import evaluation

__all__ = ['data_preparation', 'modeling', 'evaluation', '__version__']
