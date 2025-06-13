import numpy as np


""""
Here we write a function to generate a node backoff value and 
node decrement its backoff value in each time slot if the 
channel is IDLE. 
"""

def backoff_time(self, time):
    self.backoff_time = time


def generate_backoff(self):
    if self.state == "Perform carrier sense" and self.channel_state == "Idle" and self.backoff_time == 0:
        self.set_backoff_time(np.random.randint(self.CW_min, self.CW_current))
        print(f"Node {self.node_id}: Generated backoff value: {self.backoff_time} time units")
    else:
        self.state = "Backoff"
        print(f"Node {self.node_id}: backoff value: {self.backoff_time} time units")




def decrement_backoff(self):
    if self.channel_state == "Idle" and self.state == "Backoff":
        self.slot_counter += 1
        if self.slot_counter == 1:
            print(f"Node {self.node_id}: Backoff time remaining: {self.backoff_time} time units")
        if self.slot_counter == 2:
            if self.backoff_time > 0:
                self.backoff_time -= 1
            self.slot_counter = 0

            print(f"Node {self.node_id}: Backoff time remaining: {self.backoff_time} time units")
        """
        When node backoff time reach to zero, node win the transmission opportunity. 
        """
        if self.backoff_time == 0:
            self.txop += 1

        """
        If node sense channel is busy and its backoff time not reach to zero
        node stop decrement its backoff value. 
        """

        if self.channel_state == "Busy" and self.backoff_time != 0:
            print(
                f"Node {self.node_id}: Channel is {self.channel_state}. Node {self.node_id}  pause decrementing backoff and waiting for channel to become idle...")
