from . import config
from .citation_graph import CitationGraph
from backend.models import Article

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    embeddings = config.load_data(config.EMBEDDINGS_PATH)
    knn = config.load_data(config.MODEL_PATH)

    def __init__(self, qid, qindex):
        self.query_id = qid
        self.query_index = qindex
        self.query_embeddings = np.array(self.embeddings[qindex]).reshape(1, -1)

    def calculate_similarity(self, query, data, n=config.N_SIMILAR, threshold=config.THRESHOLD):
        """
        Description :
        --------------
        Compute similarity between query embeddings and all dataframe articles vectors.

        Attribute :
        ------------
        - query : Vector of integers. Query embeddings
        - data : list of vectors. Data embeddings.
        - Threshold : percentage of required similarity.
        - n : Integer. Number of similar articles to be returned.
        """
        # compute similarity
        cosine = cosine_similarity(query, data)

        # dictionary contains each article with corresponding similarity with the query
        i = 0
        similarity = dict({})
        for value in cosine[0]:
            # check if article is similar threshold% with query
            if value >= threshold:
                similarity[i] = value
            i += 1

        # sort articles in descending order based on similarity to the query and return n articles
        similarity = {
            k: v
            for k, v in [
                (key, value)
                for key, value in sorted(
                    similarity.items(), key=lambda item: item[1], reverse=True
                )
            ][:n]
        }

        return similarity

    def get_similar_articles(self):
        """
        Description :
        --------------
        Return similar articles to article query.

        Output : List of integer. Articles' index
        """
        # create citation graph for query of 3 levels
        instance = CitationGraph()
        graph = instance.create_graph(self.query_id, [[self.query_id]], 0, config.GRAPH_LEVEL)
        graph_data = instance.get_graph_data(graph)

        # get similar articles
        if len(graph_data) <= config.N_SIMILAR:
            distance, index = self.knn.kneighbors(self.query_embeddings)
            return list(index[0])
        else:
            # get embeddings of graph nodes
            graph_embeddings = []
            for xid in graph_data:
                tmp = Article.query.filter_by(id=xid).first()
                graph_embeddings.append(self.embeddings[tmp.index])

            similarity = self.calculate_similarity(self.query_embeddings, graph_embeddings)
            return list(similarity.keys())