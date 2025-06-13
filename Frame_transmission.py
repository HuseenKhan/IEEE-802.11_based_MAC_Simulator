import numpy as np
shared_channel_status = "Idle"

"""
This Function is for the frame transmission. The transmission slots of a node depends on the
frame length. Once a node start transmission, it continune to decrements its transmission slots 
until transmission reaches to zero. If during the transmission, a length of transmission of transmitting node 
is greater than 1, that means node involved in Collision.
"""

def transmitting_frame(self, ):
    transmitting_nodes = []  # List to store nodes currently in "Transmit" state


    if self.state == "Transmit":
        transmitting_nodes.append(self)

    if shared_channel_status == "Busy":
        self.slot_counter += 1
        if self.slot_counter == 1:
            print(
                f"Node {self.node_id}: Transmitting its frame... Remaining transmission slots: {self.transmission_slots}")
        if self.slot_counter == 2:
            if self.transmission_slots > 0:
                self.transmission_slots -= 1
                self.transmission_count += 1
            self.slot_counter = 0
            print(
                f"Node {self.node_id}: Transmitting its frame... Remaining transmission slots: {self.transmission_slots}")

            if len(transmitting_nodes) > 1:  # More than one node transmitting at the same time, i.e., collision
                self.collision_occurred = True
                print(
                    f"Node {self.node_id}: involved in a collision with Node(s) {', '.join(str(node.node_id) for node in transmitting_nodes if node.node_id != self.node_id)}")

        if self.transmission_slots == 0:
            if self.collision_occurred:
                print(
                    f"Node {self.node_id}: Transmission failed due to collision")
                self.collision += 1
                self.collision_occurred = False
                self.retry += 1

                """
                When node involved in a collision, node double its CW size and retransmit 
                a frame. 
                """
                print(
                    f"Node {self.node_id} has {self.retry} retransmission")
                self.CW_current = (2 * self.CW_current) + 1
                print("The maximum contention window size is", self.CW_current)
                if self.retry >= 6:  # Drop the frame after 6 retries
                    """
                    When a node retransmission reaches to 6, a frame is drop. 
                    """

                    self.frame_dropped += 1
            else:
                print(f"Node {self.node_id}: Successfully transmit its frame")
                self.successful_transmission += 1
