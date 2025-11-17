# phase1/io_mod.py
import csv
import random

def load_drivers(path) -> list[dict]:
    """
    This function will load drivers from a CSV file located at the specified path.

    If a file are used to load drivers from, the grid size will be with a gridth width at 50.0 and height at 30.0.

    Each dictionary contains the driver's x and y coordinates and nothing more than that, 
    it will return the list of drivers, with generated a 'speed' attribute for each driver, "target_id", "tx" and "ty".

    The user have to minimum provide the driver positions in the csv file. 
    The csv file have to be structured so that each row contain the following values:
    x-coordinate, y-coordinate, speed (optional).
    If speed is not provided it will be randomly generated between 0.5 and 3.0.

    The first value in a row will be read as the x–coordinate, 
    the second value as the y–coordinate, 
    and the third value (if it exists) will be read as the driver's speed.

    The information for each driver includes:
    - 'id': A unique integer identifier for the driver (from 0 to n–1), and generated as the file is read.
    - 'x': A float representing the driver's x-coordinate within the grid (0 to width). This is read from the file.
    - 'y': A float representing the driver's y-coordinate within the grid (0 to height). This is read from the file.
    - 'speed': A float representing the driver's speed.
    - 'tx': Initially set to None, representing the target x-coordinate, this is assigned later in the code.
    - 'ty': Initially set to None, representing the target y-coordinate, this is assigned later in the code.
    - 'target_id': Initially set to None, indicating no target assigned and is used by the code later on.
    """

    drivers: list[dict] = []
    count_id = 0     # Driver ID counter

    with open(path) as csvfil:
        for row in csvfil:
            row = row.strip()
            if not row:
                continue      # skip empty lines

            parts = [p.strip() for p in row.split(",")]

            # attempt to parse x,y — if this fails it's probably a header, so skip row
            try:
                x = float(parts[0])
                y = float(parts[1])
            except (ValueError, IndexError):
                continue

            # check number of values
            if len(parts) not in (2, 3):
                print(
                    "Csv file rows have the incorrect number of values. "
                    "Each row must contain either 2 or 3 values "
                    "(x, y, [speed])."
                )
                continue

            # read / handle speed
            if len(parts) == 3:
                try:
                    the_speed = float(parts[2])
                except ValueError:
                    the_speed = random.uniform(0.5, 3.0)
            else:
                the_speed = random.uniform(0.5, 3.0)

            # bounds-check for 50×30 grid
            if not (0 <= x <= 50.0) or not (0 <= y <= 30.0):
                print("Error: Coordinates for drivers are out of grid bounds.")
                continue

            driver = {
                "id": count_id,
                "x": x,
                "y": y,
                "speed": the_speed,
                "target_id": None,   # no target assigned yet
                "tx": None,          # set later
                "ty": None,
            }

            drivers.append(driver)
            count_id += 1

    return drivers



def load_requests(path: str) -> list[dict]:
    """Load request data from a CSV file with columns:
    time, pickup x, pickup y, delivery x, delivery y.
    """
    requests = []
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        req_id = 0
        for row in reader:
            # Skip empty lines
            if not row:
                continue

            # Skip header/comment line starting with '#'
            if row[0].startswith("#"):
                continue

            # Row format: time, px, py, dx, dy
            t = int(row[0])
            px = float(row[1])
            py = float(row[2])
            dx = float(row[3])
            dy = float(row[4])

            req = {
                "id": req_id,
                "px": px,
                "py": py,
                "dx": dx,
                "dy": dy,
                "t": t,
                "status": "waiting",
                "driver_id": None,
            }
            requests.append(req)
            req_id += 1

    return requests

def generate_drivers(n: int, width=None, height=None) -> list[dict]:
    """
    This function will create random drivers IDs and locations for the simulation.
    No. of drivers are represented by n. Width and height are the size of the grid.
    It will return a list of dictionaries with the drivers information.

    The information for each driver includes:
    - 'id': A unique integer identifier for the driver (from 0 to n-1).
    - 'x': A float representing the driver's x-coordinate within the grid (0 to width).
    - 'y': A float representing the driver's y-coordinate within the grid (0 to height).
    - 'speed': A float representing the driver's speed.

    If the grid size is not provided, it will default to a width of 50.0 and a height of 30.0.

    The project works with time in minutes. And the speed is the amount of units in the grid
    the driver can move per time unit:

    A slow driver has a speed between 0.5 and 1.0
    An average driver has a speed between 1.0 and 2.0
    A fast driver has a speed between 2.0 and 3.0

    >>> drivers = generate_drivers(3, 10, 10)
    >>> len(drivers)
    3
    >>> all(isinstance(driver, dict) for driver in drivers)
    True
    >>> all('id' in d and isinstance(d['id'], int) for d in drivers)
    True
    >>> all('x' in d and isinstance(d['x'], float) for d in drivers)
    True
    >>> all('y' in d and isinstance(d['y'], float) for d in drivers)
    True
    >>> all('speed' in d and isinstance(d['speed'], float) for d in drivers)
    True
    >>> all(0.5 <= d['speed'] <= 3.0 for d in drivers)
    True
    """

    # Defaults if no width/height provided
    width = 50.0 if width is None else float(width)
    height = 30.0 if height is None else float(height)

    drivers = []

    for i in range(n):
        driver = {
            "id": i,
            "x": random.uniform(0, width),
            "y": random.uniform(0, height),
            "speed": random.uniform(0.5, 3.0),
            "target_id": None,
            "tx": None,
            "ty": None
        }
        drivers.append(driver)

    return drivers

def generate_requests(start_t: int, out_list: list[dict],
                      req_rate: float, width: int, height: int) -> None:
    """Generate new random requests (placeholder version)."""
    # For now, we don’t actually generate new requests dynamically
    # You can expand this later if needed.
    return None