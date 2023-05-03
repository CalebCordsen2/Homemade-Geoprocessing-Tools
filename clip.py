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
        you wish to use as your clip feature for the clip.
    
    
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
    try:
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
                    if(row[0]!=None):
                    # Add to list point geometries
                        inputPoints.append(row[0])
            # Do the same process on the clip feature
            clipPoints = []
            with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
                for row in SearchCursor:
                    if(row[0]!=None):
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
                    if(row[0]!=None):
                    # Add to list point geometries
                        inputPoints.append(row[0])
            # Do the same process on the clip feature, adding the clip lines
            clipLines = []
            with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
                for row in SearchCursor:
                    if(row[0]!=None):
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
                    if(row[0]!=None):
                    # Add to list point geometries
                        inputPoints.append(row[0])
            # Do the same process on the clip feature, adding the clip polygons
            clipPolygons = []
            with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
                for row in SearchCursor:
                    if(row[0]!=None):
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
                    if(row[0]!=None):
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
                    if(row[0]!=None):
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
            # # Create an empty list that will store the line geometry of the clip feature
            # # and one that will store the polygons of the clip feature
            # clipLineGeo = []
            # clipPolygonGeo = []
            # # Open a search cursor on the clipFile
            # with arcpy.da.SearchCursor(clipFile,['SHAPE@']) as SearchCursor:
            #     # Go through every line in the search cursor
            #     for row in SearchCursor:
            #         # Grab the geometry of that polygon and its polyline boundary
            #         pLines = row[0].boundary()
            #         # Add polygon to polygon list
            #         clipPolygonGeo.append(row[0])
            #         # Get the Array containing the lines points by doing .getPart()
            #         pLineArray = pLines.getPart()
            #         # Loop through the lines 
            #         for line in pLineArray:
            #             # Set up a prev point
            #             prevPoint = None
            #             # Loop through the points in the line
            #             for point in line:
            #                 # If there is a prevPoint, create a polyLine out of the current point and the previous point
            #                 # and append to the clipLineGeo list
            #                 if(prevPoint!=None):
            #                     clipLineGeo.append(arcpy.Polyline(arcpy.Array([prevPoint,point])))
            #                 # set the previous point to the current point before moving on.
            #                 prevPoint = point
            # # Create an empty list to store output lilnes        
            # outputLines = []
            # # Open a search cursor on the inputFile
            # with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
            #     # Go through every line in the search cursor
            #     for row in SearchCursor:
            #         if(row[0]!=None):
            #             # Grab the geometry of that line
            #             print(row[0])
            #             pLine = row[0]
            #             # Get the Array containing the lines points by doing .getPart(0)
            #             pLineArray = pLine.getPart(0)
            #             # Some lines may have more than two points. Since they are stored in an array
            #             # Just loop through the array accessing individual elt points each time
            #             # Set up a prevPoint that will initially be None
            #             prevPoint = None
            #             # Set up a boolean that saves whether the previous point was within the polygon or not
            #             prevPointWithin = False
            #             # Loop through the points
            #             for point in pLineArray:
            #                 for polygon in clipPolygonGeo:
            #                     if(point.within(polygon)):
            #                         outputLines.append(point)
            #                 prevPoint = point
            #       # Create output file
            # arcpy.CreateFeatureclass_management(returnDir, outputName,'POINT',spatial_reference=inputCoordinateSystem)
            #   # Open an insert cursor on the output shape file
            # with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            #       # Add to output the output points and then return success message
            #       for point in outputLines:
            #           iCursor.insertRow(point)
            return "POLYLINE and POLYGON clips are not implemented at this time!"
            # Set up a list that will store the polyline geometries from the clip objects
        #-----------------------------------------------------------------------------------------------------------------------
        elif(inputGeo == "POLYGON" and clipGEO == "POLYGON"):
            return "POLYGON and POLYGON clips are not implemented at this time"
        #-----------------------------------------------------------------------------------------------------------------------
        elif(inputGeo == "MULTIPOINT" or clipGEO == "MULTIPOINT"):
            return "Sorry this clip does not support multipoint geometries at this time!"
        else:
            return "You tried to clip a geometry of higher order by a lower order which you cannot do. Try again!"
    except:
        return "The clip has failed. Sorry!"
    
def batchClip(returnDirs,outputNames,inputFiles,clipFiles):
    '''
    Parameters
    ----------
    returnDirs : This should be a list of strings representing a series of file paths.
        This should be a list of strings representing file paths to the directories/folders you wish to save
        your created clip files to.
    outputNames : This should be a list of strings representing  file names and extensions.
        This should be a list of strings representing file names and extensions. These will be 
        the names of the outputted clip shape files.
    inputFiles : This should be a list of strings representing a series of file paths.
        This should be a list of strings representing file paths that point to valid shape files that 
        you wish to use as your input features for clipping
    clipFiles : This should be a list of strings representing a series of file paths.
        This should be a list of strings representing file paths that points to valid shape files that
        you wish to use as your clip features for the clip.
    
    
    Returns
    -------
    A list of strings where each entry in the list represents whether the buffer at that index failed or succeeded
            
    Description
    -----------
    The batchClip function does a batch of clips on multiple inputted files. The inputs are formated in lists
    where each entry in the list represents a clip to be done. The entry must be consistent across the different input lists.
    For example, everything at index 0 across the different lists represents the input for one clip to be done. The inputFile at
    index 0 in the inputFiles list will have a clip ran on using the clipfeature at index 0 in 
    clipFiles. This will return a list of status's
    where S represents a successful clip and F represents a failed clip. Ultimately the logic of this function is to call
    the clip function on each list entry.
    '''
    # Check to make sure the input lists are all of same size. If they aren't return an error message
    if(len(returnDirs)!=len(outputNames) or len(inputFiles)!=len(outputNames) or len(inputFiles)!=len(clipFiles)):
        return "Please input lists of all the same size!"
    else:
        # If they are the same size create an empty return list
        returnList = []
        # Loop through the lists
        for index in range(len(returnDirs)):
            # Store in x the return message from running a clip at each index
            x = clip(returnDirs[index],outputNames[index],inputFiles[index],clipFiles[index])
            # If the return message was a success append a S, otherwise a F
            if(x == "The clip was successful!"):
                returnList.append("S")
            else:
                returnList.append("F")
        # Return the list of return messages
        return returnList
    
    
