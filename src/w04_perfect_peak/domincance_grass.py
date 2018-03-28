'''Import libraries
'''
import sys
import os
import grass.script as grass
import grass.script.setup as gsetup


''' Set path to files and initialize GRASS environment 
'''
# Path/file settings
tl_path = r'C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue'
data_path = tl_path + os.sep + "data"
grassdb_path = tl_path + os.sep + r"grass"
dgm_filepath = data_path + os.sep + r"KU_DGM10\KU_DGM10.tif"
summit_filepath = data_path + os.sep + r"gipfelliste\brandenberger_alpen.shp"
summit_filepath = data_path + os.sep + r"gipfelliste\rofangebirge_subset.shp"

# Initialize GRASS
gisdb = os.path.join(os.getenv('APPDATA', 'grassdata'))
gisbase = os.environ['GISBASE'] 
gisdbase = grassdb_path
location = "Kufstein"
mapset   = "PERMANENT"

gsetup.init(gisbase, gisdbase, location, mapset)

# Check if GRASS has successfully been initialized
#grass.message('--- GRASS GIS 7: Current GRASS GIS 7 environment:')
#print grass.gisenv()

# Import pygrass (only possible after GRASS initialization)
from grass.pygrass.vector import VectorTopo
from grass.pygrass.modules import Module


''' Import data
(first time only)
'''
# grass.run_command('r.in.gdal', overwrite='true', input=dgm_filepath, output='dgm')
# grass.run_command('v.in.ogr', overwrite='true', input=summit_filepath, output='summit')


''' Get coordinates from summit data
'''
# See e.g. https://gis.stackexchange.com/questions/28061/how-to-access-vector-coordinates-in-grass-gis-from-python/28100#28100
summit = VectorTopo("summit", "PERMANENT", LOCATION_NAME="Kufstein")
summit.open(mode = 'r')
pointsList = []
for i in range(len(summit)):
    pointsList.append(summit.read(i+1))

''' Compute dominance
'''
# Example using just one summit
s = 14
summit.read(s).attrs["Name"]

# Use height from dem a position of actual summit
#type("x")
#x = grass.raster_what('dgm', [[summit.read(s).x, summit.read(s).y]], env=None, localized=False)
#hs = x[0]["dgm"]["value"]
#hs = str(float(hs)+1)
#print(hs)

# Use maximum height in the vicinitiy of the actual summit
grass.run_command("r.neighbors", input = "dgm", output = "dgm_maxfilter", method = "maximum", size = 31, overwrite = True)
type("x")
x = grass.raster_what('dgm_maxfilter', [[summit.read(s).x, summit.read(s).y]], env=None, localized=False)
hs = x[0]["dgm_maxfilter"]["value"]
hs = str(float(hs)+1)
print(hs)

# Reclass dem
# See e.g. https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
# Version using reclass file: 
#rfile = tmppath + os.sep + "temp.txt"
#with open(rfile, "w") as text_file:
#    text_file.write("%s thru 99999999999999999 = 1" % hs)
#grass.run_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = rfile, overwrite=True)

# Version without reclass file
grass.write_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = "-", stdin = "%s thru 9000 = 1" % hs, overwrite=True)

# Convert actual summit to raster   
grass.run_command("v.extract", input = "summit", output = "act_summit", where = 'Name = "%s"' % summit.read(s).attrs["Name"], overwrite=True)
grass.run_command("v.to.rast", input = "act_summit", output = "act_summit_rst", use="val", value = 1, overwrite=True)

d = grass.read_command("r.distance", map="act_summit_rst,dgm_reclass")
print(d)
domincance = d.split(":")[2]
print(domincance)


''' Compute prominance
'''

ah = str(float(hs)-100)



grass.write_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = "-", stdin = "%s thru 9000 = 1" % ah, overwrite=True)
grass.run_command("r.to.vect", input = "dgm_reclass", output = "dgm_reclass_vect", type="area", overwrite = True)
grass.run_command("v.select", ainput="dgm_reclass_vect", binput="act_summit", output="act_summit_area", operator="contains", overwrite=True)
grass.run_command("v.select", ainput="summit", binput="act_summit_area", output="summits_in_act_summit_area", operator="within", overwrite=True)
check_summits = VectorTopo("summits_in_act_summit_area", "PERMANENT", LOCATION_NAME="Kufstein")
check_summits.open(mode = 'r')
len(check_summits)


pointsList = []
for i in range(len(summit)):
    pointsList.append(summit.read(i+1))

