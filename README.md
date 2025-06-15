# A Python-based channel access simulator for IEEE 802.11-based wireless networks

# Introduction

This simulator is wrritten in Python to understand the MAC mechansim of IEEE 802.11 based Wireless Network. The ultimate aim of this simulator is to implement the Spatial Reuse mechanism and to capture the operation of the MAC mechanism in each timeslot. This simulator allows different input parameters such as number of nodes, simulation area, minimum required SNR, frame length, simulation time and returns the following node parameters as the parimary results: 
Node transmission opportunities
Average collision rate 
Average CWmin per TXOP/Sucessful transmission
Average defer per TXOP/Suessful Transmission.

# Usage
To run the simulator, it is sufficient to run the `main.py` file. The `Simulation_setup.py` create the simulation scenario including number of nodes, frame length and time_slots (Simulation time). 
The sensing matrix is to decrale which node can sense who. 

```python
sensing_matrix = [
    [0, 1, 1],  # AP1 sense AP2 and AP3
    [1, 0, 1],  # AP2 sense AP1 and AP3
    [1, 1, 0],  # AP3 sense AP1 and AP2
]

# Assign sensing nodes to each node
for i in range(len(nodes)):
    sensing_nodes_for_i = [nodes[j] for j in range(len(nodes)) if sensing_matrix[i][j] == 1]
    nodes[i].set_sensing_nodes(sensing_nodes_for_i)





