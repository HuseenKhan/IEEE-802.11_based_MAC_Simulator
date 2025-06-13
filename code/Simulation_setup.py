from CSMA_CA_Simulator import WLANNode

channel_energy = -100
shared_channel_status = "Idle"

# Node IDs and creation
node_ids = [f"AP{i}" for i in range(1, 4)]  # Creates ['AP1', 'AP2', 'AP3']
nodes = [WLANNode(node_id, 21) for node_id in node_ids]

"""
This is a sensing matrix. The size of matrix depends on the 
number of nodes.If there 4 nodes, the size is 4 x 4 and so 
on. 1 represent node can sense, 0 represent node cannot sense
"""

sensing_matrix = [
    [0, 1, 1],  # AP1 sense AP2 and AP3
    [1, 0, 1],  # AP2 sense AP1 and AP3
    [1, 1, 0],  # AP3 sense AP1 and AP2
]

# Assign sensing nodes to each node
for i in range(len(nodes)):
    sensing_nodes_for_i = [nodes[j] for j in range(len(nodes)) if sensing_matrix[i][j] == 1]
    nodes[i].set_sensing_nodes(sensing_nodes_for_i)

"""
time_slots is the simulation time. 
"""
time_slots = 100000
