import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph() #semplice, non orientato e pesato
        self._airports = DAO.getAllAirports()
        self._idMapAirports ={}
        for i in self._airports:
            self._idMapAirports[i.ID]=i
        self._bestPath = []
        self._bestObjFun = 0

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addAllArchiV1()
        print(len( self._graph.nodes))
        print(len(self._graph.edges))

    def addAllArchiV1(self):
        allEdges = DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP,e.aeroportoD):
                    self._graph[e.aeroportoP][e.aeroportoD]['weight']+=e.peso
                else:
                    self._graph.add_edge(e.aeroportoP,e.aeroportoD, weight=e.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node)
        neighbTuples = []
        for n in neighbors:
            neighbTuples.append(((n, self._graph[node][n]['weight'])))

        neighbTuples.sort(key=lambda x : x[1])
        return neighbTuples

    def getPath(self,v0,v1):
        path = nx.dijkstra_path(self._graph, v0, v1)
        return path

    def getCamminoOttimo(self, v0, v1, t):
        self._bestPath = []
        self._bestObjFun = 0
        parziale=[v0]
        self._ricorsione(parziale, v1, t)
        return self._bestPath, self._bestObjFun

    def _ricorsione(self, parziale, v1, t):
        #verificare se parziale è una possibile soluzione
            #verificare se parziale è meglio del best corrente
                #in ogni caso esco
        if parziale[-1]==v1: #se la destinazione finale corrisponde al mio aeroporto di arrivo
            if self.getObjFun(parziale)>self._bestObjFun:
                self._bestPath=copy.deepcopy(parziale)
                self._bestObjFun=self.getObjFun(parziale)
        if len(parziale)==t+1:
            return
        #se arrivo qui è perchè posso ancora aggiungere nodi, quindi partendo dall'ultimo nodo che ho aggiunto prendo i
        #vicini e li aggiungo
        else:
            neigh = list(neighbors(self._graph, parziale[-1])) #ricorda di metterli in una lista
            for n in neigh:
                if n not in parziale: #verificare se sono già passato per quel nodo o no
                    parziale.append(n)
                    self._ricorsione(parziale, v1, t)
                    parziale.pop() #backtracking


    def getObjFun(self, listOfNodes):
        #devo sommare il valore dei pesi di tutti gli archi
        objval=0
        for i in range(0, len(listOfNodes)-1):
            objval += self._graph[listOfNodes[i]][listOfNodes[i+1]]['weight']
        return objval

