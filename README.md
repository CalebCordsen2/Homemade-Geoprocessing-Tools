# "Homemade" Geoprocessing Tools
## Author: Caleb Cordsen

### Description
Geoprocessing tools are used often to conduct a wide variety of spatial analysis everyday. The majority of organizations use tools provided from ESRI such as ArcGIS Pro to do said analysis. However since ESRI tools are proprietary, there is a level of mystery to how these tools really function under the hood. 

In an attempt to better understand geospatial data and processes, the author of this repository has attempted to homemake some well known geoprocessing tools like the buffer. It should be noted that these homemade tools do rely on certain features of ArcPy to access spatial data through things like insert and search cursors, as well as using ArcPy functionaility to create new layers. So while it seeks to get away from the plug and chug of calling the ArcPy functions by building a custom version of things like buffer, this project does still rely on certain ArcPy tools. 

### Use
This project also built a simple GUI using tkinter so that users can interact with the geoprocessing tools and run them in a more user friendly environment then a python script. To run the GUI or use the scripts, one must be in a valid ArcPy environment (correct licensing and such). Running the GUI can be done from main.py and should launch the GUI across machines. Generally through cloning this repo, users should be able to import whatever functions they want to use or run the GUI from main.py. More detailed documentation about functionality is documented within the code.

### Limitations
Since these tools are homemade they are certainly not utilizing the most optimized algorithms, and thus runtimes are often longer than their ESRI counterparts. There are also limitations in the options available to users compared to ESRI tools. Still, this project proved invaluable to the author to learn more about the structure of geospatial data and how certain geoprocesses work at the base level.
