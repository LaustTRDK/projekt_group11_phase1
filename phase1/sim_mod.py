def init_state(drivers, requests, timeout, req_rate, width, height):
    """Initialize the simulation."""
    state = {
        "t": 0,
        "drivers": drivers,
        "pending": requests,   # vores requests bliver sat her
        "future": [],
        "served": 0,
        "expired": 0,
        "served_waits": [],
        "timeout": timeout,
        "req_rate": req_rate,
        "width": width,
        "height": height,
    }

    print("INIT: drivers =", len(drivers), "requests =", len(requests))
    return state


def simulate_step(state):
    """
    Simulates one step in time.

    Parameters
    ----------
    state : dict
        Contains the entire simulation state (drivers, requests, time, etc.)

    Returns
    -------
    state, metrics : tuple
        The updated simulation state and a metrics dictionary for the GUI.
    """

    # 1) Advance simulation time
    state["t"] += 1

    # 2) Move new requests from 'future' to 'pending'
    new_requests = []
    for req in state["future"]:
        if req["t"] <= state["t"]:
            state["pending"].append(req)
        else:
            new_requests.append(req)
    state["future"] = new_requests

    # 3) Remove expired requests
    active_requests = []
    for req in state["pending"]:
        wait_time = state["t"] - req["t"]
        if wait_time > state["timeout"]:
            state["expired"] += 1
            # Mark as expired (not kept in pending anymore)
            req["status"] = "expired"
        else:
            active_requests.append(req)
    state["pending"] = active_requests

    # 4) Find idle drivers (no active assignment)
    idle_drivers = []
    for driver in state["drivers"]:
        if driver.get("target_id") is None:
            idle_drivers.append(driver)

    # 5) Find waiting requests (no assigned driver yet)
    waiting_requests = []
    for req in state["pending"]:
        if req["status"] == "waiting" and req.get("driver_id") is None:
            waiting_requests.append(req)

    # 6) Match idle drivers with waiting requests
    # Match the first idle driver with the first waiting request, and so on.
    pairs_to_match = min(len(idle_drivers), len(waiting_requests))

    for i in range(pairs_to_match):
        driver = idle_drivers[i]
        req = waiting_requests[i]

        # Link them together
        driver["target_id"] = req["id"]
        req["driver_id"] = driver["id"]

        # The request is now assigned to a driver
        req["status"] = "assigned"

    # 7) Move drivers towards their current target and handle pickup/dropoff
    for driver in state["drivers"]:
        # Skip drivers that do not have an active assignment
        target_id = driver.get("target_id")
        if target_id is None:
            continue

        # Find the request this driver is serving
        current_request = None
        for req in state["pending"]:
            if req["id"] == target_id:
                current_request = req
                break

        # If the request no longer exists, free the driver and continue
        if current_request is None:
            driver["target_id"] = None
            continue

        # Decide which point the driver is heading towards
        if current_request["status"] in ("waiting", "assigned"):
            # Drive towards the pickup location
            target_x = current_request["px"]
            target_y = current_request["py"]
        elif current_request["status"] == "picked":
            # Drive towards the dropoff location
            target_x = current_request["dx"]
            target_y = current_request["dy"]
        else:
            # For delivered/expired requests, there is nothing to do
            driver["target_id"] = None
            continue

        # Compute direction from driver to target
        dx = target_x - driver["x"]
        dy = target_y - driver["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Safety: if already at the target, we just mark as reached
        if distance == 0:
            reached_target = True
        else:
            # Speed per time step (use default if missing)
            speed = driver.get("speed", 1.0)

            if distance <= speed:
                # The driver can reach the target in this step
                driver["x"] = target_x
                driver["y"] = target_y
                reached_target = True
            else:
                # Move one step towards the target
                driver["x"] += speed * dx / distance
                driver["y"] += speed * dy / distance
                reached_target = False

        # What happens when the driver reaches the target?
        if reached_target:
            if current_request["status"] in ("waiting", "assigned"):
                # The driver has picked up the order
                current_request["status"] = "picked"

            elif current_request["status"] == "picked":
                # The driver has delivered the order
                current_request["status"] = "delivered"
                state["served"] += 1

                # Record waiting time (example: from appearance to delivery)
                wait_time = state["t"] - current_request["t"]
                state["served_waits"].append(wait_time)

                # The driver is now free again
                driver["target_id"] = None

    # 8) Remove finished requests from 'pending'
    remaining_requests = []
    for req in state["pending"]:
        if req["status"] in ("waiting", "assigned", "picked"):
            # Still active in the system
            remaining_requests.append(req)
        # "delivered" and "expired" requests are dropped here
    state["pending"] = remaining_requests

    # 9) Compute average waiting time for metrics
    if state["served_waits"]:
        avg_wait = sum(state["served_waits"]) / len(state["served_waits"])
    else:
        avg_wait = 0.0

    # 10) Compute metrics for the GUI
    metrics = {
        "served": state["served"],
        "expired": state["expired"],
        "pending": len(state["pending"]),
        "t": state["t"],
        "avg_wait": avg_wait,
    }

    # 11) Return updated state and metrics
    return state, metrics


