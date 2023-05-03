"""
Author: Caleb Cordsen
Date: 4/8/2023

Description: This file contains the functions that help make the buffer function work!
"""
# Import necessary things
import arcpy
from arcpy import env
import math
import numpy as np
import os
import signal
import time

def unitConversion(inputFile,size,unit):
    '''
    Parameters
    ----------
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid shape file made up 
        of points.
    size : This should be a number.
        This should be a number representing how big you want the buffer to be. Currently this
        function is limited to only doing buffers of the same unit that the inputFile exists in.
    unit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.

    Returns
    -------
    float
        A float representing the float number that represents the inputFile units that is equivalent
        to the inputed size and unit. For example, if your inputFile is in feet but you input 50 as
        your size and meters as your unit, then this function outputs the number of feet that is
        equivalent to 50 meters.
        
    Description
    -----------
    This function takes in a inputFile and using arcpy spatial reference methods gets the metersPerUnit
    of the inputtedShape file. It then looks at the inputted size and unit. It converts the measurement of 
    size and unit into meters. For example, if you input 1 centimeter it will convert it to 0.01 meters.
    Then it takes this number and divides by the metersPerUnit measurement. The result of this is 
    the equivalent number representing the same measurement of the inputted size and unit but in the
    units of the inputFile. For example consider a scenario where you have an inputFile that is in feet.
    You input into the function a size of 750 and a unit of centimeters. First the function will
    convert 750 centimeteres into 7.5 meters by matching the unit to a preset conversion to meters
    using if statements. Then it will detect the metersPertUnit of feet which is about 0.3048.
    Then it will takes 7.5 meters and divide by 0.3048 which yields about 24.6063. This number will be
    returned and ultimately is what 750 centimeters is in feet (the inputFile's unit). 
    '''
    # Enter a series of if statements that checks the unit type. It then converts the size of that unit
    # into meters. If no such unit is found, it says that unit is unsupported at this time
    if(unit=="meters"):
        meterVersion = size
    elif(unit=="kilometers"):
        meterVersion = size*1000
    elif(unit=="decimeters"):
        meterVersion = size*0.1
    elif(unit=="centimeters"):
        meterVersion = size*0.01
    elif(unit=="millimeters"):
        meterVersion = size*0.001
    elif(unit=="miles"):
        meterVersion = size*1609.344
    elif(unit=="yards"):
        meterVersion = size*0.9144
    elif(unit=="feet"):
        meterVersion = size*0.3048
    elif(unit=="inches"):
        meterVersion = size*0.0254
    elif(unit=="nautical miles"):
        meterVersion = size*1852
    else:
        return "Sorry that unit type is unsupported at this time!"
    # Make a variable metersPerInputFileUnit that uses arcpy methods to get the metersPerUnit
    # of the inputFile's unit type
    metersPerInputFileUnit = arcpy.Describe(inputFile).spatialReference.metersPerUnit
    # Return the size of the unit given to the function converted to meters divided by the number
    # calculated above
    return meterVersion/metersPerInputFileUnit

