# phase1/io_mod.py
import csv
import random

def load_requests(filename):
    """
    Loads all requests from a CSV file.

    Each request contains information such as:
    - id
    - t (time when the request appears)
    - pickup_x, pickup_y
    - dropoff_x, dropoff_y

    Returns
    -------
    requests : list of dict
        Each dict represents a single request.
    """

    requests = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            req = {
                "id": int(row["id"]),
                "t": int(row["t"]),
                "pickup_x": int(row["pickup_x"]),
                "pickup_y": int(row["pickup_y"]),
                "dropoff_x": int(row["dropoff_x"]),
                "dropoff_y": int(row["dropoff_y"]),
                "status": "waiting",
                "driver_id": None
            }
            requests.append(req)

    return requests



def load_drivers(path) -> list[dict]:
    """ This function will load drivers from a CSV file located at the specified path. 

    If a file are used to load drivers from, the grid size will be with a gridth width at 50.0 and height at 30.0. 

    Each dictionary contains the driver's x and y coordinates and nothing more than that, the driver "IDs" will be generated as pr row in the file. 
    It will return the list of drivers, with generated a 'speed' attribute for each driver, "target_id", "tx" and "ty".

    The user have to minimum provide the driver positions in the csv file. The csv file have to be structured so that each row contains information in the specefic order of: 
    x-coordinate, y-coordinate, speed (optional). 
    If speed is not provided it will be randomly generated between 0.5 and 3.0.

    The first value in a row will be read as the x-coordinate, the second value as the y-coordinate, and the third value (if present) as the speed.


    The information for each driver includes:
    - 'id': A unique integer identifier for the driver (from 0 to n-1), and generated as the file is read.
    - 'x': A float representing the driver's x-coordinate within the grid (0 to width). This is read from the file.
    - 'y': A float representing the driver's y-coordinate within the grid (0 to height). This is read from the file.
    - 'speed': A float representing the driver's speed. This is randomly generated for each driver. 
    - 'tx': Initially set to float, representing the target x-coordinate, this is assigned later in the code.
    - 'ty': Initially set to float, representing the target y-coordinate, this is assigned later in the code.
    - 'target_id': Initially set to None, indicating no target assigned and is used by the code later on.
    """
    with open(path) as csvfil:
        for row in csvfil:
            # Validate the file content, is the file seperated by ",".
            seperators = [";", " ", "\t", ",", ":"]
            counts = {d: row.count(d) for d in seperators}

            if counts[","] > 0:
                continue
            else:
                print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                #"""system stop"""

    drivers : list[dict]= []
    count_id = 0 # Driver ID counter
    with open(path) as csvfil:
        for row in csvfil:
            # Clean the file
            if count_id == 0: # Skip the header / first row
                count_id += 1 # Count the number of drivers by counting the rows in the file.
                continue
            parts = row.split(",") # Split the row into parts based on commas
            clean = [p.strip() for p in row.split(",")] # Remove any leading/trailing whitespace or newline characters
            
            # Convert the string values into float values if they are digits. 
            parts_float  = [] # List to hold the converted float values from the row
            for i in clean: # Convert each part to float if it is a digit
                if i.isdigit():
                    parts_float.append(float(i))

            # Validate the number of values in each row after conversion to float. There should eighter be 2 or 3 values. 
            no_info_row = len(parts_float) # Count the number of values in the row after conversion to float.
            if not no_info_row == 2 or no_info_row == 3: # Check how many values are in the row after conversion. There should be 2 or 3 values. 
                print("Csv file rows have the incorrect number of values. Each row must contain either 2 or 3 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include.")
                # """sys.exit(1)""" # Exit the program if the row does not have the correct number of values.
            
            # Check if the coordiantes are within the grid bounds.
            x = parts_float[0]
            y = parts_float[1]
            if not (0 <= x <= 50.0) or not (0 <= y <= 30.0):
                print("Error : Coordinates for drivers are out of grid bounds.")
                """system stop"""
            
            # Create the driver dictionary
            if no_info_row == 3:
                the_speed = parts_float[2] # If speed is provided then use it.
            else:
                the_speed = random.uniform(0.5, 3.0) # If speed is not provided use a random speed between 0.5 and 3.0
            driver = {
                "id": count_id,
                "x": parts_float[0], # Takes the first value as x-coordinate
                "y": parts_float[1], # Takes the second value as y-coordinate
                "speed": the_speed # returns a random float between 0.5 and 3.0
                "target_id": None # initially no target assigned 
                "tx": float, "ty": float # target coordinates
            }
            drivers.append(driver)
    return drivers

