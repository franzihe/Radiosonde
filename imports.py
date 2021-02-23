# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import os
import numpy as np
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import xarray as xr
from metpy.units import units
from metpy.plots import SkewT
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

import functions as fct
