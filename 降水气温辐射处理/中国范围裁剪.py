import xarray as xr
import rioxarray
import geopandas as gpd
from shapely.geometry import mapping

ds = xr.open_dataset('download.nc')
# ds['lon'] = ds['lon'] - 180 # 根据实际NC文件的经度范围确定是否开启这一行
shp = gpd.read_file(r"D:\\Python\\data\\china.shp")

ds.rio.write_crs("epsg:4326", inplace=True)
ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)

ds = ds.rio.clip(shp.geometry.apply(mapping),shp.crs,drop=False)

ds.to_netcdf(r'D:\Python\data\clip_nc.nc') # 保存NC文件

