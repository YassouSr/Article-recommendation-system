"""
This file contains necessary information for recommendation algorithm.
"""

import pickle

# Files path
EMBEDDINGS_PATH = "backend/bin/word2vec_embeddings.pkl"
MODEL_PATH = "backend/bin/knn_model.pkl"

# Algorithm tuning constants
THRESHOLD = 0.5
N_SIMILAR = 16
GRAPH_LEVEL = 3

# Load binary data
def load_data(path):
    """
    Description : Load data from path. 
    
    Attribute : 
    ------------
        - path : String. Location to file to be loaded.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)
