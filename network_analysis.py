#!/usr/bin/env python
'''
Created on Oct 13, 2014

@author: scobb
'''
import sys


# create dictionary (hash table): node -> edge list
node_to_edge = dict()

class Node(object):
    def __init__(self, id, t, parent=None):
        self.id = id
        self.parent = parent
        self.t = t
        
    def __eq__(self, other):
        return self.id == other.id
    
    def __str__(self):
        #return '%s %s %s' % (str(self.parent), str(self.id), str(self.t))
        if self.parent != None:
            return '%s %s %s' % (str(self.parent), str(self.id), str(self.t))
        else:
            return ''

class Edge(object):
    def __init__(self, n1, n2, t):
        self.n1 = n1
        self.n2 = n2
        self.t = t
        
        # update edge dictionary - maps nodes to edges
        if n1 in node_to_edge:
            node_to_edge[n1].append(self)
        else:
            node_to_edge[n1] = [self]
        
        if n2 in node_to_edge:
            node_to_edge[n2].append(self)
        else:
            node_to_edge[n2] = [self]
    
    def __str__(self):
        return '[%s---%s at %s]' % (str(self.n1),
                                    str(self.n2),
                                    str(self.t))
        
class Path(object):
    def __init__(self, start):
        self.nodes = [start]
        
    def __str__(self):
        ret_str = ''
        prefix = ''
        for node in self.nodes:
            if node.parent != None:
                ret_str += prefix + str(node)
                prefix = '\n'
        return ret_str
    
    def remove_last_node(self):
        self.nodes.pop(-1)
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def get_last_node(self):
        return self.nodes[-1]

def BFS(path, node_ind, target_node, start_time, end_time):
    ''' BFS - recursieve breadth-first search. Alters path in place such that
    it connects 0th node to the target node with edges meeting the time
    requirements.
    
    Time complexity: O(m+n)
    '''
    if path.nodes[node_ind].id == target_node:
        # found it
        return
    if start_time > end_time:
        # unsuccessful path
        path.remove_last_node()
        return
    for edge in node_to_edge[path.nodes[node_ind].id]:
        n1 = Node(edge.n1, edge.t, path.nodes[node_ind].id)
        n2 = Node(edge.n2, edge.t, path.nodes[node_ind].id)
        if n1 not in path.nodes and edge.t >= start_time and \
          edge.t <= end_time:
            # valid edge
            path.add_node(n1)
            BFS(path, node_ind+1, target_node, edge.t, end_time)
        elif n2 not in path.nodes and edge.t >= start_time and \
          edge.t <= end_time:
            # valid edge
            path.add_node(n2)
            BFS(path, node_ind+1, target_node, edge.t, end_time)
    
    if path.get_last_node().id != target_node:
        path.remove_last_node()
    
                
if __name__ == "__main__":
    
    try:
        file_name = sys.argv[1]
        #'Samples/input0.txt'
    except:
        print('Missing filename argument\nUsage: %s <filename>' % sys.argv[0])
        exit(1)
    
    edges = []
    file_handle = open(file_name, 'r')
    
    # parse the file
    num_edges = int(file_handle.readline().split()[1])
    for _ in range(num_edges):
        node1, node2, time = file_handle.readline().split()
        edges.append(Edge(int(node1), int(node2), int(time)))
        
    from_node, to_node, start_time, end_time = file_handle.readline().split()
    
    # create path object
    path = Path(Node(int(from_node), int(start_time)))
    
    # recursive BFS to find path (alters in place)
    BFS(path, 0, int(to_node), int(start_time), int(end_time))
    
    if (len(path.nodes) > 0):
        print(len(path.nodes) -1)
        print(path)
    else:
        print (len(path.nodes))

    
    
        
    