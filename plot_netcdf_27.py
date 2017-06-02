from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

model_in = 'D:/Jupyter_Notebooks/Testing/data/geo_em.d01.boulder_creek_1km.nc'
model_out = 'D:/Jupyter_Notebooks/Testing/data/2014081216_LDASOUT_DOMAIN1'
geo = Dataset(model_in, mode='r')
nc = Dataset(model_out, mode='r')

lats = geo.variables['XLAT_M'][0,::-1,:]
lons = geo.variables['XLONG_M'][0,::-1,:]

lon_0 = lons.mean()
lat_0 = lats.mean()

m = Basemap(width=5000000,height=3500000,
            resolution='i',epsg=26954,\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0, llcrnrlon=-105.8,llcrnrlat=39.6,urcrnrlon=-104.7,urcrnrlat=40.4)
            
#lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lons, lats)

var = 'SFCEVP' # Enter the variable id to plot
var_data = np.array(nc.variables[var][0,::-1,:])
var_units = nc.variables[var].units
var_desc = nc.variables[var].description

# mask invalid data
var_plot = np.ma.masked_less(var_data, -9999)

print(nc.variables[var])

#map = Basemap(projection='merc',llcrnrlon=-93.,llcrnrlat=35.,urcrnrlon=-73.,urcrnrlat=45.,resolution='i') # projection, lat/lon extents and resolution of polygons to draw
# resolutions: c - crude, l - low, i - intermediate, h - high, f - full
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
m.drawcounties() # you can even add counties (and other shapefiles!)
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
cs = m.pcolor(xi,yi,np.squeeze(var_plot))

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(var_units)

# Add Title
plt.title(var_desc)
cs.set_alpha(0.7)

plt.show()
nc.close()
geo.close()