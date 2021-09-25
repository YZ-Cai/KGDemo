#coding=utf-8
from Graph.Graph import Graph
from BasicService.BasicService import BasicService
from ModuleTemplate.ModuleTemplate import ModuleTemplate
from flask import Flask, request
import json
app = Flask(__name__)


"""
initializations when start server service
"""
graph = Graph("../data/DefaultDataset")                     # load in graph data
basicService = BasicService(graph)                          # initialize basic service
moduleTemplate = ModuleTemplate(graph, inputVariable=100)   # initialize ModuleTemplate 


"""
APIs for front end
"""
# get full graph
@app.route('/getFullGraph',methods=['POST'])
def getFullGraph():
    return basicService.getFullGraph()

# get all neighbors of a node
@app.route('/getNeighbors',methods=['POST'])
def getNeighbors():
    responseDict = json.loads(str(request.get_data(), "utf8"))
    nodeName = responseDict.get('nodename')
    return basicService.getNeighbors(nodeName)

# test module template 
@app.route('/testModuleTemplate',methods=['POST'])
def testModuleTemplate():
    
    # get the input data from front end
    responseDict = json.loads(str(request.get_data(), "utf8"))
    variableFromFrontEnd = responseDict.get('variableFromFrontEnd')
    
    # modify public variable
    moduleTemplate.publicVariableName = "I am a public variable!"
    
    # invoke the public function
    return moduleTemplate.testAllAPIs(variableFromFrontEnd)


"""
start the server
"""
app.run(host='0.0.0.0', port=5000)  # 0.0.0.0代表本机任何地址均可访问
