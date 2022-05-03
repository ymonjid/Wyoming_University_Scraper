#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:30:42 2022

@author: ymonjid
"""

import pandas as pd
import json

# Path to chrome driver
path = "/home/ymonjid/Desktop/chromedriver_linux64/chromedriver"

# Number of equivalences to extract
num_equivs = 10

# Data scraping
import Wyoming_University_Scraper as WUS
college = "Wyoming University"
url = "https://wyossb.uwyo.edu/bnrprod/bwckytfc.p_display_transfer_catalog"
df = WUS.get_equivalences(college, url, num_equivs, True, path)

# Write the DataFrame to json format
result = df.to_json(orient="records")
parsed = json.loads(result)
results = json.dumps(parsed, indent=4) 
