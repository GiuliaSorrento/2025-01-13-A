import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._classificazioni = []
        self._idMapC = {}
        self._optPath = None
        self._optLen = None

        def get_list_nodes(self):
            self._bestListNodes = []
            self._bestScore = len(self._graph.nodes)
            self._bestLen = 0

            allNodes = list(self._graph.nodes)
            allNodes.sort(key=lambda x: x.GeneID)

            for root in allNodes:
                rimanenti = copy.deepcopy(allNodes)
                rimanenti.remove(root)
                rimanenti = [x for x in rimanenti if x.Essential == root.Essential]

                self._ricorsione([root], list(rimanenti))

            print(self._bestLen, self._bestScore)
            return self._bestListNodes, self._bestLen, self._bestScore

        def _ricorsione(self, parziale, rimanenti):
            if len(parziale) > self._bestLen:
                self._bestLen = len(parziale)
                self._bestScore = self._getScore(parziale)
                self._bestListNodes = copy.deepcopy(parziale)
                if len(parziale) == self._bestLen:
                    if self._getScore(parziale) < self._bestScore:
                        self._bestScore = self._getScore(parziale)
                        self._bestListNodes = copy.deepcopy(parziale)

            if len(rimanenti) == 0:
                return

            for n in rimanenti:
                if n.GeneID > parziale[-1].GeneID:
                    parziale.append(n)
                    rimanenti.remove(n)
                    self._ricorsione(parziale, rimanenti)
                    parziale.remove(n)
                    rimanenti.append(n)

        def _getScore(self, parziale):
            return nx.number_connected_components(self._graph.subgraph(parziale))

    def getLocalizations(self):
        return DAO.getAllLocalizations()

    def buildGraph(self, loc):
        self._graph.clear()
        self._classificazioni = DAO.getAllNodes(loc)
        for c in self._classificazioni:
            self._idMapC[c.GeneID] = c    #numero di nodi giusto

        self._graph.add_nodes_from(self._classificazioni)  #num nodi giusto

        mapGeneCromo= DAO.getMapGeneCromo(loc,self._idMapC)   #numero di nodi giusto

        interazioni = DAO.get_all_interactions()
        for inter in interazioni:
            if inter.GeneID1  in self._idMapC and inter.GeneID2  in self._idMapC:
                nodo1 = self._idMapC[inter.GeneID1]
                nodo2 = self._idMapC[inter.GeneID2]
                if nodo1!=nodo2:
                    self._graph.add_edge(nodo1, nodo2)

        for e in self._graph.edges:
            crom1 = mapGeneCromo[e[0]]
            crom2 = mapGeneCromo[e[1]]
            if crom1 == crom2:
                self._graph[e[0]][e[1]]["weight"]= crom1
            else:
                self._graph[e[0]][e[1]]["weight"]= crom1+crom2



    def getGraphDetails(self):
        return len(self._graph.nodes) , len(self._graph.edges) #num nodi giusto

    def getArchiPesoCres(self):
        #ordinati in senso crescente di peso
        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"])
        return edges

    def get_connesse(self):
        """tutte le componenti connesse del grafo di dimensione
            maggiore di 1, in ordine decrescente di dimensione (vedere screenshots sotto). Per ogni componente
            connessa stampare il GeneID dei nodi nella componente e la dimensione della componente."""
        return sorted(nx.connected_components(self._graph), key=lambda connessa: len(connessa), reverse=True)