#coding=utf-8
"""
Graph DataBase APIs
-----------------
Reading and writing APIs for all services
Author: Yuzheng Cai
2021/9/23
"""



class Graph():

    """
    private variables
    """
    __datasetName = ""      # dataset name
    __N = 0                 # number of nodes
    __M = 0                 # number of edges
    __nodeIdToName = []     # list for mapping node's id to its name/attribute, __nodeIdToName[node id] = node name
    __edgeIdToName = []     # list for mapping edge's id to its name/attribute, __edgeIdToName[edge id] = edge name
    __triples = []          # list contains all triples, __triples[edge id] = (head node id, edge id, tail node id) 
    __inNeighbors = []      # list contains in-neighbors of each node, __inNeighbors[node id] = [(edge id, in-neighbor id),...]
    __outNeighbors = []     # list contains out-neighbors of each node, __outNeighbors[node id] = [(edge id, out-neighbor id),...]
    __nodeNameToId = {}     # dictionary mapping node name to node id, __nodeNameToId[node name] = node id
    __edgeNameToId = {}     # dictionary mapping edge name to node id, __edgeNameToId[edge name] = a list of edge ids

    
    def __init__(self, datasetName):
        """
        initialization
        """
        self.__datasetName = datasetName
        self.__loadDataset()

    
    def __loadDataset(self):
        """
        load in graph dataset
        """
        try:
            # load nodes mapping
            nodeIdToNameFile = open(self.__datasetName+"/NodesMapping.txt", encoding="utf8")
            for line in nodeIdToNameFile.readlines():
                elements = line.strip().split(",")
                if len(elements)==2:
                    if elements[0]==str(len(self.__nodeIdToName)):
                        self.__nodeIdToName.append(elements[1])
                    else:
                        print("ERROR! Node id "+elements[0]+" is inconsistent in line "+str(len(self.__nodeIdToName))+" of "+self.__datasetName+"/nodeIdToName.txt!")
                        raise
                    if elements[1] in self.__nodeNameToId:
                        print("ERROR! Node name \'"+elements[1]+"\' is duplicate in line "+str(len(self.__nodeIdToName))+" of "+self.__datasetName+"/nodeIdToName.txt!")
                        raise
                    else:
                        self.__nodeNameToId[elements[1]] = int(elements[0])
            self.__N = len(self.__nodeIdToName)
            nodeIdToNameFile.close()

            # load edges mapping
            edgeIdToNameFile = open(self.__datasetName+"/EdgesMapping.txt", encoding="utf8")
            for line in edgeIdToNameFile.readlines():
                elements = line.strip().split(",")
                if len(elements)==2:
                    if elements[0]==str(len(self.__edgeIdToName)):
                        self.__edgeIdToName.append(elements[1])
                    else:
                        print("ERROR! Edge id "+elements[0]+" is inconsistent in line "+str(len(self.__edgeIdToName))+" of "+self.__datasetName+"/edgeIdToName.txt!")
                        raise
                    if elements[1] in self.__edgeNameToId:
                        self.__edgeNameToId[elements[1]].append(int(elements[0]))
                    else:
                        self.__edgeNameToId[elements[1]] = [int(elements[0])]
            self.__M = len(self.__edgeIdToName)
            edgeIdToNameFile.close()

            # initialize in-neighbors and out-neighbors
            for i in range(self.__N):
                self.__inNeighbors.append([])
                self.__outNeighbors.append([])

            # load triples
            triplesFile = open(self.__datasetName+"/Triples.txt", encoding="utf8")
            for line in triplesFile.readlines():
                elements = line.strip().split(",")
                if len(elements)==3:
                    h, r, t = int(elements[0]), int(elements[1]), int(elements[2])
                    if r==len(self.__triples) and h>=0 and h<self.__N and r>=0 and r<self.__M and t>=0 and t<self.__N:
                        self.__triples.append((h, r, t))
                        self.__inNeighbors[t].append((r, h))
                        self.__outNeighbors[h].append((r, t))
                    else:
                        print("ERROR! In line "+str(len(self.__triples))+" of "+self.__datasetName+"/Triples.txt!")

            if len(self.__triples)==self.__M:
                print("Successfully loaded in graph data! |V|="+str(self.__N)+" |E|="+str(self.__M))
            else:
                print("ERROR! The number of Triples is not consistent with the number of edges!")
                raise
            triplesFile.close()

        except:
            print("ERROR! Fail to load graph dataset: "+self.__datasetName)

    
    def getNumberOfNodes(self):
        return self.__N
    

    def getNumberOfEdges(self):
        return self.__M


    def getAllnodeIdToName(self):
        """
        return a list, list[node id (int)] = node name (string)
        """
        return self.__nodeIdToName


    def getAlledgeIdToName(self):
        """
        return a list, list[edge id (int)] = edge name (string)
        """
        return self.__edgeIdToName


    def getAllTriples(self):
        """
        return a list, list[edge id (int)] = (head node id, edge id, tail node id) 
        """
        return self.__triples

    
    def getNodeNameById(self, nodeId):
        """
        return a node's name (string) given its id (int), returns -1 if error
        """
        if nodeId>=0 and nodeId<self.__N:
            return self.__nodeIdToName[nodeId]
        else:
            print("ERROR! Can not find a node with id="+str(nodeId)+". Node id from 0 to "+str(self.__N-1)+" required.")
            return -1


    def getNodeIdByName(self, nodeName):
        """
        return a node's id (int) given its name (string), returns -1 if not found
        """
        if nodeName in self.__nodeNameToId:
            return self.__nodeNameToId[nodeName]
        else:
            return -1
    

    def getEdgeNameById(self, edgeId):
        """
        return an edge's name (string) given its id (int), returns -1 if error
        """
        if edgeId>=0 and edgeId<self.__M:
            return self.__edgeIdToName[edgeId]
        else:
            print("ERROR! Can not find an edge with id="+str(edgeId)+". Edge id from 0 to "+str(self.__M-1)+" required.")
            return -1

    
    def getEdgeIdByName(self, edgeName):
        """
        return a list of edge's ids (list of int) given its name (string), returns -1 if not found
        """
        if edgeName in self.__edgeNameToId[edgeName]:
            return self.__edgeNameToId[edgeName]
        else:
            return -1

    
    def getHeadAndTailNodeIdByEdgeId(self, edgeId):
        """
        return (head node id, tail node id) given an edge id, returns (-1, -1) if error
        """
        if edgeId>=0 and edgeId<self.__M:
            triple = self.__triples[edgeId]
            return (triple[0], triple[2])
        else:
            print("ERROR! Can not find an edge with id="+str(edgeId)+". Edge id from 0 to "+str(self.__M-1)+" required.")
            return -1


    def getInNeighbors(self, nodeId):
        """
        given a node id, return a list of tuples: [(edge id, in-neighbor id),...], returns -1 if error
        """
        if nodeId>=0 and nodeId<self.__N:
            return self.__inNeighbors[nodeId]
        else:
            print("ERROR! Can not find a node with id="+str(nodeId)+". Node id from 0 to "+str(self.__N-1)+" required.")
            return -1
                

    def getOutNeighbors(self, nodeId):
        """
        given a node id, return a list of tuples: [(edge id, out-neighbor id),...], returns -1 if error
        """
        if nodeId>=0 and nodeId<self.__N:
            return self.__outNeighbors[nodeId]
        else:
            print("ERROR! Can not find a node with id="+str(nodeId)+". Node id from 0 to "+str(self.__N-1)+" required.")
            return -1


    def addNewNode(self, nodeName):
        """
        create a new node given a node name (string), return a node id (int).
        if a node already exists, return its id directly(int).
        please invoke function saveToDataBase() to save data to disk, or it will be lost when program terminated.
        to avoid frequently IO, please invoke saveToDataBase() after a batch of modifications are done.
        """
        if nodeName in self.__nodeNameToId:
            return self.__nodeNameToId[nodeName]
        else:
            nodeId = self.__N
            self.__nodeIdToName.append(nodeName)
            self.__nodeNameToId[nodeName] = nodeId
            self.__inNeighbors.append([])
            self.__outNeighbors.append([])
            self.__N += 1
            return nodeId


    def addNewEdge(self, headNodeName, edgeName, tailNodeName):
        """
        create a new edge given (head node name, relation name, tail node name) (triple of string).
        return (head node id, edge id, tail node id).
        please invoke function saveToDataBase() to save data to disk, or it will be lost when program terminated.
        to avoid frequently IO, please invoke saveToDataBase() after a batch of modifications are done.
        """
        headNodeId = self.addNewNode(headNodeName)
        tailNodeId = self.addNewNode(tailNodeName)
        edgeId = self.__M

        # update edge storage
        self.__edgeIdToName.append(edgeName)
        if edgeName in self.__edgeNameToId:
            self.__edgeNameToId[edgeName].append(edgeId)
        else:
            self.__edgeNameToId[edgeName] = [edgeId]
        self.__triples.append((headNodeId, edgeId, tailNodeId))
        self.__M += 1

        # update neighbors
        self.__outNeighbors[headNodeId].append((edgeId, tailNodeId))
        self.__inNeighbors[tailNodeId].append((edgeId, headNodeId))

        return (headNodeId, edgeId, tailNodeId)


    def saveToDataBase(self):
        """
        save current graph to database file, return 0 if success, else return -1
        """
        try:
            # update node id to name mapping
            nodeIdToNameFile = open(self.__datasetName+"/NodesMapping.txt", "w+", encoding="utf8")
            outputLines = []
            for i in range(self.__N):
                outputLines.append(str(i)+","+self.__nodeIdToName[i])
            nodeIdToNameFile.write("\n".join(outputLines))
            nodeIdToNameFile.close()

            # update edge id to name mapping
            edgeIdToNameFile = open(self.__datasetName+"/EdgesMapping.txt", "w+", encoding="utf8")
            outputLines = []
            for i in range(self.__M):
                outputLines.append(str(i)+","+self.__edgeIdToName[i])
            edgeIdToNameFile.write("\n".join(outputLines))
            edgeIdToNameFile.close()

            # update tiples
            triplesFile = open(self.__datasetName+"/Triples.txt", "w+", encoding="utf8")
            outputLines = []
            for i in range(self.__M):
                outputLines.append(str(self.__triples[i][0])+","+str(self.__triples[i][1])+","+str(self.__triples[i][2]))
            triplesFile.write("\n".join(outputLines))
            triplesFile.close()

            return 0
        except:
            return -1    


    def toGraphJson(self, nodesIdList, idTriplesList):
        """
        given a list of node ids and a list of id triples (head node id, edge id, tail id),
        return the json format for front end {'nodes':[node name,...], 'edges':[(h,r,t),...]}
        """

        # convert edges
        nodesIdSet = set(nodesIdList)
        triples = []
        for hId, rId, tId in idTriplesList:
            h = self.getNodeNameById(hId)
            r = self.getEdgeNameById(rId)
            t = self.getNodeNameById(tId)
            if h!=-1 and r!=-1 and t!=-1:
                nodesIdSet.add(hId)
                nodesIdSet.add(tId)
                triples.append([h, r, t])

        # convert nodes
        nodesIdList = list(nodesIdSet)
        nodesNames = []
        for nodeId in nodesIdList:
            nodeName = self.getNodeNameById(nodeId)
            if nodeName!=-1:
                nodesNames.append(nodeName)

        return {'nodes':nodesNames, 'edges':triples}

        
