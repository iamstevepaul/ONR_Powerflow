"""
In this file the sectionalizing and tie switch details are specified. 
Also the path for the DSS file containing the circuit information is specified.
The final DSS circuit which will be used by the environment is created.
"""

import os
import networkx as nx
import numpy as np
from  DSS_CircuitSetup import*
sectional_swt=[{'no':1,'line':'L25'},
               {'no':2,'line':'L17'},
               {'no':3,'line':'L30'},
               {'no':4,'line':'L14'},
               {'no':5,'line':'L13'}]

tie_swt=[{'no':1,'from node':'828','from conn':'.1.2.3', 'to node':'832','to conn':'.1.2.3', 'length':21,'code':'303', 'name':'L33'},
         {'no':2,'from node':'824','from conn':'.1.2.3','to node':'848','to conn':'.1.2.3','length':32,'code':'303', 'name':'L34'},
         {'no':3,'from node':'840','from conn':'.1.2.3','to node':'848','to conn':'.1.2.3','length':32,'code':'303', 'name':'L35'},
         {'no':4,'from node':'814','from conn':'.1.2.3','to node':'828','to conn':'.1.2.3','length':32,'code':'303', 'name':'L36'}]

switch_bus_map = np.array([
    [30,19],
    [21,22],
    [22,24],
    [16,17],
    [12,16],
    [16,19],
    [12,29],
    [25,29],
    [7,16]
])

mult_constant = 1.000000000
def initialize():
    FolderName=os.path.dirname(os.path.realpath("__file__"))
    DSSfile=r""+ FolderName+ "\ieee34Mod1.dss"
    DSSCktobj=CktModSetup(DSSfile,sectional_swt,tie_swt) # initially the sectionalizing switches close and tie switches open
    DSSCktobj.dssSolution.Solve() #solving snapshot power flows
    if DSSCktobj.dssSolution.Converged:
       conv_flag=1
    else:
       conv_flag=0
    G_init=graph_struct(DSSCktobj)
    return DSSCktobj,G_init,conv_flag

