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



def load_requests(path) -> list[dict]: 
    """This function is ment to load request records from a file and return a lidt of request intitialized with default for missing field.

    The file added should contain a header as the top row. The information contained in the file should be in the order of:
    1) Request time - that is the time when the request will appear. This information must be in a increasing amount, becouse a customer can not request food back in time.
    2) x coordinat for the pickup of the request - the x coordinat in the grid for the driver to pick up the order.
    3) y coordinat for the pickup of the request - the y coordinat in the grid for the driver to pick up the order.
    4) x corrdinat for the delivery - the x coordinat in the grid for the the customer placement for delivery.
    5) y coordinat for the delivery - the y coordinat in the grid for the the customer placement for delivery.
    6) ******* måske waiting time. 

    None of the information can be negative and the coordinates value must be within the grids parameters that is width at 50.0 and hight at 30.0. 

    The request id will be added as the number of rows taken from the file. 
    """
    # Chek the whole document for negative numbers by seaching for "-"
    with open(path) as csvfil:
        for line in csvfil:
            if "-" in line:
                print("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                # system exit
    
    # Clean the full csv file into a list(list(float))
    count_id_full = 0
    full_clean_file : List[list[float]] = []
    with open(path) as csvfil:
        for row in csvfil:
            if count_id_full == 0:
                count_id_full += 1
                continue
            clean = [p.strip() for p in row.split(",")]
            clean_float = []
            for i in clean:
                if i.isdigit():
                    clean_float.append(float(i))
            full_clean_file.append(clean_float)
    
    # Check that the seperator in the file is indeed ",".
    with open(path, "r") as csvfile:
        for row in csvfile:
            # Validate that the file content, that the file information is seperated by ",".
            seperators = [";", " ", "\t", ",", ":"] # IF time make the test for others seperators work
            
            counts = {d: row.count(d) for d in seperators}
            if counts[","] > 0:
                continue
            else:
                print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                "system stop"
    
    # Check the csv file for that the right amount of information is precent in each row and that the coordiantes match that of the grid.
    count_id_gridchek = 1 # request ID counter
    for row in full_clean_file:
        no_info_row = len(row)
        if not no_info_row == 5 or no_info_row == 6: # Check how many values are in the row after conversion. There should be 5 or 6 values. Be aware that negative numbers will diapear and therefore trigger this check but any negative numbers should be found in previous checks.
                print(f"Error : Csv file rows have the incorrect number of values. Each row must contain either 5 or 6 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include, the error occured in row no. {count_id_gridchek}.")
                # system stop or call the function again
        if not (row[1] <= 50.0) and (row[3] <=50.0): # Chek tht the x coordinates (witch) from the file is not highter than the defould grid width (50.0)
            print(f"Error : An x coordinates that cooresponds to the placement in the grid width are highter than the max width. The error is to be found in the columns of x picup and/or x delivery. The error occured in row no. {count_id_gridchek}.") 
            # system stop
        if not (row[2] <=30.0) and (row[4] <= 30.0): # Chek tht the y coordinates (hight) from the file is not highter than the defould grid hight (30.0)
            print(f"Error : An y coordinate that coorespond to the placement in the grid hight are higher than the max hight. The error is to be found in the columns of y picup and/or y delivery. The error occured in row no. {count_id_gridchek}.")
        count_id_gridchek += 1
    
    # Chek that the column of the request time is indeed in an increasing value order. Becouse you can not place orders in the past.
    last_request_time = 0 # The last request time placeholder to compare to ensure that the request_time information is in a increasing order.
    for row in full_clean_file:
        if not (row[0] >= last_request_time):
            print("The request time (forst column) in the csv file is not in a increasing value order. Please correct the error before trying again")
            # system stop
        else:
            last_request_time = row[0]
    
    # Make the request list[dict] that is needed for the simulation
    requests : list[dict] = []
    count_id = 1
    for row in full_clean_file:
        """ "t_wait"
        if no_info_row == 6:
            the_t_wait = 
        else:
            the_t_wait = random.uniform(?????)""""Excercise set 5 funcktions.py"
        request = {
            "id" : count_id,
            "px" : row[1],
            "py" : row[2],
            "dx" : row[3],
            "dy" : row[4],
            "t" : int,
            #"t_wait" : ????,
            "status" : "waiting"
            "driver_id" : None
        }
        requests.append(request)
        count_id += 1
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
            "status" : "waiting"
            "driver_id" : None
        }

        out_list.append(request)