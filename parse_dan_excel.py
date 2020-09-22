#!/usr/bin/env python3
import pandas as pd
import sys
import json

with open("data/TALB_2018.geojson") as f:
  geojson = json.load(f)

def find_talb(name):
  for i,f in enumerate(geojson["features"]):
    if f["properties"]["TALB2018_1"] == name:
      return i
  print(f + " not found")
  exit(1)

talb = pd.read_excel("misc/cancer_FOROUTPUT_checked.xlsx", sheet_name="TALB", skiprows=11, usecols="B:H,L:Q",
    names = ["TALB", "maori_prostate_cancer", "maori_breast_cancer", "maori_lung_cancer", "maori_male_all_cancer_40-69", "maori_female_all_cancer_45-69", "maori_all_cancer_18+",
        "non-maori_prostate_cancer", "non-maori_breast_cancer", "non-maori_lung_cancer", "non-maori_male_all_cancer_40-69", "non-maori_female_all_cancer_45-69", "non-maori_all_cancer_18+"]
)

for i, row in talb.iterrows():
    print(row["TALB"])
    if pd.isna(row["TALB"]):
        continue
    i = find_talb(row["TALB"])
    row = dict(row)
    del row["TALB"]
    geojson["features"][i]["properties"]["cancer"] = row

with open("data/TALB_2018.geojson", "w") as f:
  json.dump(geojson, f)