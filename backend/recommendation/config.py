''' Les paramètres de configuration globale d'algorithme de recommandation '''

import pickle

# Chemin d'accès aux fichiers
EMBEDDINGS_PATH = "backend/bin/glove_w2v_embeddings.pkl"
MODEL_PATH = "backend/bin/glove_knn_model.pkl"

# Constantes de réglage de l'algorithme
THRESHOLD = 0.4    # Pourcentage de similarité
N_SIMILAR = 10     # Nombre de recommandations à retourner
GRAPH_LEVEL = 3    # Le niveau de graphe de citations à construire

# Charger les données binaires
def load_data(path):
    """
    Description : Chargement des données à partir du chemin. 
    
    Attribut : 
    ------------
        - path : emplacement du fichier à charger.
    """

    with open(path, 'rb') as f:
        return pickle.load(f)