def PointsBuffer(returnDir,inputFile, outputName, buffSize, buffUnit, pointsForBuff = 87):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created buffer file to.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid shape file made up 
        of points.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted buffer shape file.
    buffSize : This should be a number.
        This should be a number representing how big you want the buffer to be.
    buffUnit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.
    pointsForBuff : This should be an interger., optional
        This should be an integer representing how many points you want the buffer
        to be composed of. Beware the less number of points you make the buffer of the less circular
        the buffer will be I.E inputting 4 here will result in a square/rhombus buffer. The default
        value is 87 since this is around the number of points Arc uses to make their buffers.

    Returns
    -------
    str
        A message as a string saying whether or not the buffer was successful or errored out.
    
    Description
    -----------
    The PointsBuffer function first call the unitConversion function to convert the inputted buffSize
    and buffUnit to a number workable with the inputShapeFile. If the unit was invalid
    it will simply create the buffer of buffSize in the inputFile's unit type. Then it 
    will first create an empty list called centerCoordLst.  This list will
    consist of tuples of (x,y) pairs representing all the points in the inputFile. Then it will
    get the input files coordinate system and store it in inputCoordinateSystem. Then it briefly
    checks to make sure that the output name and directory that you have inputted does not already exist.
    If it does this function deletes it to make room for a new file. Then it opens a search cursor
    on the inputfile, extracting the x and y coordinates using SHAPE@X and SHAPE@Y. It goes through
    each point in the inputFile and appends their (x,y) pair to centerCoordLst. Then it makes
    a new shape file based on inputted returnDir and outputName, making it of type polygon and giving
    it the same coordinate system as the input file. Then it opens an insert cursor on the newly
    made shape file accessing its geometry property. Then with that insert cursor open, the function
    enters a loop iterating through the previously made centerCoordLst. For each (x,y) pair in this list,
    we declare a new list, circleCoordPoints that will contain all the arc points that make up the buffer.
    To determine the points we enter another loop using np.linspace. np.linspace takes in a start value,
    a stop value, and how many divisions you want. In this functions case, it goes from 0 to 360 since
    this represents the range of angular values that make up a circle. Then it takes in the inputted
    number of points to construct the buffer, subsequently dividing 0 to 360 up into even intervals, where
    the number of intervals is the number of points. The function includes the optional keyword in
    np.linspace endpoint=False since we do not want to include 360 as one of the points np.linspace
    generates since 0 and 360 are the same in a circle. Np.linspace returns an array of the
    point that divide up 0,360 aka angles. Our function
    loops directly through this. Now it calculates newX and newY values to begin building the circle.
    To do this it exploits the unit circle in the following way: A unit circle is a circle of radius 
    one and center point at (0,0). The points that make up the unit circle can be generated by
    doing (cos(radianMeasure),sin(radianMeasure)) aka the (x,y) points that make up the unit circle
    can be found by doing x = cos(radianMeasure) and y = sin(radianMeasure) So for example,
    one of the points on the unit circle is (0,1) and this can be generated by doing (cos(pi/2),sin(pi/2))
    math.cos and math.sin operate in radians so we will convert our degrees from np.linspace
    to radians by doing math.radians(angle). Then we can feed that number to math.cos() and
    math.sin() to get our X and Y respectively. However, this X and Y is that on a unit circle which
    has a radius of 1 and center point of (0,0). To transform this to a buffer where radius = newBuffSize
    and center point of (xCenterCoord,yCenterCoord) we multiple the math.cos() and math.sin()
    operations by newBuffSize then add xCenterCoord to x and yCenterCoord to y. This will transform our
    points to properly build our buffer. Consider why this works: Our right most point in a unit circle
    is (1,0). If we want a cirlce with radius = 4 and center point (5,7) our right most point should
    be at (9,7) aka 4 units to the right of the center. If (1,0) is determined via (cos(0),sin(0)) 
    then to transform it to (9,7) just adding 5 to the x and 7 to the y is insufficient since then we
    get (6,7). To replicate both the center point and radius we need to multiple the cos and sin values
    by the radius before adding the center point. This results in (9,7). So we apply this transformation
    generally to form all the buffer points.
    Then we add this newly generated point to our CircleCoordPoints. Once
    all the points have been generated stuff them into an arcpy array, and then put that arcpy array
    into an arcpy polygon and then insert that arcpy polygon as a new row in the outputfile. This
    process repeats for every point in the inputed shape file. This will try the above and if an error
    occurs will return a string saying so. This is for functionality with the GUI.
    '''
    # Try the following buffer methods
    try:
        # Convert the inputted units to the inputFiles units
        newBuffSize = unitConversion(inputFile,buffSize,buffUnit)
        # If not valid input unit, then just proceed to make the buffer in the inputFile's units
        # with the original size
        if(newBuffSize == "Sorry that unit type is unsupported at this time!"):
            print("That unit type is not supported. Creating buffer of inputted size in input files unit type")
            newBuffSize = buffSize
        # Create an empty list of center coordinates for the inputted points
        centerCoordLst = []
        # Get the coordinate system of the inputted file
        inputCoordinateSystem = arcpy.Describe(inputFile).spatialReference
        
        # Make sure to delete the output file if it already exists
        if (os.path.exists(os.path.join(returnDir,outputName))):
            arcpy.management.Delete(os.path.join(returnDir,outputName))
        
        # Use a search cursor to get the x and y coordinates of each point in the point file
        with arcpy.da.SearchCursor(inputFile,['SHAPE@X','SHAPE@Y']) as sCursor:
            for row in sCursor:
                centerCoordLst.append((row[0],row[1]))
        
        # Create a new shapefile based on the input to the function
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POLYGON',spatial_reference=inputCoordinateSystem)
        
        # Open a insert cursor on the new shapefile
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            # Loop through the list of coordinates of the point
            for xCenterCoord,yCenterCoord in centerCoordLst:
                # Create an empty list that will store the buffer points
                circleCoordPoints = []
                # Get angles equal width apart from one another from 0 to 360 
                for angle in np.linspace(0,360,pointsForBuff,endpoint=False):
                    # For each angle calculate the new X and Y by constructing unit circle points
                    # (cos for x and sin for y) and then multiply by newBuffSize and add to center points
                    newX = newBuffSize*math.cos(math.radians(angle))+xCenterCoord
                    newY = newBuffSize*math.sin(math.radians(angle))+yCenterCoord
                    # Add that point to the buffer points list
                    circleCoordPoints.append(arcpy.Point(newX,newY))
                # Create an arcpy array from the buffer poitns and then a polygon from the array.
                # Insert the polygon
                circlePointArray = arcpy.Array(circleCoordPoints)
                bufferPolygon = arcpy.Polygon(circlePointArray)
                iCursor.insertRow([bufferPolygon])
        # If this all occurs then the buffer was successful and a success message should be returned.
        return "The buffer was successful!"
    # If an error occured, the buffer was unsuccessful.
    except:
        return "The buffer was unsuccessful. Sorry!"
            
def lineBuffer(returnDir,inputFile, outputName, buffSize, buffUnit):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created buffer file to.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid polyline shape file.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted buffer shape file.
    buffSize : This should be a number.
        This should be a number representing how big you want the buffer to be.
    buffUnit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.
    Returns
    -------
    str
        This function returns a string representing a success or failure message.
        
    Description
    -----------
    The lineBuffer function utilizes a crude methodology to build a line buffer.First it 
    calls the unitConversion function to convert the inputted buffSize
    and buffUnit to a number workable with the inputShapeFile. If the unit was invalid
    it will simply create the buffer of buffSize in the inputFile's unit type. Then it sets up
    intermediate and output shape files in the same coordinate system as the inputted file.
    This function loops through each line in a POLYLINE geometry. It looks at each point in the line
    and creates a circle buffer around each point using the same methods as the cirlce buffer funciton.
    It then goes to the next point while saving the previous point. It then creates a rectangle of 
    width 2*BufferSize around the line that connects the current point and the previous point. 
    This is done by creating a unit vector in the direction of the line and then multiplying this by 
    the buffer size. The vector is constructed by doing <dx,dy> where dx = currentPointX - prevPointX
    and dy = currentPointY - prevPointY. It is then converted to a unit vector by dividing by the 
    distance which is the square root of (dx squared + dy squared). Finally it is multiplied by the 
    buffer size. Then it builds the rectangle by starting at each endpoint of the line and adding 
    to it the perpendicular vector which is <-dy,dx>. It adds to each endpoint both <-dy,dx> and
    <dy,-dx> so get the four endpoints of the rectangle. It then makes these into a polygon and adds
    it to the intermediate file. Finally, at the end it calls arcpy's dissolve function to create
    one polygon at the output file name from the many polygons created in the intermediate file.

    '''
    # Try the following buffer methods
    try:
        # Convert the inputted units to the inputFiles units
        newBuffSize = unitConversion(inputFile,buffSize,buffUnit)
        # If not valid input unit, then just proceed to make the buffer in the inputFile's units
        # with the original size
        if(newBuffSize == "Sorry that unit type is unsupported at this time!"):
            print("That unit type is not supported. Creating buffer of inputted size in input files unit type")
            newBuffSize = buffSize
        # Get the inputFile's coordinate system
        inputCoordinateSystem = arcpy.Describe(inputFile).spatialReference
        # Delete intermediate and output files if they exist
        if (os.path.exists(os.path.join(returnDir,outputName))):
            arcpy.management.Delete(os.path.join(returnDir,outputName))
        if (os.path.exists(os.path.join(returnDir,'intermediate.shp'))):
            arcpy.management.Delete(os.path.join(returnDir,'intermediate.shp'))
        # Create an intermediate shape file
        arcpy.CreateFeatureclass_management(returnDir, 'intermediate.shp','POLYGON',spatial_reference=inputCoordinateSystem)
        
        # Open an insert cursor on the intermediate shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,'intermediate.shp'), ['SHAPE@']) as iCursor:
            # Open a search cursor on the input file
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
                        # Make a list for circular buffer points
                        circleCoordPoints = []
                        # Make a circle buffer around each point using methods described in
                        # point buffer
                        for angle in np.linspace(0,360,87,endpoint=False):
                            newX = newBuffSize*math.cos(math.radians(angle))+point.X
                            newY = newBuffSize*math.sin(math.radians(angle))+point.Y
                            circleCoordPoints.append(arcpy.Point(newX,newY))
                        circlePointArray = arcpy.Array(circleCoordPoints)
                        bufferPolygon = arcpy.Polygon(circlePointArray)
                        iCursor.insertRow([bufferPolygon])
                        # If the prevPoint is not none, we can construct a rectangle Buffer
                        if(prevPoint!=None):
                            # Calculate a vector in the direction of the line of size newBuffSize
                            dx = point.X - prevPoint.X
                            dy = point.Y - prevPoint.Y
                            D = math.sqrt(dx*dx + dy*dy)
                            dx = newBuffSize * dx / D
                            dy = newBuffSize*dy/D
                            rectangleCoords = []
                            # Add the four points of the buffer rectangle by using the 
                            # perpendicular vector and then make a polygon out of them and add to 
                            # intermediate shape file
                            rectangleCoords.append(arcpy.Point(prevPoint.X-dy,prevPoint.Y+dx))
                            rectangleCoords.append(arcpy.Point(prevPoint.X+dy,prevPoint.Y-dx))
                            rectangleCoords.append(arcpy.Point(point.X+dy,point.Y-dx))
                            rectangleCoords.append(arcpy.Point(point.X-dy,point.Y+dx))
                            rectangleArray = arcpy.Array(rectangleCoords)
                            rectanglePolygon = arcpy.Polygon(rectangleArray)
                            iCursor.insertRow([rectanglePolygon])
                        # set the previous point to the current point before moving on.
                        prevPoint = point
        # Use arcpy's dissolve to create the shape file for the output.
        arcpy.analysis.PairwiseDissolve(os.path.join(returnDir,'intermediate.shp'),os.path.join(returnDir,outputName))
        return "The buffer was successful!"
    # If an error occured, the buffer was unsuccessful.
    except:
        return "The buffer was unsuccessful. Sorry!"
  
