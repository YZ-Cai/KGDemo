#coding=utf-8
"""
Basic Graph Services
-----------------
Author: Yuzheng Cai
2021/9/24
"""



from Graph.Graph import Graph


class BasicService():

    """
    private variables
    """
    __graph:Graph           # graph database
    
    
    def __init__(self, graph:Graph):
        """
        initialization
        """
        self.__graph = graph

    
    def getFullGraph(self):
        """
        return the full graph in json format
        """
        return {'graph': self.__graph.toGraphJson([], self.__graph.getAllTriples())}


    def getNeighbors(self, nodeName):
        """
        return a node and its neighbors and their edges in json format
        """
        nodeId = self.__graph.getNodeIdByName(nodeName)
        nodeIds = []
        idTriples = []
        if nodeId!=-1:
            nodeIds.append(nodeId)
            # in-neighbors
            for edgeId, inNeighborId in self.__graph.getInNeighbors(nodeId):
                idTriples.append([inNeighborId, edgeId, nodeId])
            # out-neighbors
            for edgeId, outNeighborId in self.__graph.getOutNeighbors(nodeId):
                idTriples.append([nodeId, edgeId, outNeighborId])
        return {'graph': self.__graph.toGraphJson(nodeIds, idTriples)}
        