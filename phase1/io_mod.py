    # MODULE_NAME
"""This is the module

There will be a vararity of functions made for the phase 1 of the project. 

Functions that are a part of the assigment: 
- generate_drivers
- load_drivers
- generate_requests
- load_requests

This module is created for the purpose of handling input operations related to drivers and requests in a simulation. Both the generation of random drivers and requests as reading a csv file for optaining drivers and requests information. 
"""
# Programmer at der skal kunne tilgås
from typing import List
import random
import numpy

# Generate drivers: 
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

    width = 50.0 if width is None else float(width) # There is a defould width if not any other is given. 
    height = 30.0 if height is None else float(height) # There is a defould hight if not any other is given. 
    
    for i in range(n):
        driver = {
            "id": i,
            "x": random.uniform(0, width), # returns a random float between 0 and width
            "y": random.uniform(0, height), # returns a random float between 0 and height
            "speed": random.uniform(0.5, 3.0), # returns a random float between 0.5 and 3.0
            "target_id": None, # initially no target assigned 
            "tx": None, # target x coordinate
            "ty": None # target y coordinate
        }
        drivers.append(driver)
        
    return drivers

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
                raise ValueError("Error: Inconsistent separator found in file. You may have used the wrong file.")
                #print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                #"""system stop"""
    
    # Validate that there is no negative values in the file.
    with open(path) as csvfil:
        for line in csvfil:
            if "-" in line:
                raise ValueError("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                #print("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                # system exit

    drivers : list[dict]= []
    count_id = 0 # Driver ID counter
    with open(path) as csvfil:
        for row in csvfil:
            # Clean the file
            if count_id == 0: # Skip the header / first row
                count_id += 1 # Count the number of drivers by counting the rows in the file.
                continue
            clean = [p.strip() for p in row.split(",")] # Remove any leading/trailing whitespace or newline characters
            
            # Convert the string values into float values if they are digits. 
            parts_float  = [] # List to hold the converted float values from the row
            for i in clean: # Convert each part to float if it is a digit
                if i.isdigit():
                    parts_float.append(float(i))

            # Validate the number of values in each row after conversion to float. There should eighter be 2 or 3 values. 
            no_info_row = len(parts_float) # Count the number of values in the row after conversion to float.
            if not no_info_row == 2 or no_info_row == 3: # Check how many values are in the row after conversion. There should be 2 or 3 values. 
                raise ValueError("Error : Csv file rows have the incorrect number of values. Each row must contain either 2 or 3 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include.")
                # print("Error : Csv file rows have the incorrect number of values. Each row must contain either 2 or 3 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include.")
                # """sys.exit(1)""" # Exit the program if the row does not have the correct number of values.
            
            # Check if the coordiantes are within the grid bounds.
            x = parts_float[0]
            y = parts_float[1]
            if not (0 <= x <= 50.0) or not (0 <= y <= 30.0):
                raise ValueError("Error : Coordinates for drivers are out of grid bounds.")
                # print("Error : Coordinates for drivers are out of grid bounds.")
                # """system stop"""
            
            # Create the driver dictionary
            if no_info_row == 3:
                the_speed = parts_float[2] # If speed is provided then use it.
            else:
                the_speed = random.uniform(0.5, 3.0) # If speed is not provided use a random speed between 0.5 and 3.0
            driver = {
                "id": count_id,
                "x": parts_float[0], # Takes the first value as x-coordinate
                "y": parts_float[1], # Takes the second value as y-coordinate
                "speed": the_speed, # returns a random float between 0.5 and 3.0
                "target_id": None, # initially no target assigned 
                "tx": None, # target coordinates
                "ty": None # target coordinates
            }
            drivers.append(driver)
    return drivers

def generate_requests(start_t : int, out_list : list, req_rate : float, width = 50, height = 30) -> None:
    """This function will generate request to the simulation acording to the request rate. This uses the Poisson distribution to determine the number of requests to generate at each time step.
    The generated requests will be appended to the provided output list (out_list).
    Each request is represented as a dictionary with the following keys:
    - 'id': A unique integer identifier for the request.
    - 'px': A float representing the pickup x-coordinate within the grid (0 to width
    - 'py': A float representing the pickup y-coordinate within the grid (0 to height).
    - 'dx': A float representing the delivery x-coordinate within the grid (0 to width).
    - 'dy': A float representing the delivery y-coordinate within the grid (0 to height).
    - 't': An integer representing the request time (start_t).
    - 'status': A string representing the request status, initially set to "waiting".
    - 'driver_id': Initially set to None, indicating no driver assigned.
    The grid size can be adjusted by changing the width and height parameters. If not provided, they default to 50 and 30, respectively.

    The request rate is the average requests pr. minute that have to be generated. It will genereate the requests at a given rate and sendt it to output list that will be read and used by the simulation.
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
    width = 50.0 if width is None else float(width) # There is a defould width if not any other is given. 
    height = 30.0 if height is None else float(height) # There is a defould hight if not any other is given.

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

        request = {
            "id" : new_id,
            "px" : px,
            "py" : py,
            "dx" : dx,
            "dy" : dy,
            "t" : start_t,
            "status" : "waiting",
            "driver_id" : None
        }

        out_list.append(request)


def load_requests(path) -> list[dict]: 
    """This function is ment to load request records from a file and return a lidt of request intitialized with default for missing field.

    The file added should contain a header as the top row. The information contained in the file should be in the order of:
    1) Request time - that is the time when the request will appear. This information must be in a increasing amount, becouse a customer can not request food back in time.
    2) x coordinat for the pickup of the request - the x coordinat in the grid for the driver to pick up the order.
    3) y coordinat for the pickup of the request - the y coordinat in the grid for the driver to pick up the order.
    4) x corrdinat for the delivery - the x coordinat in the grid for the the customer placement for delivery.
    5) y coordinat for the delivery - the y coordinat in the grid for the the customer placement for delivery.

    None of the information can be a negativevalue and the coordinates value must be within the grids parameters that is width at 50.0 and hight at 30.0. 

    The request id will be added as the number of rows taken from the file.'
    Each dictionary contains the request's pickup and delivery coordinates, request time, status, and driver ID.
    
    >>> request_list = []
    >>> testingeeee = "/Users/melan/OneDrive/Dokumenter/SDU/Kandidat/1 Semester/DM857 introduktion til programering/Project/projekt_group11_phase1-main/data/requests.csv"
    >>> load_requests(testingeeee)
    >>> all('id' in d isinstance('id', int) for d in request_list)
    True
    >>> all('px' in d and 0.0 <= d['px'] <= 50.0 for d in request_list)
    True
    """
    # Chek the whole document for negative numbers by seaching for "-"
    with open(path) as csvfil:
        for line in csvfil:
            if "-" in line:
                raise ValueError("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                #print("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
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
                raise ValueError("Error: Inconsistent separator found in file. You may have used the wrong file.")
                # print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                "system stop"
    
    # Check the csv file for that the right amount of information is precent in each row and that the coordiantes match that of the grid.
    count_id_gridchek = 1 # request ID counter
    for row in full_clean_file:
        no_info_row = len(row)
        if not no_info_row == 5 or no_info_row == 6: # Check how many values are in the row after conversion. There should be 5 or 6 values. Be aware that negative numbers will diapear and therefore trigger this check but any negative numbers should be found in previous checks.
            raise ValueError(f"Error : Csv file rows have the incorrect number of values. Each row must contain either 5 or 6 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include, the error occured in row no. {count_id_gridchek}.")
                # print(f"Error : Csv file rows have the incorrect number of values. Each row must contain either 5 or 6 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include, the error occured in row no. {count_id_gridchek}.")
                # system stop or call the function again
        if not (row[1] <= 50.0) and (row[3] <=50.0): # Chek tht the x coordinates (witch) from the file is not highter than the defould grid width (50.0)
            raise ValueError(f"Error : An x coordinates that cooresponds to the placement in the grid width are highter than the max width. The error is to be found in the columns of x picup and/or x delivery. The error occured in row no. {count_id_gridchek}.")
            #print(f"Error : An x coordinates that cooresponds to the placement in the grid width are highter than the max width. The error is to be found in the columns of x picup and/or x delivery. The error occured in row no. {count_id_gridchek}.") 
            # system stop
        if not (row[2] <=30.0) and (row[4] <= 30.0): # Chek tht the y coordinates (hight) from the file is not highter than the defould grid hight (30.0)
            raise ValueError(f"Error : An y coordinate that coorespond to the placement in the grid hight are higher than the max hight. The error is to be found in the columns of y picup and/or y delivery. The error occured in row no. {count_id_gridchek}.")
            # print(f"Error : An y coordinate that coorespond to the placement in the grid hight are higher than the max hight. The error is to be found in the columns of y picup and/or y delivery. The error occured in row no. {count_id_gridchek}.")
        count_id_gridchek += 1
    
    # Chek that the column of the request time is indeed in an increasing value order. Becouse you can not place orders in the past.
    last_request_time = 0 # The last request time placeholder to compare to ensure that the request_time information is in a increasing order.
    for row in full_clean_file:
        if not (row[0] >= last_request_time):
            raise ValueError("The request time (forst column) in the csv file is not in a increasing value order. Please correct the error before trying again")
            # print("The request time (forst column) in the csv file is not in a increasing value order. Please correct the error before trying again")
            # system stop
        else:
            last_request_time = row[0]
    
    # Make the request list[dict] that is needed for the simulation
    requests : list[dict] = []
    count_id = 1
    for row in full_clean_file:
        request = {
            "id" : count_id,
            "px" : row[1],
            "py" : row[2],
            "dx" : row[3],
            "dy" : row[4],
            "t" : int(row[0]),
            "status" : "waiting",
            "driver_id" : None
        }
        requests.append(request)
        count_id += 1
    return requests

# Dockstring test
if __name__ == "__main__":
    import doctest
    doctest.testmod()