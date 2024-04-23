import netCDF4 as nc

dataset=nc.Dataset('scpdsi_reshape.nc')

latitudes = dataset.variables['latitude'][:]
longitudes = dataset.variables['longitude'][:]

# 计算分辨率
lat_resolution = latitudes[1] - latitudes[0]
lon_resolution = longitudes[1] - longitudes[0]

print(f"Latitude resolution: {lat_resolution}")
print(f"Longitude resolution: {lon_resolution}")

# 查看全局属性
for attr in dataset.ncattrs():
    print(attr, '=', getattr(dataset, attr))

# 查看可能包含投影信息的变量属性
for var in dataset.variables:
    print(f"Variable '{var}' attributes:")
    for attr_name in dataset.variables[var].ncattrs():
        print(f"  - {attr_name}: {getattr(dataset.variables[var], attr_name)}")


       # ?C:\Users\Lenovo\Documents\ArcGIS\Default.gdb\pf20_Resample4
