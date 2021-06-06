"""Contains tools which are useful, though not necessary, for EDDN event listening"""

from math import sqrt


def get3dDistance(locationA, locationB = [0.0, 0.0, 0.0]):
    """Evaluates the distance between a pair of three-dimensional coordinates (floats), the 2nd Parameter defaults to 0,0,0 (Sol)"""
    squareDist = 0
    
    for dimension in range (3):
        # Centre the coordinate
        locationA(dimension) -= locationB(dimension)

        # Sum of square of each dimension
        squareDist += locationA(dimension) ** 2

    distance = sqrt(squareDist)
    return distance
