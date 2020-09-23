#!/usr/bin/env python3

import csv
import sys
import re
import json

with open("data/TALB_2018.geojson") as f:
  geojson = json.load(f)

def find_talb(name):
  for i,f in enumerate(geojson["features"]):
    if f["properties"]["TALB2018_1"] == name:
      return i
  print(f + " not found")
  exit(1)

for i, f in enumerate(geojson["features"]):
  del geojson["features"][i]["properties"]["smoking"]

with open("data/2018_census/2018-census-place-summaries-health-table2-2018-csv.csv") as f:
  reader = csv.DictReader(f)
  for row in reader:
#"Year","Area_type","Area_code","Area_description","Cigarette_smoking_behaviour_code","Cigarette_smoking_behaviour_description","Sex_code","Sex_description","Age_group_life_cycle_groups_code","Age_group_life_cycle_groups_description","Maori_ethnic_group_indicator_summary_code","Maori_ethnic_group_indicator_summary_description","Census_usually_resident_population_count_aged_15_years_and_over","Cigarette_smoking_behaviour_by_Maori_ethnic_group_indicator_summary_percent","Cigarette_smoking_behaviour_by_sex_percent","Cigarette_smoking_behaviour_percent"
    if row["Area_type"] == "Territorial Authority Local Board":
      area = row["Area_description"]
      if area == "Total":
        continue
      year = row["Year"]
      smoker = row["Cigarette_smoking_behaviour_description"]
      age_group = row["Age_group_life_cycle_groups_description"]
      sex = row["Sex_description"]
      maori = row["Maori_ethnic_group_indicator_summary_description"]
      count = row["Census_usually_resident_population_count_aged_15_years_and_over"]
      if count == "C":
        continue
      else:
        count = int(count)
      i = find_talb(area)
      if "smoking" not in geojson["features"][i]["properties"]:
        geojson["features"][i]["properties"]["smoking"] = {
          "maori_male_smoker": 0,
          "maori_male_non-smoker": 0,
          "maori_female_smoker": 0,
          "maori_female_non-smoker": 0,
          "non-maori_male_smoker": 0,
          "non-maori_male_non-smoker": 0,
          "non-maori_female_smoker": 0,
          "non-maori_female_non-smoker": 0,
          "total_15+": 0
        }
      if age_group != "Total":
        continue
      if smoker in ["Regular smoker", "Ex-smoker"]:
        if maori == "Maori":
          if sex == "Male":
            geojson["features"][i]["properties"]["smoking"]["maori_male_smoker"] += count
          elif sex == "Female":
            geojson["features"][i]["properties"]["smoking"]["maori_female_smoker"] += count
        elif maori == "No 'Maori' response given":
          if sex == "Male":
            geojson["features"][i]["properties"]["smoking"]["non-maori_male_smoker"] += count
          elif sex == "Female":
            geojson["features"][i]["properties"]["smoking"]["non-maori_female_smoker"] += count
      elif smoker == "Never smoked regularly":
        if maori == "Maori":
          if sex == "Male":
            geojson["features"][i]["properties"]["smoking"]["maori_male_non-smoker"] += count
          elif sex == "Female":
            geojson["features"][i]["properties"]["smoking"]["maori_female_non-smoker"] += count
        elif maori == "No 'Maori' response given":
          if sex == "Male":
            geojson["features"][i]["properties"]["smoking"]["non-maori_male_non-smoker"] += count
          elif sex == "Female":
            geojson["features"][i]["properties"]["smoking"]["non-maori_female_non-smoker"] += count
      if smoker == "Total" and maori == "Total" and sex == "Total":
        geojson["features"][i]["properties"]["smoking"]["total_15+"] += count

with open("data/2018_census/2018-census-place-summaries-popdwell-table3-2018-csv.csv") as f:
  reader = csv.DictReader(f)
  for row in reader:
    #"Year","Area_type","Area_code","Area_description","Age_group_5_year_groups_to_85_years_and_over_code","Age_group_5_year_groups_to_85_years_and_over_description","Sex_code","Sex_description","Maori_ethnic_group
#_indicator_summary_code","Maori_ethnic_group_indicator_summary_description","Census_usually_resident_population_count","Age_group_5_year_groups_to_85_years_and_over_by_Maori_ethnic_group_indicator_summary_perc
#ent","Age_group_5_year_groups_to_85_years_and_over_by_sex_percent"
      if row["Area_type"] == "Territorial Authority Local Board":
        area = row["Area_description"]
        if area == "Total":
          continue
        i = find_talb(area)
        year = row["Year"]
        age_group = row["Age_group_5_year_groups_to_85_years_and_over_description"]
        sex = row["Sex_description"]
        if sex != "Total":
          continue
        maori = row["Maori_ethnic_group_indicator_summary_description"]
        if maori == "No 'Maori' response given":
          maori = "Non-maori"
        count = row["Census_usually_resident_population_count"]
        if count == "C":
          count = None
        else:
          count = int(count)
        if "age" not in geojson["features"][i]["properties"]:
          geojson["features"][i]["properties"]["age"] = {
            "Maori": {},
            "Non-maori": {},
            "Total": {}
          }
        geojson["features"][i]["properties"]["age"][maori][age_group] = count


with open("data/TALB_2018.geojson", "w") as f:
  json.dump(geojson, f)