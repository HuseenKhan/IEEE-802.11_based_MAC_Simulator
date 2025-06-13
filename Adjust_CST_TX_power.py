
CST_MIN=-82 #Minimum CST in dBm
CST_MAX=-62 # Node Maximum CST value
TPC_MAX=20  # Node Maximum transmission Power in dBm
TPC_MIN=0   # Nose Minimum transmission Power in dBm
CST_current=CST_MIN
transmission_power_current=TPC_MAX



"""
This function determine the channel status. To determine that each node compare its current CST value with the 
power sensed by node
"""


def update_channel_state(self):
    # Set channel state based on CST values
    if self.CST_current > self.channel_energy:
        self.channel_state = "Idle"
    else:
        self.channel_state = "Busy"

    """ 
    We only consider the downlink traffic scenario. So, whenever a node sense the power with in the 
    range of CSTmin and CSTmax, a node consider that there is an opportunity for transmission and the current transmission
    is from different BSS. We assume there is no BSS color collision.

    """




def update_CST_TPC(self):
    """
    This function adjust the CST and TPC value of a node. Whenever a node sense another transmission, node
    increase its CST higher than the channel energy and decrease its transmission power with same proportion
    """

    if self.CST_MIN < self.channel_energy < self.CST_MAX:

        delta_value = min(self.channel_energy + 1 - self.CST_MIN, self.CST_MAX - self.CST_MIN)
        self.CST_current = self.CST_MIN + delta_value
        print("Node current CST value is".format(self.CST_current))
        self.transmission_power_current = max(self.TPC_MAX - delta_value, self.TPC_MIN)
        print("Node current TX power is value is".format(self.transmission_power_current))
    else:
        print("Do not change the CST and TX power of a node")