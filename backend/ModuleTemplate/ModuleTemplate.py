#coding=utf-8
"""
Module Template (Name of your module)
-----------------
Please write some introduction here
Author: Please put your name here
2021/9/24
"""


from Graph.Graph import Graph
# import something you need here



class ModuleTemplate():

    """
    private variables
    """
    __graph:Graph                   # graph database
    __privateVariableName = None    # private variable, only can be access by functions in this class


    """
    public variable
    """
    publicVariableName = None       # public variable, can be access by other programs


    def __init__(self, graph:Graph, inputVariable):
        """
        initialization, input must contain the graph api class
        you can add other input variables if you need
        """
        self.__graph = graph
        # do something here, such as initialize your own data
        print("initialize module template, and the input variable is "+str(inputVariable))


    def testAllAPIs(self, variableFromFrontEnd):
        """
        A public function, note that you should describe its input and output variable format here
        this function can test all the APIs and return there answer
        """

        # assign value to private variable
        self.__privateVariableName = "I am a private variable!"

        # test all APIs and return answer
        return {
            'private variable': self.__privateVariableName,
            'public variable': self.publicVariableName,
            'variable from front end': variableFromFrontEnd,
            'getNumberOfNodes': self.__graph.getNumberOfNodes(),
            'getNumberOfEdges': self.__graph.getNumberOfEdges(),
            'getAllnodeIdToName': self.__graph.getAllnodeIdToName(),
            'getAlledgeIdToName': self.__graph.getAlledgeIdToName(),
            'getAllTriples': self.__graph.getAllTriples(),
            'getNodeNameById(0)': self.__graph.getNodeNameById(0),
            'getNodeIdByName(节点0)': self.__graph.getNodeIdByName("节点0"),
            'getEdgeNameById(0)': self.__graph.getEdgeNameById(0),
            'getEdgeIdByName(边0)': self.__graph.getEdgeIdByName("边0"),
            'getHeadAndTailNodeIdByEdgeId(0)': self.__graph.getHeadAndTailNodeIdByEdgeId(0),
            'getInNeighbors(2)': self.__graph.getInNeighbors(2),
            'getOutNeighbors(2)': self.__graph.getOutNeighbors(2),
            'addNewNode(节点4)': self.__graph.addNewNode("节点4"),
            'addNewEdge(节点4,边5,节点5)': self.__graph.addNewEdge("节点4","边4","节点5"),
            'saveToDataBase()': self.__graph.saveToDataBase(),
            'toGraphJson([],[(0,0,1),(0,1,2),(2,2,1),(2,3,3)])': self.__graph.toGraphJson([],[(0,0,1),(0,1,2),(2,2,1),(2,3,3)]),
            'self.__getFullGraph()': self.__getFullGraph()
        }


    def __getFullGraph(self):
        """
        A private function, only functions inside this class can invoke it
        note that you should describe its input and output variable format here
        this function can return the full graph in json format
        """
        
        """
        if you need to show a graph in frontend, you need to return the correct json format
        An example graph is:    1 -> 2 -> 3
        Its correct json format is:
        {
            'graph':{
                'nodes': ['name of node 1', 'name of node 2', 'name of node 3'],
                'edges': [  ['name of node 1', 'name of edge 1->2', 'name of node 2'],
                            ['name of node 2', 'name of edge 2->3', 'name of node 3']   ]
            }
        }
        There is an API to help you return the correct json format, what you need is to prepare a list of node id and id triples
        then invoke function "self.__graph.toGraphJson(node id list, id triples list)"
        then you can "return {'graph': self.__graph.toGraphJson(node id list, id triples list)}"
        """
        # the following send the whole graph to frontend
        return {'graph': self.__graph.toGraphJson([], self.__graph.getAllTriples())}



