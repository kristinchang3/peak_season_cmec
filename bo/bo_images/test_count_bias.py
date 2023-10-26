import numpy as np
import os
import json
from pcmdi_metrics.variability_mode.lib import tree
from pcmdi_metrics.io.base import Base
from basin_definition import basin
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pcmdi_metrics.graphics import portrait_plot


def lon_swap(lonw):
    lonw = ( (lonw + 180) % 360) - 180
    return lonw

region_list = ['NPacific','SPacific','NAtlantic','SAtlantic','Indian']
#region  = 'NPacific'
region  = 'NAtlantic'


dir = "/pscratch/sd/d/dong12/"
fn_ref = dir+"ERA5_stats_out.txt"  
filelist = dir+"list/metrics_stats_list.txt"

field_list = ['lat','lon','area','width','length']

def character_loop( region, fn_ref, filelist ):

    lats,latn,lonw,lone = basin(region)
    print("lat, lon, = ", lats, latn, lonw, lone)

    data = np.loadtxt(fn_ref)
    
    data = data[(data[:,2]<=2675)]
    
    columns = data[:, 0:5]  # 4th, 5th, 6th, 7th, and 8th columns


    if lonw > lone:
        filtered_data = columns[(columns[:, 3] > lats) & (columns[:, 3] < latn) &
                                ( (columns[:, 4] > lonw) | (columns[:, 4] < lone) ) ]
    else:
        filtered_data = columns[(columns[:, 3] > lats) & (columns[:, 3] < latn) &
                                (columns[:, 4] > lonw) & (columns[:, 4] < lone)]
    
    
    print("----------")

    #=================================
    
    metrics = np.empty([3,6])
    
    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})
    
    
    model_list = []
    
    with open(filelist, 'r') as file:
        jj = -1 
        for line in file:
            jj += 1
            filename = dir+"list/"+line.strip()
    
            print("filename = ", filename)
    
            data = np.loadtxt(filename)
            
            data = data[(data[:,2]<=2675)]
            
            columns = data[:, 0:5]  # 4th, 5th, 6th, 7th, and 8th columns
            
    
            if lonw > lone:
                cmip6_data = columns[(columns[:, 3] > lats) & (columns[:, 3] < latn) &
                                        ( (columns[:, 4] > lonw) | (columns[:, 4] < lone) ) ]
            else:
                cmip6_data = columns[(columns[:, 3] > lats) & (columns[:, 3] < latn) &
                                (columns[:, 4] > lonw) & (columns[:, 4] < lone)]
            
            
            #=================================
            
            #for i in range(columns.shape[1]):

            a = len(cmip6_data[:,0])
            #b = filtered_data[-1,0]
            b = len(filtered_data[:,0])

            na = cmip6_data[-1,2]
            nb = filtered_data[-1,2]
            
            print("a = ", a, "  b = ", b)
            print("na = ", na, "  nb = ", nb)

            na = np.round(na/4/365)
            nb = np.round(nb/4/365)

            print("na = ", na, "  nb = ", nb)

            bias = (a/na - b/nb) / (a/na)

            print("bias = ", bias)
            
            #z = bias/np.sqrt(np.var(a)/na + np.var(b)/nb)
        
            metrics[0,jj] = float_formatter(bias) 
            #metrics[1,i] = float_formatter(std)
            #metrics[2,i] = z
            
#                plot_hist(b, region, model_name, field_list[i], j, i)

#            metrics_all = np.append(metrics_all, metrics[np.newaxis,:,:], axis=0)
            
    

    #return result_dict
    #return metrics_all[1:,0,0]
    return metrics[0,:]



dir = "/pscratch/sd/d/dong12/"
fn_ref = dir+"ERA5_stats_out.txt"
filelist = dir+"list/metrics_stats_list.txt"

narr = np.empty([6,len(region_list)])

for k in range(len(region_list)):

    region = region_list[k]
    print("region = ", region)

    obs_dict = character_loop( region, fn_ref, filelist)

    narr[:,k] = obs_dict

#metrics_all = metrics[np.newaxis, :, :]
#metrics_all = np.append(metrics_all, metrics[np.newaxis,:,:], axis=0)

print(narr)
#narr = narr


#np.savetxt('hist_NAtlantic.txt', narr)
print("save data done!!!!!!!!")

region_list = ['N. Pacific','S. Pacific','N. Atlantic','S. Atlantic','Indian Ocean']

yaxis_labels = ["BCC-CSM2-MR","CanESM2","CCSM4","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]#,'IPSL-CM5A-LR', 'IPSL-CM5B-LR', 'IPSL-CM6A-LR']

xaxis_labels = field_list
xaxis_labels[0] = 'lat'
xaxis_labels[1] = 'lon'
xaxis_labels[2] = 'area'
xaxis_labels[3] = 'width'
xaxis_labels[4] = 'length'

maxvalue = np.max(narr)
minvalue = np.min(narr)
maxvalue = max(maxvalue, minvalue*-1)
maxvalue *= 0.7
minvalue = maxvalue*-1

fig, ax, cbar = \
portrait_plot(narr,
              xaxis_labels=region_list,
              yaxis_labels=yaxis_labels,
              annotate=True,
#              annotate_data = parr, 
              cbar_label='normalized bias (Z-Score)',
              vrange = (minvalue, maxvalue), 
              logo_off = True)

ax.set_title( 'AR count bias (relative wrt ERA5)', fontsize=20, color="black")

plt.tight_layout()
plt.savefig('AR_count_plot.png')
plt.show()


#result_dict = character_loop( region, filename, filelist )
#
#cwd = os.getcwd() 
#
#AR_metrics_to_json(
#    cwd,
#    json_fout,
#    result_dict,
#    cmec_flag=True,
#    )
