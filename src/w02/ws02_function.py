import pandas as pd

def getONI():
    url = "http://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
    # help(pd.read_fwf)
    oni = pd.read_fwf(url, widths = [5, 5, 7, 7])
    return(oni)

def meanSST(onidata):
    sst = onidata['TOTAL'].tolist()
    out = 0.0
    for i in range(len(sst)):
        out += sst[i]
    ltm = out / len(sst)
    return(ltm)


def fovsE(onidata):
    anm = oni['ANOM'].tolist()
    anm[:10]
    ssn = oni['SEAS'].tolist()
    yrs = oni['YR'].tolist()
    n = 0
    while anm[n] <= 2:
        n += 1
    print("The", ssn[n], "season in", yrs[n], "exceeded strong El Nino conditions.\n")
    n = 0
    while anm[n] >= -2:
        n += 1
    print("The", ssn[n], "season in", yrs[n], "exceeded strong La Nina conditions.\n")


def warmENSO(onidata):
    w = m = s = v = 0
    onidata = onidata['ANOM'].tolist()
    onidata[:10]
    for i in range(len(onidata)):
        val = onidata[i]
        if val >= 0.5 and val < 1.0:
            w += 1
        elif val >= 1.0 and val < 1.5:
            m += 1
        elif val >= 1.5 and val < 2.0:
            s += 1
        elif val >= 2.0:
            v += 1
    print("There were", w, "weak,", m, "moderate,", s, "strong, and", v, "very strong months with warm ENSO conditions.")



oni = getONI()
ltm = meanSST(oni)
fovsE(oni)
warmENSO(oni)

