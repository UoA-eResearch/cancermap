#!/usr/bin/env python3

import pandas as pd
import glob

files = glob.glob("misc/*")

target_sheets = ["DataDemographic", "L_CancerbyDemo", "L_SubgrpReg"]

DHB_lookup = [
"Northland",
"Waitemata",
"Auckland",
"Counties Manukau",
"Waikato",
"Lakes",
"Bay of Plenty",
"Tairawhiti",
"Hawke's Bay",
"Taranaki",
"MidCentral",
"Whanganui",
"Capital & Coast",
"Hutt Valley",
"Wairarapa",
"Nelson Marlborough",
"West Coast",
"Canterbury",
"South Canterbury",
"Southern",
]

results = []

for filename in files:
    df = pd.read_excel(filename, sheet_name=None)
    sheet = [k for k in df.keys() if k in target_sheets]
    if sheet:
        print(filename, sheet)
        df = df[sheet[0]]
        if "2012" in filename:
            df = pd.read_excel(filename, sheet_name="L_SubgrpReg", skiprows=2009, nrows=(3968-2009))
            df["DHB"] = df["DHBRptID"].apply(lambda x: DHB_lookup[int(x) - 1] if x != 99 and not pd.isna(x) else None)
            df["Year"] = 2012
            df["Cases"] = df["CountOfID"]
        elif "2013" in filename:
            df = pd.read_excel(filename, sheet_name="L_CancerbyDemo", skiprows=2209, nrows=(5191-2209))
            df["DHB"] = df.DHBRpt
            df["Cases"] = df.CountOfID
            df["Subgroup"] = df.Cancer
            df["Year"] = 2013
        else:
            assert len(df.Demography[df.Demography.isin(DHB_lookup)].value_counts()) == len(DHB_lookup)
            df = df[df.Demography.isin(DHB_lookup)]
            df["DHB"] = df.Demography
            if "Subgroup" not in df.keys():
                df["Subgroup"] = df["Desc"]
        results.append(df[["Year", "DHB", "Subgroup", "Sex", "Cases"]])

df = pd.concat(results)
df.DHB[df.DHB == "Not stated"] = None
df.Cases[df.Cases == "-"] = None
df["Year"] = df["Year"].astype(int)
df["Cases"] = df["Cases"].astype('Int64')
df = df[df.Sex != "AllSex"]
df = df.sort_values(by=list(df.columns), ascending=False)
df.to_csv("NZ_cancer.csv", index=False)