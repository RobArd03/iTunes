import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMap = {}

    def buildGraph(self, durataMin):
        self._graph.clear()
        self._nodes = DAO.getAlbums(durataMin)
        self._graph.add_nodes_from(self._nodes)
        self._idMap = {n.AlbumId: n for n in self._nodes}
        self._allEdges = DAO.getAllEdges(self._idMap)
        self._graph.add_edges_from(self._allEdges)


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

