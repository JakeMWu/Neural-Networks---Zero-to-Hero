# Python file for ease of reading
import math
import numpy as np
import matplotlib.pyplot as plt 
from graphviz import Digraph
%matplotlib inline

class Value:
    
    def __init__(self,data, _children=(), _op=''):
        self.data = data
        # Children is a tuple, set may be more efficient
        # it allows us to see the values composing the value
        # we're interested in 
        self._prev = set(_children)
        # We also want to track the operations which led to 
        # our value (node?)
        self._op = _op
    
    # repr formats the expression
    def __repr__(self):
        return f"Value(data={self.data})"
    
    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), '+')
        return out 
    
    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), '*')
        return out 

    def trace(root):
    # builds a set of all nodes and edges in a graph
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges
    
#for graph visualization 
def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'}) # LR = left to right
    
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        # for any value in the graph, create a rectangular ('record') node for it
        dot.node(name = uid, label = "{data %.4f}" % (n.data, ), shape='record')
        if n._op:
            # if this value is a result of some operation create an op node for it 
            dot.node(name = uid+ n._op, label = n._op)
            # and connect this node to it
            dot.edge(uid + n._op, uid)
            
    for n1, n2 in edges:
        #connect n1 to the op node of n2
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
        
    return dot #alternatively dot.render(view=True)

a = Value(2.0)
b = Value(-3.0)
c = Value(10.0)
d = a*b + c
d

draw_dot(d)
