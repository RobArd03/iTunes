import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMap = {}
        self._bestSet = {}
        self._maxLen = 0

    def buildGraph(self, durataMin):
        self._graph.clear()
        self._nodes = DAO.getAlbums(durataMin)
        self._graph.add_nodes_from(self._nodes)
        self._idMap = {n.AlbumId: n for n in self._nodes}
        self._allEdges = DAO.getAllEdges(self._idMap)
        self._graph.add_edges_from(self._allEdges)


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        return self._nodes

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._graph, a1)
        return len(cc), self._getDuratatot(cc)

    def _getDuratatot(self, listOfNodes):
        return sum([n.dTot for n in listOfNodes])

    def getsetOfNodes(self, a1, soglia):
        self._bestSet = {}
        self._maxLen = 0

        parziale = {a1}
        cc = nx.node_connected_component(self._graph, a1)

        cc.remove(a1)

        for n in cc:
            # richiamo la ricorsione
            parziale.add(n)
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia)
            parziale.remove(n)
            cc.add(n)

        return self._bestSet, self._getDuratatot(self._bestSet)

    def _ricorsione(self, parziale, rimanenti, soglia):
        # 1) verifico che parziale sia una sol. ammissibile
        if self._getDuratatot(parziale) > soglia:
            return
        # 2) se parziale soddisfa i criteri, allora verifico se è migliore di bestSet
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)
        # 3) aggiungo e faccio ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n)





