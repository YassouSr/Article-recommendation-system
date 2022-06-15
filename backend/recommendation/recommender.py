''' Algorithme de recommandations des articles selon la requete d'utilisateur '''

from . import config
from .citation_graph import CitationGraph
from backend.models import Article
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    # Embeddings de tous les articles de BD 
    embeddings = config.load_data(config.EMBEDDINGS_PATH)
    knn = config.load_data(config.MODEL_PATH)

    def __init__(self, qid):
        self.query_id = qid
        self.query_embeddings = np.array(self.embeddings[qid]).reshape(1, -1)


    def calculate_similarity(self, xid, query, data, n=config.N_SIMILAR, threshold=config.THRESHOLD):
        """
        Description :
        --------------
        Calcule la similarité entre les incorporations de la requête et tous les vecteurs d'articles du cadre de données.

        Paramètres :
        ------------
        - xid : id d'article
        - query : vecteur d'incorporations de requête
        - data : dictionnaire de vecteurs et ses ids à comparer avec query.
        - Threshold : pourcentage de similarité requis.
        - n : nombre d'articles similaires à retourner.
        """
        data_xid = list(data.keys())
        data_values = list(data.values())

        # Calculer la similarité
        cosine = cosine_similarity(query, data_values)

        # Dictionnaire contient chaque article avec la similarité correspondante avec la requête
        similarity = dict({})
        for i, value in enumerate(cosine[0]):
            if value >= threshold:
                similarity[data_xid[i]] = value
        
        if xid in similarity:
            similarity.pop(xid)

        # Trier les articles par ordre décroissant en fonction de leur similarité avec la requête et retourner n articles
        similarity = [k for k, v in [(key, value) for key, value in sorted(similarity.items(), key=lambda item: item[1], reverse=True)][:n]]

        return similarity


    def get_similar_articles(self):
        """
        Description :
        --------------
        Retourne les articles similaires à la requête de l'article.

        Sortie : Liste d'entiers. Index des articles
        """

        # Créer un graphe de citations pour une requête de 3 niveaux
        instance = CitationGraph()
        graph = instance.create_graph(self.query_id, [[self.query_id]], 0, config.GRAPH_LEVEL)
        graph_data = instance.get_graph_data(graph)

        # Retourner les articles similaires
        if len(graph_data) <= config.N_SIMILAR:
            _, index = self.knn.kneighbors(self.query_embeddings)
            index = list(index[0])

            if self.query_id in index:
                index.remove(self.query_id)

            return index
        else:
            # Obtenir les vecteurs des voisins de requete 
            data = {xid:self.embeddings[xid] for xid in graph_data}
            index = self.calculate_similarity(self.query_id, self.query_embeddings, data)
            
            return index
