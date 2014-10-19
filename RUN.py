#!/usr/bin/env python
'''
Created on Oct 13, 2014

@author: scobb
'''
import sys


# create dictionary (hash table): node -> edge list
NODE_STATUS_DICT = dict()

# global path object that we will update
PATH = None

class Node(object):
    def __init__(self, id, t, parent=None):
        self.id = id
        self.parent = parent
        self.t = t
        
    def __eq__(self, other):
        return self.id == other.id
    
    def __str__(self):
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
        # note: 'in' is O(1) check for dictionaries
        if n1 in NODE_STATUS_DICT:
            NODE_STATUS_DICT[n1]['edges'].append(self)
        else:
            NODE_STATUS_DICT[n1] = {'traversed': False,
                                    'edges': [self]
                                    }
        
        if n2 in NODE_STATUS_DICT:
            NODE_STATUS_DICT[n2]['edges'].append(self)
        else:
            NODE_STATUS_DICT[n2] = {'traversed': False,
                                    'edges': [self]
                                    }

    def __str__(self):
        return '%s %s %s' % (str(self.n1),
                            str(self.n2),
                            str(self.t))
        
class Path(object):
    def __init__(self, start):
        self.nodes = [start]
        self.edges = []
        
    def __str__(self):
        ret_str = str(len(self.edges)) + '\n'
        prefix = ''
        for edge in self.edges:
            ret_str += prefix + str(edge)
            prefix = '\n'
        return ret_str
    
    def remove_last_node(self):
        self.nodes.pop(-1)
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def remove_last_edge(self):
        if self.edges:
            self.edges.pop(-1)
        
    def get_last_node(self):
        return self.nodes[-1]
    
    def traverse(self, node, edge):
        self.add_node(node)
        self.add_edge(edge)
    
    def backtrack(self):
        self.remove_last_edge()
        self.remove_last_node()

def DFS(node_ind, target_node, start_time, end_time):
    ''' DFS - recursive depth-first search. Alters PATH in place such that
    it connects 0th node to the target node with edges meeting the time
    requirements.
    
    Time complexity: O(m)
    '''
    if start_time > end_time:
        # unsuccessful base case
        PATH.backtrack()
        return
    if PATH.nodes[node_ind].id == target_node:
        # successful base case
        return
    while len(NODE_STATUS_DICT[PATH.nodes[node_ind].id]['edges']) > 0 and \
        PATH.get_last_node().id != target_node:
        # we will traverse each edge at most once
        edge = NODE_STATUS_DICT[PATH.nodes[node_ind].id]['edges'].pop(0)
        n1 = Node(edge.n1, edge.t, PATH.nodes[node_ind].id)
        n2 = Node(edge.n2, edge.t, PATH.nodes[node_ind].id)
        if not NODE_STATUS_DICT[n1.id]['traversed'] and edge.t >= start_time:
            # valid node to add, but mark it off
            PATH.traverse(n1, edge)
            NODE_STATUS_DICT[n1.id]['traversed'] = True
            DFS(node_ind+1, target_node, edge.t, end_time)
        elif not NODE_STATUS_DICT[n2.id]['traversed'] and edge.t >= start_time:
            # valid node to add, but mark it off
            PATH.traverse(n2, edge)
            NODE_STATUS_DICT[n2.id]['traversed'] = True
            DFS(node_ind+1, target_node, edge.t, end_time)
    
    if PATH.get_last_node().id != target_node:
        # unsuccessful case - backtrack
        PATH.backtrack()
        
def main(file_name):
    
    edges = []
    file_handle = open(file_name, 'r')
    
    # parse the file
    num_edges = int(file_handle.readline().split()[1])
    for _ in range(num_edges):
        node1, node2, time = file_handle.readline().split()
        edges.append(Edge(int(node1), int(node2), int(time)))
        
    from_node, to_node, start_time, end_time = file_handle.readline().split()
    
    # create PATH object with start node, mark start node traversed
    global PATH 
    PATH = Path(Node(int(from_node), int(start_time)))
    NODE_STATUS_DICT[int(from_node)]['traversed'] = True

    # recursive DFS to find PATH (alters in place)
    DFS(0, int(to_node), int(start_time), int(end_time))
    
    if (len(PATH.nodes) > 0):
        print(PATH)
    else:
        print (len(PATH.nodes))
    
                
if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except:
        print('Missing filename argument\nUsage: %s <filename>' % sys.argv[0])
        exit(1)
    main(file_name)
    
        
    
