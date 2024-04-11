import xarray as xr

# 打开NetCDF文件
ds = xr.open_dataset('download.nc')

# 打印经度范围
if 'lon' in ds.variables:
    lon_min = ds['lon'].min().values
    lon_max = ds['lon'].max().values
    print(f"经度范围: {lon_min} 到 {lon_max}")
elif 'longitude' in ds.variables:
    lon_min = ds['longitude'].min().values
    lon_max = ds['longitude'].max().values
    print(f"经度范围: {lon_min} 到 {lon_max}")
else:
    print("未找到经度变量")

# 打印纬度范围
if 'lat' in ds.variables:
    lat_min = ds['lat'].min().values
    lat_max = ds['lat'].max().values
    print(f"纬度范围: {lat_min} 到 {lat_max}")
elif 'latitude' in ds.variables:
    lat_min = ds['latitude'].min().values
    lat_max = ds['latitude'].max().values
    print(f"纬度范围: {lat_min} 到 {lat_max}")
else:
    print("未找到纬度变量")
