#imports


class Node:
    def __init__(self,myName,myID,mySeq):
        self.name = myName
        self.ID = myID
        self.right = None 
        self.left = None 
        self.distances = [] #a list of tuples (sequence name, distance)
        self.seq = mySeq

    def printRoot(self,f):
        string = self.name
        if self.left:
            string += '('
            self.left.printTree(string,f)
            string += ')'
        if self.right:
            string += '('
            self.right.printTree(string,f)
            string += ')'
        return string
    
    def printTree(self,string,f): 
        string += self.name
        if self.left: 
            string += ':'+ str(self.distances[0]) + '('
            self.left.printTree(string,f)
            string += ')'
        if self.right: 
            string += ':'+ str(self.distances[0]) + '('
            self.right.printTree(string,f)
            string += ')'
        f.write(string + '\n')
            

#read strings from file (in: string fileName) into an array (out: [string])
def readStrings(fileName):
    #initializing 
    mySeqs = []
    myNames = []
    f = open(fileName,"r")
    seqName = ''
    sequence = ''
    counter = 0

    #reading and splitting file
    myFile = f.read()
    lineList = myFile.splitlines()
    
    #read through the file
    for line in lineList:
        if (counter%2==0):   #names and sequences alternate, using mod to do this
            boop = line
            seqName = boop.replace(">S", "")  #getting rid of pesky >'s 
            myNames.append(seqName)
        else:
            sequence = line 
            mySeqs.append(sequence)
        counter+=1
    f.close()
    return mySeqs, myNames

#returns (out: int distance) between two given sequences (in: 2 strings)
def calcDistance(s1,s2):
    dist = 0
    for i in range(0,len(s1)):
        if (s1[i] != s2[i]):
            dist+=1
    return dist

#initializes and returns an array of nodes, a node for each sequence.
def initNodes(seqs,names):
    myNodes = []
    for i in range (0,len(seqs)):
        myNodes.append(Node(names[i],i+1,seqs[i]))
    return myNodes

def initDistances(nodes):
    for s in range(0,len(nodes)):
        for s2 in range(0,len(nodes)):
            if (s != s2):
                nodes[s].distances.append((nodes[s2].ID,calcDistance(nodes[s].seq,nodes[s2].seq)))
            else:
                nodes[s].distances.append((nodes[s].ID,201))

#returns the ID's of the nodes with the minimum distance, changes multTrees to be true if there are multiple minimum distances. 
def takeMin2(nodes,multTrees):
    Min = 201
    node1 = -1
    node2 = -1
    for n in nodes:
        for d in n.distances:
            if (d[1] < Min):
                Min = d[1]
                node1 = n.ID
    for d in nodes[node1-1].distances:
        if (d[1] == Min):
            if (node2>0):
                multTrees = True
            else:
                node2 = d[0]

    return node1, node2

def connectNodes(nodes,ID1,ID2):
    for d in nodes[ID1-1].distances:
        if (d[1] == 201):
            d = (ID1,0)
    for d in nodes[ID2-1].distances:
        if (d[1] == 201):
            d = (ID2,0)
    #make parent    
    parent = Node((nodes[ID2-1].name + nodes[ID1-1].name),0,'')
    parent.left = nodes[ID1-1]
    parent.right = nodes[ID2-1]
    #make sure node2 is larger
    if (ID2 < ID1):
        temp = ID1
        ID1 = ID2
        ID2 = temp
    #remove newly connected nodes
    del nodes[ID2-1]
    del nodes[ID1-1]
    #calculate new distances and delete distances to old nodes
    for n in nodes:
        n.distances.append((len(nodes)+1,(n.distances[ID1-1][1]+n.distances[ID2-1][1])/2))
        parent.distances.append((n.ID,(n.distances[ID1-1][1]+n.distances[ID2-1][1])/2))
        del n.distances[ID2-1]
        del n.distances[ID1-1]    
    parent.distances.append((parent.ID,201))
    #add parent and redo ID's
    nodes.append(parent)
    redoIDs(nodes)

#recounts the ID's for indexing purposes.
def redoIDs(nodes):
    for i in range(0,len(nodes)):
        nodes[i].ID = i+1
        for d in range(0,len(nodes[i].distances)):
            nodes[i].distances[d] = (d+1, nodes[i].distances[d][1])

#builds a tree and returns the root
def buildTree(fileName):
    #initialization
    multTrees = False
    seqs, names = readStrings(fileName)
    nodes = initNodes(seqs,names)
    initDistances(nodes)
    #o1
    writeDistMat(nodes,'3.o1')
    #connect nodes til we have one big ol' tree
    while (len(nodes)>1):
        print 'nodes left: ' + str(len(nodes))
        ID1, ID2 = takeMin2(nodes,multTrees) 
        print nodes[ID1-1].name
        print nodes[ID2-1].name
        connectNodes(nodes,ID1,ID2)
    
    #3.o2
    f = open("3.o2","w+")
    f.write(nodes[0].printRoot(f))
    f.close()
    #3.o3
    f = open("3.o3","w+")
    f.write(str(multTrees))
    f.close()
    
    return nodes[0]

def writeDistMat(nodes,fileName):
    #init
    f = open(fileName,"w+")
    #top axis
    firstLine = '-  ' 
    for i in range(1,len(nodes)+1):
        firstLine += 'S' + str(i) + ' '
    firstLine += '\n'
    f.write(firstLine)
    
    #distances 
    for n in nodes:
        line = n.name + ' '
        for d in n.distances:
            line += (str(d[1]) + ' ')
        line += '\n'
        line = line.replace("201","0")
        f.write(line)
    f.close() 
    
###### run tha program ######

buildTree('3.in')
