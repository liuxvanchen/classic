import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取下载的 NetCDF 文件
data = xr.open_dataset('download.nc')

# 提取温度数据
temperature = data['t2m']
radiation = data['ssrd']
precipitation = data['tp']


# 绘制温度数据
plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
temperature.mean(dim='time').plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

# 添加中国的轮廓线
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
ax.add_feature(cfeature.LAND.with_scale('50m'))
ax.add_feature(cfeature.LAKES.with_scale('50m'))

# 设置地图范围（中国）
ax.set_extent([73, 135, 18, 53])

# 显示地图
plt.title('Mean Temperature with China Contour')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# 绘制辐射数据
plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
radiation.mean(dim='time').plot(ax=ax, transform=ccrs.PlateCarree(), cmap='Spectral')

# 添加中国的轮廓线
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
ax.add_feature(cfeature.LAND.with_scale('50m'))
ax.add_feature(cfeature.LAKES.with_scale('50m'))

# 设置地图范围（中国）
ax.set_extent([73, 135, 18, 53])

# 显示地图
plt.title('Mean Surface Solar Radiation Downwards with China Contour')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


#绘制降水量数据
plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
precipitation.mean(dim='time').plot(ax=ax, transform=ccrs.PlateCarree(), cmap='PuBu')

# 添加中国的轮廓线
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
ax.add_feature(cfeature.LAND.with_scale('50m'))
ax.add_feature(cfeature.LAKES.with_scale('50m'))

# 设置地图范围（中国）
ax.set_extent([73, 135, 18, 53])

# 显示地图
plt.title('Mean Total Precipitation with China Contour')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()