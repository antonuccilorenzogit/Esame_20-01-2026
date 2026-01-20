import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._lista_nodi = []
        self._dict_nodi = {}
        self._lista_archi = []

    def BuildGraf(self, n_alb):
        self._lista_nodi = DAO.read_nodi(n_alb)
        print(self._lista_nodi)
        for node in self._lista_nodi:
            self._dict_nodi[node.id] = node
            self._graph.add_node(node)

        self._lista_archi = DAO.read_archi(self._dict_nodi)
        for u, v, peso in self._lista_archi:
            self._graph.add_edge(u, v, weight=peso)

    def get_artisti_vicini(self,id):
        nodo= self._dict_nodi[int(id)]
        result= []
        for node in self._graph.neighbors(nodo):
            result.append(node)
        return result, nodo

    def cerca_percorso(self, node_id, d_min,n_art):
        self.best_path = []
        self.best_weight = float('-inf')
        self._d_min=d_min
        self._n_art= n_art
        node= self._dict_nodi[int(node_id)]
        self._ricorsione([node], 0)

        return self.best_path, self.best_weight, node

    def _ricorsione(self, path, weight):
        last = path[-1]

        if len(path) > self._n_art:
            return

        if weight > self.best_weight:
            self.best_weight = weight
            self.best_path = copy.deepcopy(path)
            if len(path) == self._n_art:
                return

        vicini = self.trovo_vicini_accettabili(last)

        for node in vicini:
            edge_w = self._graph[last][node]['weight']
            if node in path:
                continue
            path.append(node)
            self._ricorsione(path, weight + edge_w)
            path.pop()

    def trovo_vicini_accettabili(self,nodo):
        result= []
        for node in self._graph.neighbors(nodo):
            if node.id in DAO.lista_artisti_ammissibili(node.id, self._d_min):
                result.append(node)
        return result

    def num_nodi(self):
        return self._graph.number_of_nodes()

    def num_archi(self):
        return self._graph.number_of_edges()


