import numpy as np
import os
import json
from pcmdi_metrics.variability_mode.lib import tree
from pcmdi_metrics.io.base import Base
#from basin_definition import basin
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pcmdi_metrics.graphics import portrait_plot
import pandas as pd
import panel as pn
import holoviews as hv
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool

float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})


narr0 = np.loadtxt("../bo/bo_data/output_spatial_corr.txt")
narr0 = np.around(narr0, decimals=1)
narr = narr0.reshape(6,-1)
narr = np.round(narr, decimals=2)

field_list = ['lat','lon','area','width','length']
region_list = ['N. Pacific','S. Pacific','N. Atlantic','S. Atlantic','Indian Ocean']
yaxis_labels = ["BCC-CSM2-MR","CanESM2","CCSM4","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]#,'IPSL-CM5A-LR', 'IPSL-CM5B-LR', 'IPSL-CM6A-LR']
xaxis_labels = field_list

maxvalue = np.max(narr)
minvalue = np.min(narr)
maxvalue = max(maxvalue, minvalue*-1)
maxvalue *= 0.7
minvalue = maxvalue*-1
# 
# fig, ax, cbar = \
# portrait_plot(narr,
#               xaxis_labels=xaxis_labels,
#               yaxis_labels=yaxis_labels,
#               annotate=True,
# #              annotate_data = parr, 
#               cbar_label='normalized bias (Z-Score)',
#               vrange = (minvalue, maxvalue), 
#               logo_off = True)
# 
# ax.set_title( region, fontsize=20, color="black")
# 
# plt.tight_layout()
# ##plt.savefig('AR_character_'+region+'.png')
# plt.show()
# 


region = 'NAtlantic'

model_names = ["BCC-CSM2-MR","CanESM2","CCSM4","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]#,'IPSL-CM5A-LR', 'IPSL-CM5B-LR', 'IPSL-CM6A-LR']
model_names = ["CanESM2","CCSM4","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0","BCC-CSM2-MR"]
region_names = region_list
field_names = field_list

da = pd.DataFrame(data=narr, index=model_names, columns=region_list)

dd = da.stack()
dd = dd.reset_index()
dd = dd.rename(columns={"level_0": "model", "level_1": "region", 0 :"peak"})

#print(dd)

img_path = 'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/bo/bo_images/'
img_links = []

for i, model in enumerate(model_names):
    #for j, field in enumerate(field_names):
    for j, region in enumerate(region_list):
        filename = img_path+'fig_freq_'+str(i)+"_"+str(j)+'.png'
        img_links.append(filename)


dd['img'] = img_links


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

# Use number of models and fields to determine cell size
num_models = len(dd['model'].unique())
num_fields = len(dd['region'].unique())

cell_height = 1/num_models
cell_width = 1/num_fields

# set desired figure size
desired_width = 3000
desired_height = 3000

# calculate final width and height based on above parameters
adjusted_width = round(int(cell_width * desired_width), -1)
adjusted_height = round(int(cell_height * desired_height), -1)

peak_plot11 = dd.hvplot.heatmap(y='model',
                       x='region',
                       C='peak',
                       hover_cols = ['img'],
                       tools = [hover],
                       height = adjusted_height,
                       width=adjusted_width,
                       colorbar=True,
                       clabel = 'spatial correlation',
                       xaxis='top',
#                       clim = (minvalue, maxvalue),
                       clim = (0.8, 1),
#                       cmap='blues').opts(xrotation=45, fontsize={
#                       cmap='RdBu_r').opts(xrotation=45, fontsize={
                       cmap='Oranges_r').opts(xrotation=45, fontsize={
                           'labels': 14,
                           'xticks': 14,
                           'yticks': 14
                       })

peak_plot11 = peak_plot11 * hv.Labels(peak_plot11)

plt.show()

#hvplot.save(peak_plot11, 'bo_charts/peak_plot31.html')
hvplot.save(peak_plot11, '../charts/peak_plot32.html')
