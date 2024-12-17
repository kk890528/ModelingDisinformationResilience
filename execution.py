# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
import pandas as pd
import random
from model import dis_information  
def simulate_information_cascade(N,network,steps,w=0.1,alpha=0.05,b1=3,b2=3,n_mali_act_1=0,n_mali_act_0=0,c=0.2):
    '''
Input:
    N: the number of nodes
    alpha: agent’s sensitivity to social pressure.
    steps: number of rounds
    
    w:Network adaptability controls the probability of connecting and disconnecting.
    b1: Controls the degree of hardness or softness in the softmax-like function of accepting disinformation
    b2: Controls the degree of hardness or softness in the softmax-like function of disconnection.
    n_mali_act_1= number of nodes of malicious agents with position '1'
    n_mali_act_0= number of nodes of malicious agents with position '0'
    c= Probability of connecting friends to friends; otherwise, connecting to random agents in the graph.
Output:
    Share: the share time of each disinoformation each round
    Mis_info: The position of disinformation
    modularity: the modularity of the  network
    group_assortativity: The dictionary contains three types of assortativity based on conviction. The key '0' represents the assortativity of the network comprising individuals holding position 0, while the key '1' denotes the assortativity of those holding position 1. The key 'all' indicates the assortativity of the entire network.
    position: the position of each agent in the end of simulation
    degrees: the degree centrality of each agent
    mali_act_1: the nodes of malicious agents with position '1'
    mali_act_0: the nodes of malicious agents with position '0'
    '''
    # gernerated the attitude of each agent.
    Q=np.random.uniform(-1, 1, size=(N,2))
    # The position of each agent.
    position=Q[:,1]>Q[:,0]
    # select the malicious actors
    mali_act_1=list(np.random.choice(np.array(network.nodes)[position],n_mali_act_1))
    mali_act_0=list(np.random.choice(np.array(network.nodes)[position==False],n_mali_act_0))
    
    # set the arttributes of malicious actors
    for node in mali_act_1:
      Q[node,0]=-10
      Q[node,1]=10
    for node in mali_act_0:
      Q[node,1]=-10
      Q[node,0]=10
    Share=[]
    Mis_info=[]
    for step in range(0, steps):
        # conduct the simulations
        Q,network,share,mis=dis_information(network,Q,alpha,w,b1,b2,mali_act_1,mali_act_0,c=0.2)
        Share.append(share)
        Mis_info.append(mis)
    # get the reuslts
    position=Q[:,1]>Q[:,0]
    dif=np.tanh(Q[:,1])-np.tanh(Q[:,0])
    modularity=nx.community.modularity(network,[set(np.array(network.nodes)[position==False]),set(np.array(network.nodes)[position])])
    nx.set_node_attributes(network, {node:dif[node] for node in network.nodes}, "Q_conviction")
    group_assortativity={}
    group_assortativity['0']=nx.numeric_assortativity_coefficient(network, "Q_conviction",nodes=list(set(np.array(network.nodes)[position==False])))
    group_assortativity['1']=nx.numeric_assortativity_coefficient(network, "Q_conviction",nodes=list(set(np.array(network.nodes)[position])))
    group_assortativity['all']=nx.numeric_assortativity_coefficient(network, "Q_conviction")
    degrees=[network.degree[i] for i in network.nodes]

    return Share,Mis_info,modularity,group_assortativity,position,degrees,mali_act_1,mali_act_0