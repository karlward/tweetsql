#!/usr/bin/env python

import networkx as nx
import re

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Tweet, User, Word

def graph_add_node(n, g, t):
    if g.has_node(n):
        g.node[n]['weight']+=1
    else:
        g.add_node(n)
        g.node[n]['label'] = n
        g.node[n]['weight'] = 1
        g.node[n]['type'] = t
 
def graph_add_edge(n1, n2, g):
    if g.has_edge(n1, n2):
        g[n1][n2]['weight']+=1
    else:
        g.add_edge(n1,n2)
        g[n1][n2]['weight']=1

graph = nx.Graph()

# iterate through every tweet, storing each tweet in t
for t in db_session.query(Tweet).all():
    # add t to the graph
    graph_add_node(t.tweet, graph, 'tweet')
    # now iterate through all the words in t, storing each word in w
    for w in t.words:
        # looking for hashtags (there's a better way to do this)
        if w.word[0] == '#':
            graph_add_node(w.word, graph, 'hashtag')
            graph_add_edge(t.tweet, w.word, graph)

# you probably want to change this string to something meaningful too
q = 'example'

# because it ends up in the file name for the GEXF output file
nx.write_gexf(graph, '{}_tweet_graph.gexf'.format(q))
print('{}_tweet_graph.gexf'.format(q))
