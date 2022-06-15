''' Class de création de graphe de citations '''

from backend.models import Article


class CitationGraph: 
    def create_graph(self, xid, graph, index, max_level):
        """ 
        Description :
        --------------
        Créer un graphe de citaitons pour une requête à plusieurs niveaux.

        Paramètres :
        ------------
        - xid : identifiant de l'article de la requête.
        - graph : Nested list. Chaque sous-liste représente un niveau du graphe.
        - index : niveau actuel du graphe.
        - max_level : niveau maximum du graphe à créer.

        Sortie : Retourne une liste des articles.
        """

        # Si le niveau du graphe est supérieur au niveau maximal autorisé
        if len(graph) >= max_level:
            return graph

        # Obtenir l'identifiant des articles du niveau actuel (index)
        children = []
        for vertex in graph[index]:
            vertex_row = Article.query.filter_by(id=vertex).first()
            references = vertex_row.references

            if references is not None:
                for ref in references:
                    tmp = Article.query.filter_by(id=ref).first()
                    if (ref != xid
                        and not any(ref in subl for subl in graph)
                        and tmp is not None) :
                        children.append(ref)

        # Pas de données pour le niveau actuel du graphe
        if len(children) == 0:
            return graph
        else:
            graph.append(children)
            return self.create_graph(xid, graph, len(graph) - 1, max_level)


    def get_graph_data(self, graph):
        """
        Description :
        --------------
        Récupèrer les identifiants de tous les articles du graphe de citation.

        Paramètres :
        ------------
        - graph : Liste de listes d'objets. Chaque élément du graphe représente un niveau.

        Sortie : Retourner une liste des identifiants.
        """

        references = []

        # Exclue le niveau 0 puisqu'il représente la requête
        for subl in graph[1:]:
            for xid in subl:
                references.append(xid)

        return references
