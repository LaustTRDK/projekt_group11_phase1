# MODULE_NAME
"""This is the module

There will be a vararity of functions made for the phase 1 of the project. 

Functions that are a part of the assigment: 
- load_drivers
- load_requests
- generate_drivers
- generate_requests
"""
# Programmer at der skal kunne tilgås
from typing import List
import random
import numpy
import sys

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

def load_drivers(list_name: list[dict]) -> list[dict]:
    """ This function will load drivers from a list of dictionaries, that is created by the function 'generate drivers'.

    Each dictionary contains the driver's ID, x and y coordinates, and speed.
    It will return the list of drivers. 
    The information for each driver includes:
    - 'id': A unique integer identifier for the driver (from 0 to n-1).
    - 'x': A float representing the driver's x-coordinate within the grid (0 to width).
    - 'y': A float representing the driver's y-coordinate within the grid (0 to height).
    - 'speed': A float representing the driver's speed.
    """
    return list_name

# Dockstring test
if __name__ == "__main__":
    import doctest
    doctest.testmod()