from backend.models import Article

class CitationGraph: 
    def create_graph(self, xid, graph, index, max_level):
        """
        Description :
        --------------
        Create graph of references for a query with multiple level.

        Attribute :
        ------------
        - xid : query article id.
        - graph : Iterable of lists. Each sub-list represent a graph level.
        - data : pandas dataframe.
        - index : current graph level.
        - max_level : maximul level of graph to create.

        Output : Return list of list of articles' id.
        """
        # level of graph reached the maximim level allowed
        if len(graph) >= max_level:
            return graph

        # get articles' id of current level (index)
        children = []
        for vertex in graph[index]:
            # vertex_row = data.filter("id == '%s'" % vertex).select("references").collect()
            vertex_row = Article.query.filter_by(id=vertex).first()
            references = vertex_row.references

            if references is not None:
                for ref in references:
                    # tmp = data.filter("id == '%s'" % ref).collect()
                    tmp = Article.query.filter_by(id=ref).first()
                    if (
                        ref != xid
                        and not any(ref in subl for subl in graph)
                        and tmp is not None
                    ):
                        children.append(ref)

        # no data for current graph level
        if len(children) == 0:
            return graph
        else:
            graph.append(children)
            return self.create_graph(xid, graph, len(graph) - 1, max_level)

    def get_graph_data(self, graph):
        """
        Description :
        --------------
        Get all articles' ids from citation graph.

        Attribute :
        ------------
        - graph : List of lists of objects. Each item in graph represents level.
        - level : Integer. Represents level of graph to extract data from.

        Output : Return list of objects.
        """
        references = []
        # exclude level 0 since it represents the query
        for subl in graph[1:]:
            for xid in subl:
                references.append(xid)

        return references
