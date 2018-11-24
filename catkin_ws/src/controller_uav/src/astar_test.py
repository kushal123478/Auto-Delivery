# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:06:26 2018

@author: Akshay
"""

import pickle
from grid_3D import Graph

def get_dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5
    
def find_path(V, B, D, costs, coords, successors, start, end, w, log):
    O = [start]
    C = []
    V[start] = 0
    while (end not in C):
        v = O[0]
        log.write("V = {}\n".format(v))
        C.append(v)
        O.remove(v)
        
        log.write("Successors of {} = {}\n".format(v, successors[v]))
        for n in successors[v]:
            log.write("Considering n = {}\n".format(n))
            if (n not in C):
                if (n not in O):
                    O.append(n)
                log.write("{} taken in\n".format(n))
                temp_ctc = costs[(v, n)] + V[v]
                if (temp_ctc < V[n]):
                    log.write("Updated V[{}] to {}\n".format(n, temp_ctc))
                    V[n] = temp_ctc
                    D[n] = V[n] + (w * get_dist(coords[n], coords[end]) + 1)
                    B[n] = v
                    
        O.sort(key = D.get)
    return get_path(B, start, end)
        
def get_path(B, start, end):
    v = end
    res = [end]
    while (v != start):
        res.append(B[v])
        v = B[v]
    res.reverse()
    return res

def load_graph(path, ugv_txt_path, uav_txt_path):
    with open(path, 'rb') as f:
        graph = pickle.load(f)
    edge_list = graph.get_edge_list()
    node_labels = {}
    new_graph = {}
    k = 1
    
    for node in graph.nodes:
        node_labels[node] = k
        k += 1    
    
    for edge in edge_list:
        new_graph[(node_labels[edge[0]], node_labels[edge[1]])] = edge[2]
        new_graph[(node_labels[edge[1]], node_labels[edge[0]])] = edge[2]
        
    neighbours = {k:[] for k in node_labels.values()}
    
    for start, end in new_graph:
        neighbours[start].append(end)
    
    ugv_path = str_to_path(ugv_txt_path, node_labels)
    uav_path = str_to_path(uav_txt_path, node_labels)
    
    return new_graph, neighbours, node_labels, ugv_path, uav_path

def str_to_path(txt_file_path, node_labels):
    final_path = []
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()
    
    for node in lines:
        x, y, z = node.split(', ')
        final_path.append(node_labels[(int(x), int(y), int(z))])
        
    return final_path

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
    
def remove_duplicates(path):
    res = []
    for x in path:
        if (x not in res): res.append(x)
    return res

def get_coord_points(path, node_labels):
    res = []
    for label in path:
        for location in node_labels:
            if (node_labels[location] == label):
                res.append(location)
                break
    return res

#def main(graph_obj_path):
graph_path = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\Graph.sav'
ugv_txt_path = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\ugv.txt'
uav_txt_path = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\uav.txt'
ugv_log = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\ugv_log.txt'
uav_log = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\uav_log.txt'
costs, neighbours, node_labels, ugv_path, uav_path = load_graph(graph_path, ugv_txt_path, uav_txt_path)
ugv_op_path = []
uav_op_path = []

with open(ugv_log, 'a') as log:
    deleteContent(log)
    for i in range(len(ugv_path) - 1):
        
        B = {k:None for k in node_labels.values()}
        V = {key:float('inf') for key in node_labels.values()}
        D = {key:float('inf') for key in node_labels.values()}
                
        curr_op_path = find_path(V, B, D, costs, list(node_labels.keys()), neighbours, 
                                ugv_path[i], ugv_path[i + 1], 1, log)
        ugv_op_path += curr_op_path
        
with open(uav_log, 'a') as log:
    deleteContent(log)
    for i in range(len(uav_path) - 1):
        
        B = {k:None for k in node_labels.values()}
        V = {key:float('inf') for key in node_labels.values()}
        D = {key:float('inf') for key in node_labels.values()}
                
        curr_op_path = find_path(V, B, D, costs, list(node_labels.keys()), neighbours, 
                                uav_path[i], uav_path[i + 1], 1, log)
        uav_op_path += curr_op_path

ugv_op_path = get_coord_points(remove_duplicates(ugv_op_path), node_labels)
uav_op_path = get_coord_points(remove_duplicates(uav_op_path), node_labels)

print (ugv_op_path)
print (uav_op_path)
                
#if (__name__ == '__main__'):
#    graph_obj_path = 'C:\\Users\\HP\\Desktop\\Homeworks\\ARMP\\Project\\Graph.sav'
#    main(graph_obj_path)