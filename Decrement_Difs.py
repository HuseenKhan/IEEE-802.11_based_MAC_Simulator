def decrement_difs(self):
    """
    This function perform the DIFS. The Duration of DIFS in our simulator is
    50 us. So, the function decrement the deffer value for 5 time slots.
    When deffer value reaches to zero, node  generate backoff value.

    """
    if self.deffer > 0:
        self.deffer -= 1
        print(f"Node {self.node_id}: decrementing DIFS value {self.deffer}")

        if self.deffer == 0:
            self.deffer_count += 1 #Count How many times node Perform DIFS
            self.set_state("Perform carrier sense")
            self.generate_backoff()

