'''
Created on Oct 13, 2014

@author: scobb
'''
import copy, sys


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
        for node in self.nodes:
            if node.parent != None:
                ret_str += str(node) + '\n'
        return ret_str

def BFS(path, node_ind, target_node, start_time, end_time):
    path = copy.copy(path)
    if path.nodes[node_ind].id == target_node:
        # found it
        return path
    if start_time > end_time:
        # unsuccessful path
        path.nodes.pop(-1)
        return path
    for edge in node_to_edge[path.nodes[node_ind].id]:
    
        if Node(edge.n1, edge.t, path.nodes[node_ind].id) not in path.nodes and \
            edge.t >= start_time and edge.t <= end_time:
            # valid edge
            path.nodes.append(Node(edge.n1, edge.t, path.nodes[node_ind].id))
            path = BFS(path, node_ind+1, target_node, edge.t, end_time)
        elif Node(edge.n2, edge.t, path.nodes[node_ind].id) not in path.nodes and \
            edge.t >= start_time and edge.t <= end_time:
            # valid edge
            path.nodes.append(Node(edge.n2, edge.t, path.nodes[node_ind].id))
            path = BFS(path, node_ind+1, target_node, edge.t, end_time)
    
    if path.nodes[-1].id != target_node:
        path.nodes.pop(-1)
    
    return path
                
if __name__ == "__main__":
    
    file_name = sys.argv[1]
    #'Samples/input0.txt'
    
    edges = []
    file_handle = file(file_name, 'r')
    num_edges = int(file_handle.readline().split()[1])
    for _ in range(num_edges):
        node1, node2, time = file_handle.readline().split()
        edges.append(Edge(int(node1), int(node2), int(time)))
        
    from_node, to_node, start_time, end_time = file_handle.readline().split()
    
    path = Path(Node(int(from_node), int(start_time)))
    
    path = BFS(path, 0, int(to_node), int(start_time), int(end_time))
    
    print(len(path.nodes))
    print(path)

    
    
        
    