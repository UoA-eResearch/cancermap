#!/usr/bin/env python3
import pandas as pd
import sys
import json

with open("data/TALB_2018.geojson") as f:
  geojson = json.load(f)

for i in range(len(geojson["features"])):
  geojson["features"][i]["properties"]["cancer"] = {}

def find_talb(name):
  if pd.isna(name):
    return
  for i,f in enumerate(geojson["features"]):
    if f["properties"]["TALB2018_1"].startswith(name.replace(".", "")):
      return i
  print(name + " not found")

year_bands = ["2010-2012", "2013-2015", "2016-2018"]
cancer_types = ["breast", "prostate", "lung"]
maori = ["maori", "non-maori", "total"]
keys = ["TALB"]
for c in cancer_types:
  for m in maori:
    for y in year_bands:
      keys.append(c + m + y)

numerator = pd.read_excel("misc/annual_counts_OUTPUT - Checked.xlsx", sheet_name="TALB", skiprows=10, nrows=88, names = keys)
print(numerator)
cancer_types = ["females 45-69 all cancer", "males 40-69 all cancer", "total 18+ all cancer"]
keys = ["TALB"]
for c in cancer_types:
  for m in maori:
    for y in year_bands:
      keys.append(c + m + y)
denominator = pd.read_excel("misc/annual_counts_OUTPUT - Checked.xlsx", sheet_name="TALB", skiprows=99, nrows=88, names = keys)
print(denominator)

for i, row in numerator.iterrows():
    print(row["TALB"])
    i = find_talb(row["TALB"])
    if i:
      row = dict(row)
      del row["TALB"]
      geojson["features"][i]["properties"]["cancer"].update(row)

for i, row in denominator.iterrows():
    print(row["TALB"])
    i = find_talb(row["TALB"])
    if i:
      row = dict(row)
      del row["TALB"]
      geojson["features"][i]["properties"]["cancer"].update(row)

with open("data/TALB_2018.geojson", "w") as f:
  json.dump(geojson, f)