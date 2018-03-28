import sys
import os
import grass.script as grass
import grass.script.setup as gsetup

tl_path = r'C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue'
data_path = tl_path + os.sep + "data"
grassdb_path = tl_path + os.sep + r"grass"
dgm_filepath = data_path + os.sep + r"KU_DGM10\KU_DGM10.tif"
summit_filepath = data_path + os.sep + r"gipfelliste\brandenberger_alpen.shp"
tmppath = data_path + os.sep + r"temp"

gisdb = os.path.join(os.getenv('APPDATA', 'grassdata'))
gisbase = os.environ['GISBASE'] 
gisdbase = grassdb_path
location = "Kufstein"
mapset   = "PERMANENT"

gsetup.init(gisbase, gisdbase, location, mapset)

grass.run_command('r.in.gdal', overwrite='true', input=dgm_filepath, output='dgm')
grass.run_command('v.in.ogr', overwrite='true', input=summit_filepath, output='summit')


from grass.pygrass.vector import VectorTopo
from grass.pygrass.modules import Module

summit = VectorTopo("summit", "PERMANENT", LOCATION_NAME="Kufstein")
summit.open(mode = 'r')
pointsList = []
for i in range(len(summit)):
    pointsList.append(summit.read(i+1))


grass.run_command("r.neighbors", input = "dgm", output = "dgm_maxfilter", method = "maximum", size = 31)
type("x")
x = grass.raster_what('dgm_maxfilter', [[pointsList[0].x, pointsList[0].y]], env=None, localized=False)
hs = x[0]["dgm_maxfilter"]["value"]
hs = str(float(hs)+1)
print(hs)


pointsList[0]
type("x")
x = grass.raster_what('dgm', [[pointsList[0].x, pointsList[0].y]], env=None, localized=False)
hs = x[0]["dgm"]["value"]
hs = str(float(hs)+1)
print(hs)

grass.write_command("r.reclass", input = "dgm", output = "dgm_reclass", rules = "-", stdin = "%s thru 9000 = 1" % hs, overwrite=True)
grass.run_command("v.to.rast", input = "summit", output = "summit_rst", use="val", value = 1, overwrite=True)

d = grass.read_command("r.distance", map="summit_rst,dgm_reclass")
print(d)