"""
Author: Caleb Cordsen
Date: 4/29/2023

Description: This file contains the functions that help make the clip function work!
"""
# Import necessary things
import arcpy
from arcpy import env
import math
import numpy as np
import os
import signal
import time


def clip(returnDir,outputName, inputFile, clipFile):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created clip file to.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted clip shape file.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid shape file that 
        you wish to use as your input features for the clip
    clipFile: This should be a string representing a file path.
        This should be a string representing a file path that points to a valid shape file that
        you wish to use your clip feature for the clip.
    
    
    Returns
    -------
    str
        This function returns a string representing a message on whether the clip executed or not.
        
    Description
    -----------
    The clip function emulates a classic clip that one sees in GIS software. The logic varies according to 
    input geometry but there are essentially six kinds of clips based on geometry. There is a 
    POINTPOINT clip, POINTLINE clip, POINTPOLYGON clip, LINELINE clip, LINEPOLYGON clip, and POLYGONPOLYGON clip. 
    Though they all require different implementations to be done, the underlying idea is the same: extract
    from the input feature the geometry that exists within the clip feature. This function will detect the inputted
    geometry and then proceed from there.
    '''
    
    
    # Add back in try and except
        
    # Get the input coordinate system and the two geometry types
    inputGeo = arcpy.Describe(inputFile).shapeType.upper()
    clipGEO = arcpy.Describe(clipFile).shapeType.upper()
    inputCoordinateSystem = arcpy.Describe(inputFile).spatialReference
    # Delete output file if they exist
    if (os.path.exists(os.path.join(returnDir,outputName))):
        arcpy.management.Delete(os.path.join(returnDir,outputName))
    
    #-------------------------------------------------------------------------------------------------------------
    # Check if both geometries are points
    if(inputGeo == "POINT" and clipGEO == "POINT"):
        # Create an empty list to store point geometries in 
        inputPoints = []
        # Open search cursor on input features
        with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                # Add to list point geometries
                inputPoints.append(row[0])
        # Do the same process on the clip feature
        clipPoints = []
        with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                clipPoints.append(row[0])
        # Create an empty list of output points
        outputPoints = []
        # Loop through input feature points
        for point in inputPoints:
            # If the current point exists in the clip feature append that point to outputPoints
            if point in clipPoints:
                outputPoints.append(point)
        # Create output file
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POINT',spatial_reference=inputCoordinateSystem)
        # Open an insert cursor on the output shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            # Add to output the output points and then return success message
            for point in outputPoints:
                iCursor.insertRow(point)
        return "The clip was successful!"
    # ------------------------------------------------------------------------------------------------------------            
    elif(inputGeo == "POINT" and clipGEO == "POLYLINE"):
        # Create an empty list to store point geometries in 
        inputPoints = []
        # Open search cursor on input features
        with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                # Add to list point geometries
                inputPoints.append(row[0])
        # Do the same process on the clip feature, adding the clip lines
        clipLines = []
        with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                clipLines.append(row[0])
        # Create an empty list of output points
        outputPoints = []
        # Loop through input feature points
        for point in inputPoints:
           # Loop through the lines in the clip feature
           for line in clipLines:
               # If the point is within the line, I.E. is on the line add it to the outputPoints
               if (point.within(line)):
                   outputPoints.append(point)
        # Create output file
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POINT',spatial_reference=inputCoordinateSystem)
        # Open an insert cursor on the output shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            # Add to output the output points and then return success message
            for point in outputPoints:
                iCursor.insertRow(point)
        return "The clip was successful!"
    # --------------------------------------------------------------------------------------------------------------
    elif(inputGeo == "POINT" and clipGEO == "POLYGON"):
        # Create an empty list to store point geometries in 
        inputPoints = []
        # Open search cursor on input features
        with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                # Add to list point geometries
                inputPoints.append(row[0])
        # Do the same process on the clip feature, adding the clip polygons
        clipPolygons = []
        with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
            for row in SearchCursor:
                clipPolygons.append(row[0])
        # Create an empty list of output points
        outputPoints = []
        # Loop through input feature points
        for point in inputPoints:
           # Loop through the polygons in the clip feature
           for poly in clipPolygons:
               # If the point is within the polygon, I.E. its inside of the polygon or if its
               # within the polygon's polyline boundary I.E. its on the boundary add it to output Points
               if (point.within(poly) or point.within(poly.boundary())):
                   outputPoints.append(point)
        # Create output file
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POINT',spatial_reference=inputCoordinateSystem)
        # Open an insert cursor on the output shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            # Add to output the output points and then return success message
            for point in outputPoints:
                iCursor.insertRow(point)
        return "The clip was successful!"
    #-------------------------------------------------------------------------------------------------------------------
    elif(inputGeo == "POLYLINE" and clipGEO == "POLYLINE"):
        # Create an empty list that will store line geometries
        inputLineGeo = []
        # Open a search cursor on the inputFile
        with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
            # Go through every line in the search cursor
            for row in SearchCursor:
                # Grab the geometry of that line
                pLine = row[0]
                # Get the Array containing the lines points by doing .getPart(0)
                pLineArray = pLine.getPart(0)
                # Some lines may have more than two points. Since they are stored in an array
                # Just loop through the array accessing individual elt points each time
                # Set up a prevPoint that will initially be None
                prevPoint = None
                # Loop through the points
                for point in pLineArray:
                    # If there is a prevPoint, create a polyLine out of the current point and the previous point
                    # and append to the inputLineGeo list
                    if(prevPoint!=None):
                        inputLineGeo.append(arcpy.Polyline(arcpy.Array([prevPoint,point])))
                    # set the previous point to the current point before moving on.
                    prevPoint = point
        # Set up a list that will store the polyline geometries from the clip objects
        cliplineObjects = []
        # Open a search cursor on the clip file
        with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
            # Go through every line in the search cursor
            for row in SearchCursor:
                # Grab the geometry of that line and append to cliplineObjects
                cliplineObjects.append(row[0])
        # Create an empty list that will have the output lines
        outputLines = []
        # Loop through both lists of lines
        for line in inputLineGeo:
            for line2 in cliplineObjects:
                # If the line from the input feature is within the line from the clip aka it is overlayed,
                # append it to the outputLines
                if(line.within(line2)):
                    outputLines.append(line)
        # Create output file
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POLYLINE',spatial_reference=inputCoordinateSystem)
         # Open an insert cursor on the output shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
             # Add to output the output points and then return success message
             for line in outputLines:
                 iCursor.insertRow([line])
        return "The clip was successful!"
    #-----------------------------------------------------------------------------------------------------------------------
    elif(inputGeo == "POLYLINE" and clipGEO == "POLYGON"):
        return "Not implemented"
    #-----------------------------------------------------------------------------------------------------------------------
    elif(inputGeo == "POLYGON" and clipGEO == "POLYGON"):
        return "Not implemented"
    #-----------------------------------------------------------------------------------------------------------------------
    elif(inputGeo == "MULTIPOINT" or clipGEO == "MULTIPOINT"):
        return "Sorry this clip does not support multipoint geometries at this time!"
    else:
        return "You tried to clip a geometry of higher order by a lower order which you cannot do. Try again!"
    
        
print(clip(r'C:\Users\caleb\GEOG 4303\CordsenCalebFinalProject\Test Results','lineonlinetest.shp',r'C:\Users\caleb\GEOG 4303\CordsenCalebFinalProject\Test Data\route.shp',r'C:\Users\caleb\GEOG 4303\CordsenCalebFinalProject\Test Data\lyons_mrd.shp'))        
    
    
