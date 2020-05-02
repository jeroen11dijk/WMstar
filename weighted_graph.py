import cProfile
import networkx as nx
from matplotlib.pyplot import show

from mstar import Mstar

G = nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c', weight=0.4)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)
G.add_edge('b', 'f', weight=0.2)
G.add_edge('g', 'e', weight=0.7)
G.add_edge('g', 'a', weight=0.5)
G.add_edge('c', 'h', weight=0.1)
G.add_edge('h', 'd', weight=0.6)
G.add_edge('i', 'a', weight=0.3)
G.add_edge('i', 'c', weight=0.9)
G.add_edge('j', 'c', weight=0.1)
G.add_edge('h', 'k', weight=0.6)
G.add_edge('a', 'k', weight=0.7)
G.add_edge('b', 'h', weight=0.4)
G.add_edge('l', 'a', weight=0.1)
G.add_edge('l', 'h', weight=0.3)
G.add_edge('m', 'c', weight=0.8)
G.add_edge('m', 'f', weight=0.3)
G.add_edge('n', 'g', weight=0.7)
G.add_edge('n', 'h', weight=0.9)
G.add_edge('n', 'a', weight=0.5)
G.add_edge('o', 'a', weight=0.3)
G.add_edge('o', 'b', weight=0.1)
G.add_edge('o', 'k', weight=0.2)
G.add_edge('o', 'n', weight=0.9)

# nx.draw_networkx(G)
# show()
v_I = ('j', 'm', 'b', 'a', 'c', 'f')
v_W = ((), (), (), (), (), ())
v_F = ('l', 'b', 'h', 'j', 'g', 'o')

v_I2 = ('m', 'k', 'j', 'd')
v_W2 = ('c', 'a', 'l', 'b')
v_F2 = ('f', 'b', 'j', 'c')

# print(Mstar(G, v_I2, v_W2, v_F2))
cProfile.run('Mstar(G, v_I, v_W, v_F)')
# cProfile.run('Mstar(G, v_I2, v_W2, v_F2)')