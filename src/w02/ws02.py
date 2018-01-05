import pandas as pd

url = "http://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

# help(pd.read_fwf)
oni = pd.read_fwf(url, widths = [5, 5, 7, 7])

### w02-1.1 -----

sst = oni['TOTAL'].tolist()

out = 0.0
for i in range(len(sst)):
    out += sst[i]

ltm = out / len(sst)


### w02-1.2 -----

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


### w02-2.1 -----

w = m = s = v = 0

for i in range(len(anm)):
    val = anm[i]
    if val >= 0.5 and val < 1.0:
        w += 1
    elif val >= 1.0 and val < 1.5:
        m += 1
    elif val >= 1.5 and val < 2.0:
        s += 1
    elif val >= 2.0:
        v += 1

print("There were", w, "weak,", m, "moderate,", s, "strong, and", v, "very strong months with warm ENSO conditions.")


### analogous for w02-2.2 -----

dct = {"Weak El Nino":w, "Moderate El Nino":m, "Strong El Nino":s, "Very Strong El Nino":v}


