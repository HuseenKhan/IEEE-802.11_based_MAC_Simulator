import numpy as np

class Buffer:
    def __init__(self):
        self.frames = [1]

    def has_frames(self):
        return len(self.frames) > 0

    def get_frame(self):
        return self.frames.pop(0)

    def add_frame(self):
        self.frames.append(1)

class WLANNode:
    CW_min = 0
    CW_max = 31

    def __init__(self, node_id, transmission_slots):
        self.node_id = node_id
        self.state = "DIFS"
        self.deffer = 5
        self.txop = 0
        self.successful_transmission = 0
        self.collision = 0
        self.retry = 0
        self.buffer = Buffer()
        self.CW_current = self.CW_max
        self.backoff_time = 0
        self.decrement_difs_count = 0
        self.slot_counter = 0
        self.channel_state = "Idle"
        self.transmission_slots = transmission_slots
        self.original_transmission_slots = transmission_slots
        self.frame_dropped = 0
        self.CST = -82
        self.sensing_nodes = []
        self.prev_channel_state = self.channel_state
        self.channel_energy = -95
        self.recive_energy = 0
        self.total_cw_used = 0

    def set_state(self, state):
        self.state = state

    def decrement_difs(self):
        if self.deffer > 0:
            self.deffer -= 1
            print(f"Node {self.node_id}: Performing DIFS {self.deffer}")
            if self.deffer == 0:
                self.decrement_difs_count += 1
                self.set_state("Perform carrier sense")
                self.generate_backoff()

    def set_backoff_time(self, time):
        self.backoff_time = time

    def generate_backoff(self):
        if self.state == "Perform carrier sense" and self.channel_state == "Idle" and self.backoff_time == 0:
            self.set_backoff_time(np.random.randint(self.CW_min, self.CW_current))
            self.total_cw_used += self.CW_current
            print(f"Node {self.node_id}: Generated backoff value: {self.backoff_time} time units")
            self.set_state("Backoff")
            if self.backoff_time == 0:
                self.txop += 1
                self.state = "Transmit"
        else:
            self.state = "Backoff"

    def decrement_backoff(self):
        if self.channel_state == "Idle" and self.state == "Backoff":
            self.slot_counter += 1
            if self.slot_counter == 2:
                if self.backoff_time > 0:
                    self.backoff_time -= 1
                    print(f"Node {self.node_id}: Backoff time remaining: {self.backoff_time} time units")
                self.slot_counter = 0
            if self.backoff_time == 0:
                self.txop += 1
                self.state = "Transmit"

            if self.channel_state == "Busy" and self.backoff_time != 0:
                print(
                    f"Node {self.node_id}: Channel is {self.channel_state}. Node {self.node_id}  pause decrementing backoff and waiting for channel to become idle...")

            if self.channel_state == "Busy" and self.backoff_time != 0:
                print(
                    f"Node {self.node_id}: Channel is {self.channel_state}. Node {self.node_id}  pause decrementing backoff and waiting for channel to become idle...")



    def drop_frame_and_reset(self):
        print(f"Node {self.node_id}: Frame dropped after 6 retries.")
        self.buffer.get_frame()
        self.CW_current = 31
        self.retry = 0

    def transmitting_frame(self, nodes, shared_channel_status):
        transmitting_nodes = [node for node in nodes if node.state == "Transmit"]
        if shared_channel_status == "Busy":
            self.slot_counter += 1
            print(
                f"Node {self.node_id}: Transmitting data... Remaining transmission slots: {self.transmission_slots}")
            if self.slot_counter == 2:
                if self.transmission_slots > 0:
                    self.transmission_slots -= 1
                self.slot_counter = 0
                print(
                    f"Node {self.node_id}: Transmitting data... Remaining transmission slots: {self.transmission_slots}")

            if self.transmission_slots == 0:
                if len(transmitting_nodes) > 1:
                    self.collision += 1
                    print(
                        f"Node {self.node_id}: Detected a possible collision with Node(s) {', '.join(str(node.node_id) for node in transmitting_nodes if node.node_id != self.node_id)}")
                    self.retry += 1
                    self.CW_current = (2 * self.CW_current) + 1
                    if self.retry >= 6:
                        self.frame_dropped += 1
                        self.drop_frame_and_reset()
                        self.buffer.add_frame()
                else:
                    self.successful_transmission += 1
                    self.buffer.get_frame()
                    self.buffer.add_frame()
                    self.CW_current = 31

                self.set_state("DIFS")
                self.deffer = 5
                self.transmission_slots = self.original_transmission_slots

    def update_channel_state(self, channel_energy):
        sensed_transmitting_nodes = [node for node in self.sensing_nodes if node.state == "Transmit"]
        if self.state == "Transmit":
            self.channel_state = "MAC Off"
        elif sensed_transmitting_nodes and self.CST < channel_energy:
            self.channel_state = "Busy"
        elif self.CST > channel_energy:
            self.channel_state = "Idle"

        if self.prev_channel_state in ["Busy", "MAC Off"] and self.channel_state == "Idle":
            self.set_state("DIFS")
            self.deffer = 5
        self.prev_channel_state = self.channel_state

    def set_sensing_nodes(self, nodes):
        self.sensing_nodes = nodes