def polygonBuffer(returnDir,inputFile, outputName, buffSize,buffUnit):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created buffer file to.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid polygon shape file.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted buffer shape file.
    buffSize : This should be a number.
        This should be a number representing how big you want the buffer to be.
    buffUnit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.
        
    Returns
    -------
    str
        This function returns a string representing a success or failure message.
        
    Description
    -----------
    The polygonBuffer function uses a very crude methodology to create a polygon buffer. 
    It should be warned that this is definitely not using the most effective algorithm to do so 
    and creates many polygons in the process. Essentially, this function uses ArcPy methods to grab 
    the POLYLINE boundary(s) of the inputted polygon shape file. It then performs essentially a 
    line buffer on that POLYLINE boundary (adding circle buffers around each point and constructing 
    rectangle buffers around each line). Further documentation on the line buffer methods can be 
    found in the docstring for the line buffer function. It also adds the original polygon to the 
    output layer. It should be warned that the outputted buffer shape file will have many polygons
    to construct the buffer.

    '''
    # Try the following buffer methods
    try:
        # Convert the inputted units to the inputFiles units
        newBuffSize = unitConversion(inputFile,buffSize,buffUnit)
        # If not valid input unit, then just proceed to make the buffer in the inputFile's units
        # with the original size
        if(newBuffSize == "Sorry that unit type is unsupported at this time!"):
            print("That unit type is not supported. Creating buffer of inputted size in input files unit type")
            newBuffSize = buffSize
        # Get the inputFile's coordinate system
        inputCoordinateSystem = arcpy.Describe(inputFile).spatialReference
        
        # Delete intermediate and output files if they exist
        if (os.path.exists(os.path.join(returnDir,outputName))):
            arcpy.management.Delete(os.path.join(returnDir,outputName))
        if (os.path.exists(os.path.join(returnDir,'intermediate.shp'))):
            arcpy.management.Delete(os.path.join(returnDir,'intermediate.shp'))
        # Create an intermediate shape file
        arcpy.CreateFeatureclass_management(returnDir, 'intermediate.shp','POLYGON',spatial_reference=inputCoordinateSystem)
        
        # Open an insert cursor on the intermediate shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,'intermediate.shp'), ['SHAPE@']) as iCursor:
            # Open a search cursor on the input shape file
            with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
                for row in SearchCursor:
                    # Access the row containing the polygons geometry and access its POLYLINE boundary
                    # and store in the pLines
                    pLines = row[0].boundary()
                    # Insert the original polygon geometry into the intermediate
                    iCursor.insertRow([row[0]])
                    # Get the Array containing the POLYLINEs from the boundary
                    pLineArray = pLines.getPart()
                    # The polygon boundary may be composed of multiple POLYLINEs so loop through
                    # each line
                    for line in pLineArray:
                        # Set the prevPoint to None to start for each line
                        prevPoint = None
                        # Loop through each point in the line
                        for point in line:
                            # Make a list for circular buffer points
                            circleCoordPoints = []
                            # Make a circle buffer around each point using methods described in
                            # point buffer
                            for angle in np.linspace(0,360,87,endpoint=False):
                                newX = newBuffSize*math.cos(math.radians(angle))+point.X
                                newY = newBuffSize*math.sin(math.radians(angle))+point.Y
                                circleCoordPoints.append(arcpy.Point(newX,newY))
                            circlePointArray = arcpy.Array(circleCoordPoints)
                            bufferPolygon = arcpy.Polygon(circlePointArray)
                            iCursor.insertRow([bufferPolygon])
                            # If the prevPoint is not none, we can construct a rectangle Buffer
                            if(prevPoint!=None):
                                # Calculate a vector in the direction of the line of size newBuffSize
                                dx = point.X - prevPoint.X
                                dy = point.Y - prevPoint.Y
                                D = math.sqrt(dx*dx + dy*dy)
                                dx = newBuffSize * dx / D
                                dy = newBuffSize*dy/D
                                rectangleCoords = []
                                # Add the four points of the buffer rectangle by using the 
                                # perpendicular vector and then make a polygon out of them and add to 
                                # intermediate shape file
                                rectangleCoords.append(arcpy.Point(prevPoint.X-dy,prevPoint.Y+dx))
                                rectangleCoords.append(arcpy.Point(prevPoint.X+dy,prevPoint.Y-dx))
                                rectangleCoords.append(arcpy.Point(point.X+dy,point.Y-dx))
                                rectangleCoords.append(arcpy.Point(point.X-dy,point.Y+dx))
                                rectangleArray = arcpy.Array(rectangleCoords)
                                rectanglePolygon = arcpy.Polygon(rectangleArray)
                                iCursor.insertRow([rectanglePolygon])
                            # set the previous point to the current point before moving on.
                            prevPoint = point
        arcpy.analysis.PairwiseDissolve(os.path.join(returnDir,'intermediate.shp'),os.path.join(returnDir,outputName))
        return "The buffer was successful!"
    # If an error occured, the buffer was unsuccessful.
    except:
        return "The buffer was unsuccessful. Sorry!"
    
def multiPointBuffer(returnDir,inputFile, outputName, buffSize,buffUnit):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created buffer file to.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid multipoint shape file.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted buffer shape file.
    buffSize : This should be a number.
        This should be a number representing how big you want the buffer to be.
    buffUnit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.

    Returns
    -------
    str
        This function returns a string representing a success or failure message.
        
    Description
    -----------
    The multiPointBuffer function accesses all the points included in the multipoint feature and
    applies the same methodology as the point buffer to each point in the multipoint feature. It creates
    circular buffers around each point of the buffSize and buffUnit. For more documentation on how 
    the circular buffer works, see the PointsBuffer docstring.
    '''
    # Try the following buffer methods
    try:
        # Convert the inputted units to the inputFiles units
        newBuffSize = unitConversion(inputFile,buffSize,buffUnit)
        # If not valid input unit, then just proceed to make the buffer in the inputFile's units
        # with the original size
        if(newBuffSize == "Sorry that unit type is unsupported at this time!"):
            print("That unit type is not supported. Creating buffer of inputted size in input files unit type")
            newBuffSize = buffSize
        # Get the inputFile's coordinate system
        inputCoordinateSystem = arcpy.Describe(inputFile).spatialReference
        
        # Delete output files if they exist
        if (os.path.exists(os.path.join(returnDir,outputName))):
            arcpy.management.Delete(os.path.join(returnDir,outputName))
        # Create the output shape file
        arcpy.CreateFeatureclass_management(returnDir, outputName,'POLYGON',spatial_reference=inputCoordinateSystem)
        
        # Open an insert cursor on the intermediate shape file
        with arcpy.da.InsertCursor(os.path.join(returnDir,outputName), ['SHAPE@']) as iCursor:
            # Open a search cursor on the input shape file
            with arcpy.da.SearchCursor(inputFile,['SHAPE@']) as SearchCursor:
                for row in SearchCursor:
                    # Get the points from the multipoint feature by accessing the geometry
                    # and getting part
                    lstOfPoints = row[0].getPart()
                    # Loop through the points
                    for point in lstOfPoints:
                        # Make an empty list to store the buffer points
                        circleCoordPoints = []
                        # Make a circle buffer around each point using methods described in
                        # point buffer
                        for angle in np.linspace(0,360,87,endpoint=False):
                            newX = newBuffSize*math.cos(math.radians(angle))+point.X
                            newY = newBuffSize*math.sin(math.radians(angle))+point.Y
                            circleCoordPoints.append(arcpy.Point(newX,newY))
                        circlePointArray = arcpy.Array(circleCoordPoints)
                        bufferPolygon = arcpy.Polygon(circlePointArray)
                        iCursor.insertRow([bufferPolygon])
        # If this all happens return a success message
        return "The buffer was successful!"
    # If an error occured, the buffer was unsuccessful
    except:
        return "The buffer was unsuccessful. Sorry!"

