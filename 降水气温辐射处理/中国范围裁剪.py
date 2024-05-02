import xarray as xr
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
import numpy as np

# 读取矢量边界
gdf = gpd.read_file('E:\\Data-py\\shp\\全国shp\\国界线\\国界线-84.shp')

# 读取NetCDF数据
ds = xr.open_dataset('download.nc')

# 使用rioxarray为数据集添加CRS
import rioxarray
ds = ds.rio.write_crs("epsg:4326")  # 假设NetCDF数据是WGS84坐标系

# 如果CRS不匹配，转换GeoDataFrame的CRS
if ds.rio.crs != gdf.crs:
    gdf = gdf.to_crs(ds.rio.crs)

# 计算经度和纬度的分辨率
longitude_resolution = ds['longitude'].diff(dim='longitude').mean().item()
latitude_resolution = ds['latitude'].diff(dim='latitude').mean().item()

# 创建一个基于矢量数据的mask
mask = geometry_mask([geom for geom in gdf.geometry],
                     out_shape=(len(ds['latitude']), len(ds['longitude'])),
                     transform=from_origin(ds['longitude'].min().item(), ds['latitude'].max().item(),
                                           longitude_resolution, latitude_resolution),
                     invert=True)

# 将mask转换为DataArray
mask_da = xr.DataArray(mask, dims=["latitude", "longitude"], coords={"latitude": ds['latitude'], "longitude": ds['longitude']})

# 应用mask裁剪数据
clipped_ds = ds.where(mask_da, drop=True)

# 保存裁剪后的数据
clipped_ds.to_netcdf('D:\\Python\\data\\clipped.nc')
