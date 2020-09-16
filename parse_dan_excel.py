#!/usr/bin/env python3
import pandas as pd
import sys

talb = pd.read_excel("misc/cancer_FOROUTPUT_checked.xlsx", sheet_name="TALB", skiprows=11, usecols="B:H,L:Q",
    names = ["TALB", "maori_prostate_cancer", "maori_breast_cancer", "maori_lung_cancer", "maori_male_all_cancer_40-69", "maori_female_all_cancer_45-69", "maori_all_cancer_18+",
        "non-maori_prostate_cancer", "non-maori_breast_cancer", "non-maori_lung_cancer", "non-maori_male_all_cancer_40-69", "non-maori_female_all_cancer_45-69", "non-maori_all_cancer_18+"]
)

talb.to_csv("TALB_cancer.csv", index=False)

ward = pd.read_excel("misc/cancer_FOROUTPUT_checked.xlsx", sheet_name="WARD", skiprows=13, usecols="B:H,L:Q",
    names = ["WARD", "maori_prostate_cancer", "maori_breast_cancer", "maori_lung_cancer", "maori_male_all_cancer_40-69", "maori_female_all_cancer_45-69", "maori_all_cancer_18+",
        "non-maori_prostate_cancer", "non-maori_breast_cancer", "non-maori_lung_cancer", "non-maori_male_all_cancer_40-69", "non-maori_female_all_cancer_45-69", "non-maori_all_cancer_18+"]
)

ward.to_csv("WARD_cancer.csv", index=False)