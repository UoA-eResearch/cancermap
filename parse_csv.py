#!/usr/bin/env python3

import csv
import sys
import re
import json

files = sys.argv[1:]
o = {}

for fn in files:
  with open(fn) as f:
    reader = csv.DictReader(f)
    for row in reader:
#"Year","Area_type","Area_code","Area_description","Cigarette_smoking_behaviour_code","Cigarette_smoking_behaviour_description","Sex_code","Sex_description","Age_group_life_cycle_groups_code","Age_group_life_cycle_groups_description","Maori_ethnic_group_indicator_summary_code","Maori_ethnic_group_indicator_summary_description","Census_usually_resident_population_count_aged_15_years_and_over","Cigarette_smoking_behaviour_by_Maori_ethnic_group_indicator_summary_percent","Cigarette_smoking_behaviour_by_sex_percent","Cigarette_smoking_behaviour_percent"
      if row["Area_type"] == "Statistical Area 2":
        code = row["Area_code"]
        year = row["Year"]
        smoker = row["Cigarette_smoking_behaviour_description"]
        age_group = row["Age_group_life_cycle_groups_description"]
        sex = row["Sex_description"]
        maori = row["Maori_ethnic_group_indicator_summary_description"]
        if maori != "Total":
          continue
        count = row["Census_usually_resident_population_count_aged_15_years_and_over"]
        if count == "C":
          count = None
        else:
          count = int(count)
        if code not in o:
          o[code] = {
            "Male": {},
            "Female": {},
            "Total": 0
          }
        if smoker == "Total stated" and sex == "Total" and age_group == "Total" and count:
          o[code]["Total"] += count
        if smoker in ["Total", "Total stated", "Not elsewhere included"] or age_group in ["Under 15 years", "Total"] or sex == "Total":
          continue
        if smoker not in o[code][sex]:
          o[code][sex][smoker] = {}
        o[code][sex][smoker][age_group] = count

print(json.dumps(o, sort_keys=True, indent=2))
