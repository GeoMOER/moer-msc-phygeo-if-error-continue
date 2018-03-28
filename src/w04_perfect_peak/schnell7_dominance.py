dgm = gdal.Open(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")
ar = raster2array(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")
dgm = gdal.Open(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")


#%%
import math
import gdal, ogr, osr, os
import numpy as np

# nach https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#replace-no-data-value-of-raster-with-new-value
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()

#%%
ar = raster2array(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")
#%%
#gipfelsuche entweder im gis oder hiermit
def maxprozeile(ar):
    for y in range(len(ar)):
        print(y, max(ar[y]))
#%%

#dateityp des arrays (float32) ist anders als float (2041.27 z.B.), logische abfragen in py daher immer FALSE
#wo ist die zelle mit 'wert' gerundet auf nachkommastelle r in dgm_ar
    #koennen auch mehrere sein!
def woist(wert, r, dmg_ar):
    for y in range(len(ar)):
        for x in range(len(ar[0])):
            if round(float(ar[y][x]), r) == wert:
                print("zeile:", y, "spalte:", x)
                return([y, x])
    
#%%
gipf = woist(2041.27, 2, ar)


#%%
#z,s, gipfelkoordinaten, y,x von dominanz()
def distanz(z,s,y,x):
    dis = math.sqrt((z-y)**2 + (s-x)**2)    
    return(dis)

#zeile, spalte(des gipfels), array des dgm, step grosse des fensters minimale dis wird ausgesucht, res = zellengroesse
def dominanz(z,s, dgm_ar, step, res):
    end_list = []
    for y in range(z-step, z+step+1):
        for x in range(s-step, s+step+1):
            if dgm_ar[z][s] < dgm_ar[y][x]:
                dissi = distanz(z,s,y,x)
                end_list.append(dissi)                
    if len(end_list)> 0:
        #print(end_list)
        print("dominanz: ", min(end_list)*res)
        return(min(end_list)*res)
    else:
        print("""Alarm!Alarm!Alarm!Alarm!Alarm!Alarm! \n\n       setze 'step' groesser!\n\n====================================""")
        

        
        
#%%


#%%
dominanz(80,65,ar,64,200)
    
#%%
def eigenstand(h, d, p):
  if d < 100000:
    E1 = math.log(h/8848, 2) + math.log(d/100000, 2) + math.log(p/h, 2)
    E = -(E1/3)
  else:
    E1 = math.log(h/8848, 2) + math.log((p/h), 2)
    E = -(E1/3)
  return(E)  
  
#%%
def estand(y,x,ar,step,res,p):
    h = float(ar[y][x])
    d = dominanz(y,x,ar,step,res)
    print("eigenstand: ", eigenstand(h,d,p))
    return(eigenstand(h,d,p))
    

#%%
 #300 wird hier yum test angenommen
 #gipfel hat nahegelegen hoeheren gipfelnachbar deswegen reicht 5 (3 ginge auch)

estand(78,60,ar,5,200,300)
#%%
#naechster hoeherer gipfel viel wieter weg; 

estand(80,65,ar,65,200,300)
#%%
#der Ansatz, das Fenster schrittweise zu vergroessern ist nicht ideal:
#liegt der erste Punkt > Gipfel in der diagonalen des Quadrats ist die Entfernung
#e = x*(wurzel 2)
#ein wesentlich groessere Fenster kann aber trotzdem einen naeheren Punkt enthalten
#(wenn nur in x bzw y Richtung gegangen wird)
#Bsp fenstergroesse 50
distanz(0,0,50,50)
# = 70,71
#also ein fenster der groesse 70 kann eine naehere distanz (70<70,71) haben
distanz(0,0,0,70)
# = 70
#bsp von werten fuer 80|65
#14990.663761154807 53 / erster treffer
#13172.69904006009 60
#12801.562404644206 64
#12801.562404644206 100
#12801.562404644206 125 /letzter treffer weil .tif zu klein
#Erkenntnis: das Fenster sollte eher die maximale Ausdehnung oder zumindest eine sehr grosse haben
#oder die groesse erhoeht sich um xneu = xalt * (wurzel 2) auf die naechste ganzzahl aufgerundet
#beim Beispiel von 50 also auf 71
#%% beta dominanz| erst wird nach dem ersten treffer gesucht wobei sich das fenster um 1 / schritt erhöht,
#von dieser groesse dann xneu = xalt * (wurzel 2) berechnet und damit sichergestellt, dass die punkte richtig erkannt werden
#zeile, spalte(des gipfels), array des dgm, step grosse des fensters minimale dis wird ausgesucht, res = zellengroesse
def dominanzB(z,s, dgm_ar, step=1, res):
    end_list = []
    while len(end_list) == 0:
      for y in range(z-step, z+step+1):
          for x in range(s-step, s+step+1):
              if dgm_ar[z][s] < dgm_ar[y][x]:
                  dissi = distanz(z,s,y,x)
                  end_list.append(dissi)
      step = step+1
    end_list = []
    step = int((step-1) * math.sqrt(2)) + 1
    for y in range(z-step, z+step+1):
          for x in range(s-step, s+step+1):
              if dgm_ar[z][s] < dgm_ar[y][x]:
                  dissi = distanz(z,s,y,x)
                  end_list.append(dissi)                    
    if len(end_list)> 0:
        #print(end_list)
        print("dominanz: ", min(end_list)*res)
        return(min(end_list)*res)
    else:
        print("""Alarm!Alarm!Alarm!Alarm!Alarm!Alarm! \n\n       setze 'step' groesser!\n\n====================================""")