def generate_drivers(n: int, width=None, height=None) -> list[dict]:
    """This function will create random drivers IDs and locations for the simulation. 
    No. of drivers, are reprecented by n. Width and height are the size of the grid.
    it will return a list of dictionaries with the drivers information.

    The information for each driver includes:
    - 'id': A unique integer identifier for the driver (from 0 to n-1).
    - 'x': A float representing the driver's x-coordinate within the grid (0 to width).
    - 'y': A float representing the driver's y-coordinate within the grid (0 to height).
    - 'speed': A float representing the driver's speed.

    If the gridt size is not provided, it will default to a width of 50.0 and a height of 30.0.
    
    The project works with time in minutes. And the speed is the amount of units in the grid the driver can move pr. time unit'
    A slow driver has a speed between 0.5 and 1.0 grid units pr. time unit.
    A average driver has a speed between 1.0 and 2.0 grid units pr. time unit.
    A fast driver has a speed between 2.0 and 3.0 grid units pr. time unit.

    Mangler docktest for "target_id", "tx" og "ty". !!!!!!!!


    >>> drivers = generate_drivers(3, 10, 10)
    >>> len(drivers)
    3
    >>> all(isinstance(driver, dict) for driver in drivers) # Does the list only include dictoryties? 
    True
    >>> all('id' in d and isinstance(d['id'], int) for d in drivers)
    True
    >>> all('x' in d and isinstance(d['x'], float) for d in drivers) # is all x a float and between 0 and width?
    True
    >>> all('y' in d and isinstance(d['y'], float) for d in drivers) # is all y a float and between 0 and height?
    True
    >>> all('speed' in d and isinstance(d['speed'], float) for d in drivers) # is all speed a float
    True
    >>> all('speed' in d and 0.5 <= d['speed'] <= 3.0 for d in drivers) # is all speed between 0.5 and 3.0?
    True
    """
    drivers: list[dict] = []

    if width is None: # Default width if none is given to be 50, else the provided width is used.
        width = 50.0 # default width
    else:
        width = float(width)
    
    if height is None: # Default height if none is given to be 30, else the provided height is used. 
        height = 30.0 # default height
    else:
        height = float(height)
    
    for i in range(n):
        driver = {
            "id": i,
            "x": random.uniform(0, width), # returns a random float between 0 and width
            "y": random.uniform(0, height), # returns a random float between 0 and height
            "speed": random.uniform(0.5, 3.0) # returns a random float between 0.5 and 3.0
            "target_id": None # initially no target assigned 
            "tx": float, "ty": float # target coordinates
        }
        drivers.append(driver)
    return drivers


def generate_requests(start_t : int, out_list : list, req_rate : float, width = 50, height = 30) -> None:
    """This function will generate request to the simulation acording to the request rate.
    The request rate is the average requests pr. minute that have to be generated
    >>> request_list = []
    >>> generate_requests(0, request_list, 2.0)
    >>> isinstance(request_list, list)
    True
    >>> all("px" in p and isinstance(p["px"], float) for p in request_list)
    True
    >>> all("py" in p and isinstance(p["py"], float) for p in request_list)
    True
    >>> all("dy" in p and isinstance(p["dy"], float) for p in request_list)
    True
    >>> all("dx" in p and isinstance(p["dx"], float) for p in request_list)
    True
    """
    # The main part of the function to generate random numbers
    poissdist = numpy.random.poisson(req_rate)
    # Poisson distribution is commonly used for modeling the number of events occurring in a fixed time period when events happen independently at a constant average rate.

    # Making the width and height something that you can change and if not prowided then the defould is width = 50 and height = 30

    for _ in range(poissdist):
        # _ means that the value in poissdist is not important. Becouse it is random generated with the request rate. 
        # now it also have to make an request ID for the new genereated requests. 
        ## All request ID is from 1 to infinitive, using the len(out_list) then the length of the list is also counting 0 
        ## so therefore the new ID that is not used yet match the counting of the length og the out_list. 
        new_id = len(out_list)
        px = random.uniform(0, width)
        py = random.uniform(0, height)
        dx = random.uniform(0, width)
        dy = random.uniform(0, height)
        # t_wait = ????

        request = {
            "id" : new_id,
            "px" : px,
            "py" : py,
            "dx" : dx,
            "dy" : dy,
            "t" : start_t
            #"t_wait" : t_wait,
            #"status" : "waiting"
            #"driver_id" : None
        }

        out_list.append(request)
