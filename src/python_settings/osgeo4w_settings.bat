REM ###########################################################################
REM The first section will be sufficient for python bindings of osgeo
REM This is the default setting when starting the OSGeo4W shell in Windows
REM ###########################################################################

REM Short DOS names can be retrieved from the cmd interface using "dir /x"
REM Included from OSGEO4W_ROOT\bin\o4w_env.bat
set OSGEO4W_ROOT=C:\OSGEO4~1
set path=%OSGEO4W_ROOT%\bin;%WINDIR%\system32;%WINDIR%;%WINDIR%\system32\WBem

REM Included from OSGEO4W_ROOT\etc\ini\gdal.bat
SET GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
SET GDAL_DRIVER_PATH=%OSGEO4W_ROOT%\bin\gdalplugins

REM Included from OSGEO4W_ROOT\etc\ini\libgeotiff.bat
SET GEOTIFF_CSV=%OSGEO4W_ROOT%\share\epsg_csv

REM Included from OSGEO4W_ROOT\etc\ini\libjpeg.bat
set JPEGMEM=1000000

REM Included from OSGEO4W_ROOT\etc\ini\liblas.bat
SET GDAL_DATA=%OSGEO4W_ROOT%\share\gdal

REM Included from OSGEO4W_ROOT\etc\ini\orfeotoolbox-apps.bat
SET ITK_AUTOLOAD_PATH=%OSGEO4W_ROOT%\apps\orfeotoolbox\applications;%ITK_AUTOLOAD_PATH%

REM Included from OSGEO4W_ROOT\etc\ini\orfeotoolbox-python.bat
SET PYTHONPATH=%OSGEO4W_ROOT%\apps\orfeotoolbox\python;%PYTHONPATH%

REM Included from OSGEO4W_ROOT\etc\ini\proj.bat
SET PROJ_LIB=%OSGEO4W_ROOT%\share\proj

REM Included from OSGEO4W_ROOT\etc\ini\python-core.bat
SET PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27
PATH %OSGEO4W_ROOT%\apps\Python27\Scripts;%PATH%

REM Included from OSGEO4W_ROOT\etc\ini\qt4.bat
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt4\plugins
set QT_RASTER_CLIP_LIMIT=4096

REM Included from OSGEO4W_ROOT\etc\ini\rbatchfiles.bat
IF EXIST "%ProgramFiles%\R\" %OSGEO4W_ROOT%\apps\rbatchfiles\R path



REM ###########################################################################
REM The second section will make GRASS GIS available
REM ###########################################################################

REM Included from OSGEO4W_ROOT\apps\grass\grass-7.2.2\etc\env.bat
REM Some settings have already been covered above and are commented out
set GISBASE=%OSGEO4W_ROOT%\apps\grass\grass-7.2.2
set GRASS_PYTHON=%OSGEO4W_ROOT%\bin\python.exe
REM set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27
set GRASS_PROJSHARE=%OSGEO4W_ROOT%\share\proj
REM set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
REM set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
REM set GEOTIFF_CSV=%OSGEO4W_ROOT%\share\epsg_csv
set FONTCONFIG_FILE=%GISBASE%\etc\fonts.conf
REM set RStudio temporarily to %PATH% if it exists
IF EXIST "%ProgramFiles%\RStudio\bin\rstudio.exe" set PATH=%PATH%;%ProgramFiles%\RStudio\bin
REM set R_USER if %USERPROFILE%\Documents\R\ exists to catch most common cases of private R libraries
IF EXIST "%USERPROFILE%\Documents\R\" set R_USER=%USERPROFILE%\Documents\

REM The above settings allow starting grass from the command line but not from within Python.
REM Therefore, the grass Python modules have to be included in the PYTHONPATH variable.
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\grass\grass-7.2.2\etc\python

REM IMPORTANT: 
REM Before actually running grass.script functions, the grass location has to be 
REM added to the system path.
REM Before actually running pygrass modules, you have to set the GISRC variable
REM See e.g.: https://grasswiki.osgeo.org/wiki/Working_with_GRASS_without_starting_it_explicitly
REM set path=%path%;%OSGEO4W_ROOT%\apps\grass\grass-7.2.2
set path=%path%;C:\OSGeo4W64\apps\grass\grass-7.2.2
set GISRC=C:\Users\tnauss\AppData\Roaming\GRASS7\rc


REM ###########################################################################
REM The third section will make QGIS available
REM ###########################################################################
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set path=%path%;%OSGEO4W_ROOT%\apps\qgis\bin


REM ###########################################################################
REM What's next?
REM ###########################################################################
REM Run a Python session or e.g. start Eclipse and configure it:
REM Eclipse configuration:
REM Use C:\OSGeo4W64\bin\python.exe to configure the interpreter. As as you 
REM will see, the Python libraries will be selected automatically according to 
REM the content of this bash script.
REM Unfortunately, the environment variables are not set at all.
REM Copy the values of the variables from the script or better copy the content 
REM from a cmd line window using "echo %Variable-Name%" and add it to the
REM Eclipse settings (except for variable PYTHONPATH which is defined in the
REM Eclipse Libraries section).
REM Afterwards you can start Eclipse without using this batch file.
REM Uncomment the next two lines to start eclipse.
set PATH=%PATH%;C:\OSGeo4W64\apps\qgis\bin;C:\ProgramData\Oracle\Java\javapath
C:\Users\tnauss\eclipse\java-oxygen\eclipse\eclipse.exe


