import xarray as xr
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import rasterize

# 读取NetCDF数据
ds1 = xr.open_dataset(r'download.nc')
time = ds1.time.data # time 变量名
lat = ds1.latitude.data # lat 变量名
lon = ds1.longitude.data # lon 变量名
tp = np.array(ds1.tp.data)

# 读取Shapefile
gdf = gpd.read_file(r'E:\Data-py\shp\全国shp\国界线\国界线-84.shp')
gdf = gdf.to_crs('EPSG:4326') # 正确的CRS初始化方法

# 创建地理掩码
transform = rasterio.transform.from_origin(lon.min(), lat.max(), lon[1] - lon[0], lat[1] - lat[0])
mask = rasterize([(geom, 1) for geom in gdf.geometry], out_shape=(len(lat), len(lon)), transform=transform, fill=0, all_touched=True, dtype='float32')
mask[mask == 0] = np.nan # 将掩码中的0转换为nan

# 应用掩码
tp_masked = tp * mask[np.newaxis, :, :] # 假设tp是三维的，时间维度在前

# 创建新的xarray数据集
ds3 = xr.Dataset({
'tp': (('time', 'lat', 'lon'), tp_masked),
'lat': (('lat',), lat),
'lon': (('lon',), lon),
'time': (('time',), time)
})

# 保存裁剪后的数据
ds3.to_netcdf(r'D:\Python\data\clipped_tp.nc')
