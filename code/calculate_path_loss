def log_distance_path_loss(distance, d0=1, PL_d0=40.06, n=5.2):
    """
    Calculate path loss by adopting well-known Log-Distance Path Loss model.

    Parameters:
    - distance: Distance between transmitter and receiver in meters.
    - d0: Reference distance 
    - PL_d0: Path loss at the reference distance in dB.
    - n: Path loss value it define the carrier sensing range of a node. High loss value small carrier sensing range. 

  
    """
    if distance <= 0:
        raise ValueError("Distance must be greater than 0 meters.")
    return PL_d0 + 10 * n * np.log10(distance / d0)
