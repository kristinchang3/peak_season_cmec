import numpy as np
import pandas as pd
import json
import panel as pn
from matplotlib import pyplot as plt
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool

angle = np.array([[  0,  86, 199],
       [ 23, 111, 271],
       [ 16,  97, 226],
       [ 17, 103, 159]])

model_names = ["CanESM2","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]
region_names = ['California','S.America', 'W.Africa']

da = pd.DataFrame(data=angle, index=model_names, columns=region_names)

dd = da.stack()
dd = dd.reset_index()
dd = dd.rename(columns={"level_0": "model", "level_1": "region", 0 :"peak"})
ddd = dd['peak'].values


img_links = ['https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/BCC-CSM2-MR.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/ERA5.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MERRA2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MRI-ESM2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/NorESM1.png', 
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/BCC-CSM2-MR.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/ERA5.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MERRA2.png'
             ]

dd['img'] = img_links

print(dd)

# adjust pandas settings to view full column width
pd.set_option('max_colwidth', 1000)

# html for custom hover tool
hover = HoverTool(tooltips="""
    <div>
        <div>
            <img src="@img" width=400 style="float: left; margin: 0px 15px 15px 0px; border="2"></img>
        </div>
    </div>

""")

peak_plot11 = dd.hvplot.heatmap(y='model',
                       x='region',
                       C='peak',
                       hover_cols = ['img'],
                       tools = [hover],
                       height = 500,
                       width=550,
                       colorbar=True,
                       clabel = 'peak day',
                       xaxis='top',
                       cmap='blues').opts(xrotation=45, fontsize={
                           'labels': 14,
                           'xticks': 14,
                           'yticks': 14
                       })
peak_plot11
