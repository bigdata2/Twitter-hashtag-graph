# Program that calculates the average degree of hashtags
# Created by Anurag Tiwari
import json 
import datetime 
import sys
import itertools
import collections
import networkx as nx
from tweets_cleaned import is_ascii, replaceEscapeChar

class hashTagGraph():
   """ A Twitter hashtag graph is a graph connecting all the hashtags that 
       have been mentioned together in a single tweet.
   """
   def __init__(self):
      self.G = nx.Graph() 
      self.dq = collections.deque()
      self.avgDegree = 0.0
      self.input_filename = sys.argv[1]
      self.outputfile = open(sys.argv[2], 'w')

   #Function to populate graph, manipulate it and report
   #average degree after arrival of each tweet.
   def average_degree(self):
      with open(self.input_filename) as inputfile:
         for line in inputfile:
            line = replaceEscapeChar(line)
            jsonline = (json.loads(line))
            if 'text' in jsonline:
               hashTagSet, tweetTime = self.cleandata(jsonline)
               if (len(hashTagSet) > 1):
                  self.addEdges(self.G, hashTagSet, tweetTime)
                  self.delEdges(self.G, tweetTime)
               else:
                  self.delEdges(self.G, tweetTime)
               self.rollingAvgDegree()
      self.outputfile.close()

   # This function is called after each tweet is processed. It provides the
   # average degree -- (sum of degree of nodes in graph)/(sum of all nodes)
   def rollingAvgDegree(self):
      Ginfo = (nx.info(self.G))
      deg = Ginfo.split("Average degree:",1)
      if(len(deg) > 1):
         self.avgDegree = round(float(deg[1].strip()), 2)
      else:
         self.avgDegree = 0.0
      self.outputfile.write(str(self.avgDegree)+"\n")

   # Clean and extract hashtag and timestamp data from a tweet
   def cleandata(self,jsonline):
      check_ascii, ascii_str = is_ascii(jsonline['text'])
      timestamp = jsonline['created_at']
      hashTagSet = self.extractHashTags(ascii_str.upper())
      tweetTime = datetime.datetime.strptime(timestamp, 
                  '%a %b %d %H:%M:%S %z %Y')
      return (hashTagSet, tweetTime)

   def extractHashTags(self, str):
      return set(part[0:] for part in str.split() if part.startswith('#'))

   # Add edges and corresponding nodes into the graph and add edge
   # information into a FIFO queue. If the edge already exist, increment
   # its weight by 1. 
   def addEdges(self, G, hashTagSet, tweetTime):
      for a, b in itertools.combinations(hashTagSet, 2):
         edge = (a, b, tweetTime)
         if G.has_edge(a, b):
            G[a][b]['weight'] += 1
         else:
            G.add_edge(a, b, weight=1)
         self.dq.append(edge)

   # Delete edges that are more than 60 seconds old. If the edge has a 
   # weight of more than one, i.e. there is more than one tweet containing 
   # the same hashtags, the weight will be decremented and the edge will
   # not be removed. After removing an edge, nodes connected to it are 
   # checked if they became disconnected, if so, they are removed. 
   def delEdges(self, G, tweetTime):
      seconds = 0
      if(self.dq):
         seconds = (tweetTime - self.dq[0][2]).total_seconds()
      while (seconds > 60) :
         a = self.dq[0][0] # get first node from the oldest edge tuple
         b = self.dq[0][1] # get second node from the edge tuple
         if (G[a][b]['weight'] > 1):
            G[a][b]['weight'] -= 1
         else:
            G.remove_edge(a,b)
         if(G.degree(a) == 0):
            G.remove_node(a)
         if(G.degree(b) == 0):
            G.remove_node(b)
         self.dq.popleft()
         if(self.dq):
            seconds = (tweetTime - self.dq[0][2]).total_seconds()
         else:
            break 

if __name__ == '__main__':
   htagGraph = hashTagGraph()
   htagGraph.average_degree()
