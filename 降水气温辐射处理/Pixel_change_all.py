import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import netCDF4 as nc
import cartopy.feature as cfeature

# 加载NetCDF文件
dataset = nc.Dataset('download.nc')

# 读取经度和纬度数据
longitudes = dataset.variables['longitude'][:]
latitudes = dataset.variables['latitude'][:]

# 读取温度数据
t2m = dataset.variables['t2m'][:]
tp = dataset.variables['tp'][:]
ssrd = dataset.variables['ssrd'][:]

# 将温度从开尔文转换为摄氏度,降水从m转换为mm
t2m_celsius = t2m - 273.15
tp_mm = tp * 1000

# 确定时间维度的大小
time_size = t2m_celsius.shape[0]

# 确保时间维度是12的倍数
assert time_size % 12 == 0, "时间维度不是12的整数倍，检查数据！"

# 重新组织数据为(年份, 月份, 纬度, 经度)
t2m_reshaped = t2m_celsius.reshape((-1, 12, t2m_celsius.shape[1], t2m_celsius.shape[2]))
tp_mm_reshaped = tp_mm.reshape((-1, 12, tp_mm.shape[1], tp_mm.shape[2]))
ssrd_reshaped = ssrd.reshape((-1, 12, ssrd.shape[1], ssrd.shape[2]))

# 计算每年的平均值
t2m_annual_avg = t2m_reshaped.mean(axis=1)
tp_annual_avg = tp_mm_reshaped.mean(axis=1)
ssrd_annual_avg = ssrd_reshaped.mean(axis=1)

# 计算气温、降水、辐射变化量
t2m_change = t2m_annual_avg[-1, :, :] - t2m_annual_avg[0, :, :]
tp_change = tp_annual_avg[-1, :, :] - tp_annual_avg[0, :, :]
ssrd_change = ssrd_annual_avg[-1, :, :] - ssrd_annual_avg[0, :, :]

# 创建地图
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# 绘制中国的轮廓线，solid是实线样式
ax.add_feature(cfeature.BORDERS, linestyle='solid', edgecolor='black')

# 设置颜色映射
cmap = plt.get_cmap('RdBu_r')

# 绘制气温变化量
temperature_plot = ax.pcolormesh(longitudes, latitudes, t2m_change, cmap=cmap, shading='auto')

# 添加色标
cbar = plt.colorbar(temperature_plot, orientation='vertical', pad=0.02, aspect=50)
cbar.set_label('Temperature Change (°C)')

# 设置标题
plt.title('Temperature Change (1982-2020)')

plt.show()

# 创建降水图
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# 绘制中国的轮廓线，solid是实线样式
ax.add_feature(cfeature.BORDERS, linestyle='solid', edgecolor='black')

# 设置颜色映射
cmap = plt.get_cmap('Blues')

# 绘制降水变化量
tp_plot = ax.pcolormesh(longitudes, latitudes, tp_change, cmap=cmap, shading='auto')

# 添加色标
cbar = plt.colorbar(tp_plot, orientation='vertical', pad=0.02, aspect=50)
cbar.set_label('Precipitation (mm)')

# 设置标题
plt.title('Annual China Average Precipitation Change (1982-2020)')
plt.show()

# 创建辐射图
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# 绘制中国的轮廓线，solid是实线样式
ax.add_feature(cfeature.BORDERS, linestyle='solid', edgecolor='black')

# 设置颜色映射
cmap = plt.get_cmap('RdBu_r')

# 绘制辐射变化量
ssrd_plot = ax.pcolormesh(longitudes, latitudes, ssrd_change, cmap=cmap, shading='auto')

# 添加色标
cbar = plt.colorbar(ssrd_plot, orientation='vertical', pad=0.02, aspect=50)
cbar.set_label('Radiation (J/m² or W/m²)')

# 设置标题
plt.title('Annual China Average Radiation Change (1982-2020)')
plt.show()