"""Contains functions common to several libraries"""

from math import sqrt
import datetime
import re as regex
import csv


def get3dDistance(locationA, locationB = [0.0, 0.0, 0.0]):
    """Evaluates the distance between a pair of 3d coordinates (floats), the 2nd Parameter defaults to 0,0,0 (Sol)"""
    squareDist = 0
    
    for dimension in range (3):
        # Centre the coordinate
        locationA[dimension] -= locationB[dimension]

        # Sum of square of each dimension
        squareDist += locationA[dimension] ** 2

    distance = sqrt(squareDist)
    return distance

def formatTimestamp(rawTimestamp):
    regexPattern = r"(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
    
    cleanTimestampArr = regex.split(regexPattern, rawTimestamp)
    dateTimeString = cleanTimestampArr[1] + " " + cleanTimestampArr[2] + ".000000"
    cleanTimeStamp = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')
    return cleanTimeStamp

def systemListFromCSV(fileName, sysNameColumn):
    """Takes the path of a CSV file and returns a list of system name strings given their column number (index is from zero)."""
    systemList = []
    rowCount = 0
    with open(fileName, newline='') as inputcsv:
        reader = csv.reader(inputcsv, delimiter=',', quotechar='"')
        for row in reader:
            systemList.append(row[sysNameColumn])
            rowCount += 1
    print("System entries = {0}".format(rowCount))
    return systemList

def compareLists(listA: list, listB: list, strict: bool):
    """Takes two lists and a strictness parameter, checks for any matches if not strict and checks for exact matches if strict."""
    matches = 0
    if listA == None or listB == None:
        return False

    for a in listA:
        if a in listB:
            matches += 1

    if strict == True and matches == len(listB):
        return True
    if strict == False and matches >= len(listB):
        return True
    return False