def bufferMain(returnDir,inputFile, outputName, buffSize, buffUnit):
    '''
    Parameters
    ----------
    returnDir : This should be a string representing a file path.
        This should be a string representing a file path to the directory/folder you wish to save
        your created buffer file to.
    inputFile : This should be a string representing a file path.
        This should be a string representing a file path that points to a valid shape file.
    outputName : This should be a string representing a file name and extension.
        This should be a string representing a file name and extension. This will be 
        the name of the outputted buffer shape file.
    buffSize : This should be a float.
        This should be a float representing how big you want the buffer to be.
    buffUnit: This should be a string,
        This should be a string representing the unit associated with the desired buffered size.
        Restricted to the units available in the unit conversion function.
    
    Returns
    -------
    str
        This function returns a string representing a success or failure message.
        
    Description
    -----------
    The bufferMain function is the driver function for the GUI that runs buffer requests. It
    detects the inputFile geometry and then calls the appropiate buffer function for the matching
    geometry. For example, if the inputted geometry is a POLYGON, this function will call the 
    polygonBuffer function. This function will return a success or failure message depending
    on the subsequent buffer call. If the geometry type that was inputted does not match
    POINT, POLYLINE, POLYGON, or MULTIPOINT then it will send back a message saying that it does not
    recognize the geometry type.
    '''
    # Detect geometry type using ArcPy describe
    geoType = arcpy.Describe(inputFile).shapeType.upper()
    # Check if it is of a certain Geometry type. If it is call that matching geometries
    # specific buffer function
    if(geoType=="POINT"):
        return PointsBuffer(returnDir,inputFile,outputName,buffSize,buffUnit)
    elif(geoType=="POLYLINE"):
        return lineBuffer(returnDir,inputFile,outputName,buffSize,buffUnit)
    elif(geoType=="POLYGON"):
        return polygonBuffer(returnDir,inputFile,outputName,buffSize,buffUnit)
    elif(geoType=="MULTIPOINT"):
        return multiPointBuffer(returnDir,inputFile,outputName,buffSize,buffUnit)
    # If it did not match any of the above geometries, return a failure message about not recognizing
    # geometry type.
    else:
        return "Sorry that geometry type is not recognized and thus cannot be buffered!"