grass.run_command("r.contour", input="dgm", output="isolines", step=50, minlevel=0, maxlevel=6000, overwrite = True)
grass.run_command("v.select", ainput="act_summit", binput="isolines", output = "act_summit_iso", operator="overlap", overwrite = True)


grass.run_command("v.overlay", ainput="isolines", binput="act_summit", output = "act_summit_iso", operator="and", overwrite = True)
grass.run_command("v.select", ainput="summit", binput="isolines", output="summits_in_isolines", operator="within", overwrite=True)

# define a boolean to stop the flooding process     
gotit = False
 
# define a variable that contains the actual flooding altitude
floodAlt = int(FloatFirstPeakAltitude)-1
 
# then import the DEM data
g.run_command("r.in.gdal",overwrite='true', quiet='true', input=fDGM, output="DGM")
 
# and import or rasterize the current peak as a raster
g.run_command("r.in.gdal",overwrite='true', quiet='true', input='peak.tif', output="peak")
 
# set set region for GRASS according to this data
g.run_command("g.region",rast="DGM")
 
# and import the peak data as vector data
# to make it more easy we produce to data sets:
 
# this is the current peak
g.run_command("v.in.ogr", flags='o',overwrite='true',quiet='true', dsn='start_peak.shp', output='peak')
 
# these are all peaks that are higher than the current one
g.run_command("v.in.ogr", flags='o',overwrite='true',quiet='true', dsn='flood_peaks.shp', output='flood_peak')  
 
# ok now pull the plug
while gotit == False:
    g.run_command('g.remove',quiet='true', vect='tmpresult,actualMyPeakFloodArea')
    # set treshold (altitude of the current peak) and newvalues for reclassification 
    tresholds=['0',str(floodAlt),'9999']
    recvalues=['NULL','1']
    # call the makerule file function to write rules for GRASS reclassification    
    makeruleGrass('reclass.prom',tresholds,recvalues)
    # reclass DEM according to actual peak altitude
    g.run_command('r.reclass',overwrite='true', quiet='true', input="DGM", output="flood", rules="reclass.prom")
 
    # unfortunately in most cases we will have a lot of distinct "islands" spread over the mask 
    # to get rid of the wrong ones (i.e. that are not containing our peak) we split the flooding areas 
        # in clumps with a unique ID   (i.e. we produce entities)  
    g.run_command('r.clump', overwrite='true', quiet='true', input='flood', output='floodclump')
 
    # but still we have to find out in which of the masked entities the current peak is sited 
    # therefore we first identify the location of the current peak and put it in a nodata raster matrix 
    g.run_command('r.mapcalculator',overwrite='true',quiet=True, amap='peak', formula='newmap=if(A==1,A,null())', outfile='peakself')
 
    # just to find the flooding area that contains the current peak we can use .rstatistics to do so
    g.run_command('r.statistics' , overwrite='true', quiet='true', base='floodclump', cover='peakself', method='max', output='myPeakFlood')
 
    # to derive in a more simple way the result we convert the raster to vector
    g.run_command('r.to.vect', overwrite='true', quiet='true', input='myPeakFlood' ,output='actualMyPeakFloodArea' ,feature='area')
 
    # and query if theree are two peaks inside this  area
    g.run_command('v.select', overwrite='true' , quiet='true',ainput='actualMyPeakFloodArea' ,atype='area' ,binput='flood_peak' ,btype='point' ,output='tmpresult' ,operator='overlap')
 
    # for a quick and dirty analysis of the result without enganging SQL we export the resulting attribute table of the vector file to a simple ASCII file
    g.run_command('v.out.ascii' ,input='tmpresult' ,quiet='true', output='tmpresult.xyz')
 
    # if there is just ONE line (=item) in list you have got the connection via a land bridge       
    lines= readXYZ('tmpresult.xyz')
 
    # for the loop put it into a variable
    linecount =len(lines)
 
    # if linecount is NOT equal 1 there is NO landbridge
        # so we lower the flooding altitude by an fix value
    if int(linecount) != 1:
        floodAlt = floodAlt-5
    else:     # if linecount == 1 we meet the stop criteria
        gotit = True
 
# if gotit is True convert vector to raster and multiply altitude by flooding mask to derive min value of this area
g.run_command('v.to.rast',overwrite='true', quiet='true' ,input='actualMyPeakFloodArea' ,output='myPeakFlood' ,use='val') 
 
# this is an alternative  call of r.mapcalc using the generic wrapper as provides by grasscript
g.mapcalc("${out} = ${rast1} * ${rast2}", out = 'prominencemap',   rast1 ='DGM', rast2 = 'myPeakFlood')
 
# get minimum altitude that is the prominence value
promi = g.raster_info('prominencemap')['min']
