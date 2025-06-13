import math
import random
num_nodes = 9
num_stas = 9
area_size = 25

"This define the number of APs, STAs and the area size. We have a grid scenario. Each side of square is 25 meter."

"Compute the AP and STA position in the network"
def generate_ap_and_sta_locations(num_nodes, num_stas, area_size):
    ap_locations = {}
    sta_locations = {}

    """The ap and sta dictionaries store the position of each ap indexed by their IDs"""
    rooms_per_side = int(math.sqrt(num_nodes))
    room_size = area_size / rooms_per_side
    sta_count = 0

    for ap_index in range(num_nodes):
        row, col = divmod(ap_index, rooms_per_side)

        """Calculate the center of each room to fixed the position of AP in each room."""
        x_center = (col + 0.5) * room_size
        y_center = (row + 0.5) * room_size
        ap_id = f"AP{ap_index + 1}"
        ap_locations[ap_id] = (x_center, y_center)

        # Place STAs around AP
        num_stas_per_ap = num_stas // num_nodes
        for _ in range(num_stas_per_ap):
            distance = random.uniform(0, room_size / 2)

            """Angle is for the random direction from the AP"""
            angle = random.uniform(0, 2 * math.pi)
            sta_x = x_center + distance * math.cos(angle)
            sta_y = y_center + distance * math.sin(angle)
            sta_id = f"STA{sta_count + 1}"
            sta_locations[sta_id] = (sta_x, sta_y)
            sta_count += 1

    return ap_locations, sta_locations, room_size