def batchBuffer(returnDirs,inputFiles, outputNames, buffSizes, buffUnits):
    '''
    Parameters
    ----------
    returnDirs : A list of strings representing file paths.
        This should be a list of strings representing file paths to the directories/folders you wish to save
        your created buffer files to.
    inputFiles : A list of strings representing file paths.
        This should be a list of strings representing file paths that point to a series of valid shape files.
    outputNames : This should be a list of strings representing a series of file names and extensions.
        This should be a list of strings representing a series of file names and extensions. These will be 
        the names of the outputted buffer shape files.
    buffSizes : This should be a list of floats.
        This should be a list of floats representing how big you want each buffer in the series to be.
    buffUnits : This should be a list of strings,
        This should be a list of strings representing the unit associated with the desired buffered size for the series.
        Restricted to the units available in the unit conversion function.

    Returns
    -------
    A list of strings where each entry in the list represents whether the buffer at that index failed or succeeded
    
    Description
    -----------
    The batchBuffer function does a batch of buffers on multiple inputted files. The inputs are formated in lists
    where each entry in the list represents a buffer to be done. The entry must be consistent across the different input lists.
    For example, everything at index 0 across the different lists represents the input for one buffer to be done. The inputFile at
    index 0 in the inputFiles list will have a buffer ran on it of the size and unit at index 0 in buffSizes and buffUnits and will
    be outputted to the file location made from index 0 of the returnDirs and outputNames. This will return a list of status's
    where S represents a successful buffer and F represents a failed buffer. Ultimately the logic of this function is to call
    the bufferMain function on each list entry.
    '''
    # Check to make sure the input lists are all of same size. If they aren't return an error message
    if(len(returnDirs)!=len(inputFiles) or len(inputFiles)!=len(outputNames) or len(outputNames)!=len(buffSizes) or len(buffSizes)!=len(buffUnits)):
        return "Please input lists of all the same size!"
    else:
        # If they are the same size create an empty return list
        returnList = []
        # Loop through the lists
        for index in range(len(returnDirs)):
            # Store in x the return message from running a buffer at each index
            x = bufferMain(returnDirs[index],inputFiles[index],outputNames[index],buffSizes[index],buffUnits[index])
            # If the return message was a success append a S, otherwise a F
            if(x == "The buffer was successful!"):
                returnList.append("S")
            else:
                returnList.append("F")
        # Return the list of return messages
        return returnList