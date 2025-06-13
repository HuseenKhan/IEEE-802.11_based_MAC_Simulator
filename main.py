from Simulation_setup import nodes, node_ids, time_slots
import pandas as pd

channel_energy = -100
shared_channel_status = "Idle"


"""
Channel energy value is just dummy values. the channel is either IDLE 
or BUSY. When channel is BUSY , the channel energy is higher than node CST if node is
in the carrier sensing range of transmiiting node (which depends on the sensing matrix). 

Note that in  model we define the AP and STA location (AP_STA) the 
channel energy depends on the distance between the nodes 
and the path loss model. 
"""

# Simulation loop
for slot in range(1, time_slots):
    print(f"\nTime Slot: {slot}")
    shared_channel_status = "Busy" if any(n.state == "Transmit" for n in nodes) else "Idle"
    channel_energy = -40 if shared_channel_status == "Busy" else -100

    for node in nodes:
        node.update_channel_state(channel_energy)
        print(f"Node {node.node_id} Channel State: {node.channel_state}")

    for node in nodes:
        if node.state == "DIFS":
            node.decrement_difs()
        elif node.state == "Perform carrier sense":
            node.generate_backoff()
        elif node.state == "Backoff":
            node.decrement_backoff()
        elif node.state == "Transmit":
            node.transmitting_frame(nodes, shared_channel_status)

summary_data = {

    "Total TXOP": [int(n.txop) for n in nodes],
    "Successful TX": [int(n.successful_transmission) for n in nodes],
    "Total Collisions": [int(n.collision) for n in nodes],
    "Number of times node Defer": [int(n.decrement_difs_count) for n in nodes],
    "Avg CWmin per TXOP": [round(n.total_cw_used / n.txop, 2) if n.txop else 0 for n in nodes],
    "Avg defer per TXOP": [round(n.decrement_difs_count / n.txop, 2) if n.txop else 0 for n in nodes],
    "Avg CWmin per Successful TX": [round(n.total_cw_used / n.successful_transmission, 2) if n.successful_transmission else 0 for n in nodes],
    "Avg defer per Successful TX": [round(n.decrement_difs_count / n.successful_transmission, 2) if n.successful_transmission else 0 for n in nodes],
    "Average Collision Rate": [round(n.collision / n.txop, 2) if n.txop else 0 for n in nodes],
}

df_summary = pd.DataFrame(summary_data).T
df_summary.columns = node_ids

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("\n--- MAC Simulation Summary (Parameters as Rows) ---\n")
print(df_summary)
