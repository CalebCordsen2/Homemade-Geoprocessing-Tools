import arcpy
from arcpy import env
import math
import numpy as np
import os


polygons = []
polygonBoundary = []
inputFile = r'C:/Users/caleb/GEOG 4303/CordsenCalebFinalProject/Test Data/boulder_city.shp'
with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
    for row in SearchCursor:
        polygons.append(row[0])
        polygonBoundary.append(row[0].boundary())
del SearchCursor