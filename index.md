---
layout: default
#altair-loader:
#  altair-chart-1: "charts/measlesAltair.json"
hv-loader:
  hv-chart-1: ["charts/peak_plot16.html", "800"] # second argument is the desired height
  hv-chart-2: ["charts/peak_plot17.html", "800"]
#folium-loader:
#  folium-chart-1: ["charts/foliumChart.html", "400"] # second argument is the desired height
---
<div style="text-align: center;" markdown="1">
# Welcome! 

This is an internal test page with an interactive data visualization. 
</div>
<div style="text-align: center;" markdown="1">
# AR Regions 
### MJJAS 
<p align="center">
  <img src="images/MJJAS.png" width="400"/>
</p>
</div>
<div style="text-align: center;" markdown="1">
### NDJFM 
<p align="center">
  <img src="images/NDJFM.png" width="400"/>
</p>
</div>
<div style="text-align: center;" markdown="1">
# Portrait Plot 

Visualizing the Peak Season CMEC data: 
</div>
<div id="hv-chart-1"></div>
<div id="hv-chart-2"></div>
