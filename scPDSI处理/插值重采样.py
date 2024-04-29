import numpy as np
import xarray as xr
from scipy.interpolate import griddata
from pykrige.ok import OrdinaryKriging

data=xr.open_dataset('scpdsi_reshape.nc')
scpdsi=data['scpdsi']

#提取经纬度坐标
lon=scpdsi.coords['longitude'].values
lat=scpdsi.coords['latitude'].values

#创建新的经纬度值，存储为numpy数组
new_lon=np.arange(lon.min(),lon.max(),0.009)
new_lat=np.arange(lat.min(),lat.max(),0.009)

#将原始网格转化为一维数组
values=scpdsi.values.flatten()
grid_lon,grid_lat=np.meshgrid(lon,lat)
grid_lon=grid_lon.flatten()
grid_lat=grid_lat.flatten()

#执行克里金插值，使用球形变异模型，z是插值得到的数据网格，ss是估计的方差网格
OK=OrdinaryKriging(grid_lon,grid_lat,values,variogram_model='spherical',verbose=False,enable_plotting=False)
z,ss=OK.execute('grid',new_lon,new_lat)

#创建新的数组，设置经纬度，设置维度名称
new_scpdsi=xr.DataArray(z,coords=[new_lat,new_lon],dims=["lat","lon"])
print(new_scpdsi)