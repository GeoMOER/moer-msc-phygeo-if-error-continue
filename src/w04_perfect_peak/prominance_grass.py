import sys
import os
import grass.script as grass
import grass.script.setup as gsetup

''' Set path
'''
# https://gis.stackexchange.com/questions/198540/grass-7-environment-setup-for-python
tl_path = r'C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue'
data_path = tl_path + os.sep + "data"
grassdb_path = tl_path + os.sep + r"grass"
dgm_filepath = data_path + os.sep + r"KU_DGM10\KU_DGM10.tif"
summit_filepath = data_path + os.sep + r"gipfelliste\brandenberger_alpen.shp"
tmppath = data_path + os.sep + r"temp"

''' Init GRASS
os.environ['GISBASE'] = r'C:\OSGeo4W64\apps\grass\grass-7.2.2'
os.environ['GISRC'] = r'C:\Users\tnauss\AppData\Roaming\GRASS7\rc'
os.environ['LD_LIBRARY_PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\lib'
os.environ['PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\;C:\OSGeo4W64\bin'
os.environ['PYTHONLIB']= r'C:\OSGeo4W64\apps\Python27'
os.environ['PYTHONPATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\etc\python;C:\OSGeo4W64\apps\qgis\python'

sys.path.append(r"C:\OSGeo4W64\apps\grass\grass-7.2.2\etc\python")
'''

gisdb = os.path.join(os.getenv('APPDATA', 'grassdata'))
gisbase = os.environ['GISBASE'] 
gisdbase = grassdb_path
location = "Kufstein"
mapset   = "PERMANENT"

gsetup.init(gisbase, gisdbase, location, mapset)

from grass.pygrass.vector import VectorTopo
from grass.pygrass.modules import Module
'''

# Print some information
grass.message('--- GRASS GIS 7: Current GRASS GIS 7 environment:')
print grass.gisenv()

grass.message('--- GRASS GIS 7: Checking projection info:')
in_proj = grass.read_command('g.proj', flags = 'jf')
kv = grass.parse_key_val(in_proj)
print kv['+proj']

grass.message('--- GRASS GIS 7: Checking computational region info:')
in_region = grass.region()
grass.message("--- Computational region: '%s'" % in_region)
'''

'''
# import data
grass.run_command('r.in.gdal', overwrite='true', input=dgm_filepath, output='dgm')
grass.run_command('v.in.ogr', overwrite='true', input=summit_filepath, output='summit')
'''


''' Get coordinates from summit dataset
'''
# https://gis.stackexchange.com/questions/28061/how-to-access-vector-coordinates-in-grass-gis-from-python/28100#28100
summit = VectorTopo("summit", "PERMANENT", LOCATION_NAME="Kufstein")
summit.open(mode = 'r')
pointsList = []
for i in range(len(summit)):
    pointsList.append(summit.read(i+1))

''' Compute dominance
'''
# Example using just the first summit
pointsList[0]
help(grass.raster_what)
print(grass.read_command('r.what', map="dgm", points = "summit"))

type("x")
x = grass.raster_what('dgm', [[pointsList[0].x, pointsList[0].y]], env=None, localized=False)
hs = x[0]["dgm"]["value"]
hs = str(float(hs)+50)
print(hs)

# Reclass dgm
# https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
'''
# Version using reclass file 
rfile = tmppath + os.sep + "temp.txt"
with open(rfile, "w") as text_file:
    text_file.write("%s thru 99999999999999999 = 1" % hs)
grass.run_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = rfile, overwrite=True)
'''
grass.write_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = "-", stdin = "%s thru 9000 = 1" % hs, overwrite=True)
grass.run_command("v.to.rast", input = "summit", output = "summit_rst", use="val", value = 1, overwrite=True)

d = grass.read_command("r.distance", map="summit_rst,dgm_reclass")
print(d)